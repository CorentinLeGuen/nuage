import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine


@pytest.fixture(scope="function")
async def db_session():
    async with AsyncSession(engine) as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        yield ac