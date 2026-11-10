"""Verify isolated phase-zero data survives container restart; no credentials are printed."""

import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

ROOT = Path(__file__).resolve().parents[1]
COMPOSE = [
    "docker",
    "compose",
    "--env-file",
    str(ROOT / "deploy/.env"),
    "-f",
    str(ROOT / "deploy/compose.yaml"),
    "-f",
    str(ROOT / "deploy/compose.local.yaml"),
]


def run(*args):
    return subprocess.run(
        COMPOSE + list(args), capture_output=True, text=True, check=True
    ).stdout.strip()


def mysql(sql):
    return run(
        "exec",
        "-T",
        "mysql",
        "sh",
        "-c",
        'MYSQL_PWD="$MYSQL_PASSWORD" mysql -u "$MYSQL_USER" -N -D edunexus -e "$1"',
        "sh",
        sql,
    )


def ready(check):
    deadline = time.monotonic() + 180
    while time.monotonic() < deadline:
        try:
            return check()
        except (subprocess.CalledProcessError, BotoCoreError, ClientError):
            time.sleep(2)
    raise RuntimeError("Infrastructure readiness deadline exceeded; inspect container logs locally")


def main():
    values = dict(
        line.split("=", 1)
        for line in (ROOT / "deploy/.env").read_text().splitlines()
        if line and not line.startswith("#")
    )
    s3 = boto3.client(
        "s3",
        endpoint_url="http://127.0.0.1:19000",
        aws_access_key_id=values["RUSTFS_ACCESS_KEY"],
        aws_secret_access_key=values["RUSTFS_SECRET_KEY"],
        region_name="us-east-1",
        config=Config(
            s3={"addressing_style": "path"},
            retries={"max_attempts": 1},
            connect_timeout=3,
            read_timeout=3,
        ),
    )
    run("up", "-d")
    ready(lambda: mysql("SELECT 1"))
    ready(s3.list_buckets)
    ready(lambda: run("exec", "-T", "redis", "redis-cli", "ping"))
    mysql(
        "CREATE TABLE IF NOT EXISTS phase_zero_probe (id INT PRIMARY KEY, value VARCHAR(32)); INSERT INTO phase_zero_probe VALUES (1,'synthetic') ON DUPLICATE KEY UPDATE value='synthetic'"
    )
    run("exec", "-T", "redis", "redis-cli", "SET", "phase-zero-probe", "synthetic")
    bucket = "edunexus-phase-zero-probe"
    if bucket not in [item["Name"] for item in s3.list_buckets()["Buckets"]]:
        s3.create_bucket(Bucket=bucket)
    s3.put_object(Bucket=bucket, Key="synthetic.txt", Body=b"synthetic")
    try:
        urllib.request.urlopen(f"http://127.0.0.1:19000/{bucket}/synthetic.txt", timeout=5)
    except urllib.error.HTTPError as exc:
        assert exc.code in (401, 403), "Anonymous objects must be forbidden"
    else:
        raise AssertionError("Anonymous object access unexpectedly succeeded")
    run("restart", "mysql", "redis", "rustfs")
    ready(lambda: mysql("SELECT 1"))
    ready(s3.list_buckets)
    assert mysql("SELECT value FROM phase_zero_probe WHERE id=1") == "synthetic"
    assert (
        ready(lambda: run("exec", "-T", "redis", "redis-cli", "GET", "phase-zero-probe"))
        == "synthetic"
    )
    assert s3.get_object(Bucket=bucket, Key="synthetic.txt")["Body"].read() == b"synthetic"
    mysql("DELETE FROM phase_zero_probe WHERE id=1")
    run("exec", "-T", "redis", "redis-cli", "DEL", "phase-zero-probe")
    s3.delete_object(Bucket=bucket, Key="synthetic.txt")
    print("PASS: MySQL, Redis and private RustFS objects persisted across restart")


if __name__ == "__main__":
    main()
