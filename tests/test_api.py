import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_api_health(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 401
