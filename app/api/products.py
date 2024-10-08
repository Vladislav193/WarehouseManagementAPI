from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import crud_prodcut
from app.schemas import schemas
from app.database import get_db


router = APIRouter()


@router.post("/", response_model=schemas.ProductCreate)
async def create_products(product: schemas.ProductCreate, db: AsyncSession= Depends(get_db)):
    new_product = await crud_prodcut.create_product(db=db, product=product)
    return new_product


@router.get("/", response_model=List[schemas.ProductOut])
async def get_products(db:AsyncSession = Depends(get_db)):
    products = await crud_prodcut.get_product(db=db)
    return products


@router.get("/{product_id}", response_model=schemas.ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud_prodcut.get_products_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=schemas.ProductUpdate)
async def put_product(product_id: int, product: schemas.ProductUpdate, db: AsyncSession = Depends(get_db)):
    up_product = await crud_prodcut.put_products(db, product_id, product)
    if up_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return up_product


@router.delete("/{product_id}", response_model=schemas.ProductOut)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud_prodcut.delete_products(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
