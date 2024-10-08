import asyncio
import pytest
from httpx import AsyncClient
from app.main import app
from app.database import Base, engine


@pytest.fixture(scope="session")
async def db_setup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client(db_setup):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(app=app, base_url="http://test") as client:
        data_json = {
            "name": "Test Product",
            "description": "A sample product",
            "price": 10.0,
            "quantity": 100
        }
        response = await client.post("/products/", json=data_json)
        assert response.status_code == 200
        assert response.json()["name"] == "Test Product"
        assert response.json()["price"] == 10.0


@pytest.mark.asyncio
async def test_get_product():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/products/", )
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_product_id():
    async with AsyncClient(app=app, base_url="http://test") as client:
        product_id = 1
        response = await client.get(f"/products/{product_id}", )
        assert response.status_code == 200
        assert response.json()["id"] == product_id


@pytest.mark.asyncio
async def test_update_product_id():
    async with AsyncClient(app=app, base_url="http://test") as client:
        product_id = 6
        data_json = {
            "name": "Test",
            "description": "A sample product",
            "price": 10.0,
            "quantity": 90
        }
        response = await client.put(f"/products/{product_id}", json=data_json )
        assert response.status_code == 200
        assert response.json()["name"] == data_json["name"]
        assert response.json()["price"] == data_json["price"]


@pytest.mark.asyncio
async def test_update_product_id():
    async with AsyncClient(app=app, base_url="http://test") as client:
        product_id = 7
        response = await client.delete(f"/products/{product_id}")
        assert response.status_code == 404