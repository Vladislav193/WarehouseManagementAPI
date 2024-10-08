from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from app.models import models
from app.schemas import schemas
from fastapi import HTTPException

async def create_order(db: AsyncSession, order: schemas.OrderCreate):
    new_order = models.Order(status=models.OrderStatus.in_process)
    db.add(new_order)
    await db.flush()
    for item in order.items:
        print(item)
        product = await db.get(models.Product, item.product_id)
        print(product.quantity)
        if product.quantity >= item.quantity:
            order_item = models.OrderItem(order_id=new_order.id, product_id=product.id, quantity=item.quantity)
            db.add(order_item)
            product.quantity -= item.quantity
        else:
            raise ValueError(f'Недостаточно товара {item.product_id}')
    await db.commit()
    await db.refresh(new_order)
    result = await db.execute(
        select(models.Order).options(selectinload(models.Order.items)).where(models.Order.id ==new_order.id)
    )
    order_with_items = result.scalar_one_or_none()
    return order_with_items


async def get_all_order(db: AsyncSession):
    result = await db.execute(
        select(models.Order).options(selectinload(models.Order.items))
    )
    order = result.scalars().all()
    return order


async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(
        select(models.Order).options(selectinload(models.Order.items)).where(models.Order.id ==order_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Product not found")
    return order


async def path_order_status(db: AsyncSession, order_id: int, status:schemas.OrderUpdate):
    result = await get_order(db, order_id)
    result.status = status.status
    await db.commit()
    await db.refresh(result)
    return result