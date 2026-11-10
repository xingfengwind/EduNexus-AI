import httpx
import pytest

from app.api.health import app


@pytest.mark.asyncio
async def test_health_contract():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app), base_url="http://test"
    ) as client:
        response = await client.get("/internal/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "edunexus-ai"}


@pytest.mark.asyncio
async def test_no_business_routes_exposed():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app), base_url="http://test"
    ) as client:
        response = await client.get("/internal/v1/tasks")
    assert response.status_code == 404
