import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[2] / "contracts" / "events"


def test_shared_event_fixtures():
    schema = json.loads((ROOT / "envelope.schema.json").read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    validator.validate(json.loads((ROOT / "valid.json").read_text()))
    with pytest.raises(ValidationError):
        validator.validate(json.loads((ROOT / "invalid-version.json").read_text()))
