import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_upload_file(client: AsyncClient):
    file_data = {"file": ("test.txt", b"This is file content", "text/plain")}
    response = await client.post("/upload/", files=file_data)
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_download_file(client: AsyncClient):
    response = await client.get("/download/test.txt")
    assert response.status_code == 200
    assert "content" in response.json()
