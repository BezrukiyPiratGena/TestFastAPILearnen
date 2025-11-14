from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.products import Product as ProductModel
from app.models.categories import Category as CategoryModel
from app.schemas import Product as ProductSchema, ProductCreate
from app.db_depends import get_db, get_async_db

router = APIRouter(prefix='/products', tags=['products'])

@router.get('/', status_code=status.HTTP_200_OK, response_model=list[ProductSchema])
async def get_all_products(db: AsyncSession = Depends(get_async_db)):
    stmt = select(ProductModel).where(ProductModel.is_active == True)
    temp = await db.scalars(stmt)
    products = temp.all()
    return products


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProductSchema)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_async_db)):

    temp = await db.scalars(select(CategoryModel).where(CategoryModel.id == product.category_id, CategoryModel.is_active == True))
    product_is_have = temp.first()

    if product_is_have is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')

    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


@router.get('/category/{category_id}', status_code=status.HTTP_200_OK, response_model=list[ProductSchema])
async def get_product_by_category(category_id: int, db: AsyncSession = Depends(get_async_db)):

    temp = await db.scalars(select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.is_active == True))
    category_is_have = temp.first()
    if category_is_have is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found or inactive')

    temp = await db.scalars(select(ProductModel).where(ProductModel.category_id == category_id, ProductModel.is_active == True))
    products = temp.all()
    return products


@router.get('/{product_id}', response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def get_product(product_id: int, db: AsyncSession = Depends(get_async_db)):
    temp = await db.scalars(select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True))
    product_is_have = temp.first()
    if product_is_have is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    temp = await db.scalars(select(CategoryModel).where(CategoryModel.id == product_is_have.category_id, CategoryModel.is_active == True))
    category_is_have = temp.first()
    if category_is_have is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category not found')
    return product_is_have


@router.put('/{product_id}', response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def update_product(product_id: int, product: ProductCreate, db: AsyncSession = Depends(get_async_db)):
    temp = await db.scalars(select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True))
    product_is_have = temp.first()
    if product_is_have is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    temp = await db.scalars(select(CategoryModel).where(CategoryModel.id == product.category_id, CategoryModel.is_active == True))
    category_is_have = temp.first()
    if category_is_have is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category not found')
    await db.execute(update(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True).values(**product.model_dump()))
    await db.commit()
    await db.refresh(product_is_have)
    return product_is_have

@router.delete('/{product_id}', status_code=status.HTTP_200_OK, response_model=ProductSchema)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_async_db)):
    temp = await db.scalars(
        select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True))

    product_is_have = temp.first()
    if product_is_have is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    await db.execute(update(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True).values(is_active = False))
    await db.commit()
    return product_is_have
