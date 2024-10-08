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
async def test_create_order():
    async with AsyncClient(app=app, base_url="http://test") as client:
        order_data = {
            "items":[
                {
                "product_id": 1,
                "quantity": 1
                }
            ]
        }
        response = await client.post("/orders/", json=order_data)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_orders():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/orders/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_order_by_id():
    async with AsyncClient(app=app, base_url="http://test") as client:
        order_id = 1
        response = await client.get(f"/orders/{order_id}")
        assert response.status_code == 200
        assert response.json()["id"] == order_id


@pytest.mark.asyncio
async def test_update_order_status():
    async with AsyncClient(app=app, base_url="http://test") as client:
        order_id = 1
        update_data = {"status": "доставлен"}
        response = await client.patch(f"/orders/{order_id}/status", json=update_data)
        assert response.status_code == 200
        assert response.json()["status"] == "доставлен"