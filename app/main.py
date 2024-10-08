from fastapi import FastAPI
from app.api import products
from app.api import orders
from app.database import engine
from app.models.models import Base


app = FastAPI()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await create_tables()


app.include_router(products.router, prefix='/products', tags=["Products"])
app.include_router(orders.router, prefix='/orders', tags=["Orders"])