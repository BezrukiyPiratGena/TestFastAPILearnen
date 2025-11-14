from decimal import Decimal
from sqlalchemy import Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(200), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)

    category: Mapped['Category'] = relationship('Category',back_populates='products')




from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Text, DateTime, Table, Column, Date
from datetime import date

class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = 'projects'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)

    employee_id: Mapped[list['Participation']] = relationship('Employee', secondary='participations', back_populates='project_id')

class Employee(Base):
    __tablename__ = 'employees'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    project_id: Mapped[list['Participation']] = relationship('Project', secondary='participations', back_populates='employee_id')

class Participation(Base):
    __tablename__ = 'participations'
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey('employees.id'), primary_key=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False)

    projects: Mapped['Project'] = relationship(back_populates='project_id')
    employees: Mapped['Employee'] = relationship(back_populates='employee_id')




