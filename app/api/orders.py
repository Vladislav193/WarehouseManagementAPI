from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import crud_order
from app.schemas import schemas
from app.database import get_db


router = APIRouter()


@router.post("/", response_model=schemas.OrderCreate)
async def order_create(order: schemas.OrderCreate, db: AsyncSession = Depends(get_db)):
    new_order = await crud_order.create_order(db, order)
    return new_order


@router.get("/", response_model=List[schemas.OrderOut])
async def order_get(db: AsyncSession = Depends(get_db)):
    order = await crud_order.get_all_order(db)
    return order


@router.get("/{order_id}", response_model=schemas.OrderOut)
async def order_get(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await crud_order.get_order(db, order_id)
    return order


@router.patch("/{order_id}/status", response_model=schemas.OrderOut)
async def order_path(order_id: int, status: schemas.OrderUpdate, db: AsyncSession = Depends(get_db)):
    print('paaaaaaaath')
    order = await crud_order.path_order_status(db, order_id, status)
    return order