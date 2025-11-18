from pydantic import BaseModel, Field, ConfigDict, EmailStr
from decimal import Decimal
from typing import Optional

class CategoryCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50, description='Название категории (3-50 символов)')
    parent_id: Optional[int] = Field(None, description='ID родительской категории (если есть)')

class Category(BaseModel):
    id: int = Field(description='ID категории')
    name: str = Field(description='Название категории')
    parent_id: Optional[int] = Field(None, description='ID родительской категории (если есть)')
    is_active: bool = Field(description='Активность категории')

    model_config = ConfigDict(from_attributes=True)

class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100, description='Название товара (3-100 символов)')
    description: str | None = Field(None, max_length=500, description='Описание товара (до 500 символов)')
    price: Decimal = Field(gt=0, description='Цена товара (больше 0)', decimal_places=2)
    image_url: str | None = Field(None, max_length=200, description='URL изображения товара')
    stock: int = Field(ge=0, description='Количество товара на складе (0 и больше)')
    category_id: int = Field(description='ID категории, к которой относится товар')

class Product(BaseModel):
    id: int = Field(description='ID продукта')
    name: str = Field(description='Название товара')
    description: str | None = Field(None, description='Описание товара')
    price: Decimal = Field(description='Цена товара в рублях', gt=0, decimal_places=2)
    image_url: str | None = Field(None, description='URL изображение товара')
    stock: int = Field(description='Количество товара на складе')
    category_id: int = Field(description='ID категории')
    is_active: bool = Field(description='Активность товара')
    seller_id: int = Field(description='ID продавца')

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr = Field(description='Email пользователя')
    password: str = Field(min_length=8, description='Пароль пользователя (минимум 8 символов)')
    role: str = Field(default='buyer', pattern='^(buyer|seller)$', description='Роль: "buyer" или "seller")')

class User(BaseModel):
    id: int = Field(description='ID пользователя')
    email: EmailStr = Field(description='Email пользователя')
    is_active: bool = Field(description='Активность пользователя')
    role: str = Field(description='Роль пользователя')

    model_config = ConfigDict(from_attributes=True)