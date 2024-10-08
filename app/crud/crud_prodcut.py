from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import models
from app.schemas import schemas


async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


async def get_product(db: AsyncSession):
    result = await db.execute(select(models.Product))
    product = result.scalars().all()
    return product


async def get_products_id(db: AsyncSession, product_id: int):
    result = await db.execute(select(models.Product).where(models.Product.id == product_id))
    product = result.scalar_one_or_none()
    return product


async def put_products(db: AsyncSession, product_id: int, product_data: schemas.ProductUpdate):
    result = await get_products_id(db, product_id)
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(result, key, value)
    await db.commit()
    await db.refresh(result)
    return result


async def delete_products(db: AsyncSession, product_id: int):
    result = await get_products_id(db, product_id)
    await db.delete(result)
    await db.commit()