from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db import get_db
import api.cruds.products as products_cruds

router = APIRouter()

@router.get("/products-all")
def get_products(db: Session = Depends(get_db)):
    return products_cruds.get_all_products(db)

@router.get("/products-by-category/{category}")
def get_products_by_category(category: str, db: Session = Depends(get_db)):
    return products_cruds.get_products_by_category(category, db)

@router.get("/products-by-maker/{maker}")
def get_products_by_maker(maker: str, db: Session = Depends(get_db)):
    return products_cruds.get_cpu_by_maker(maker, db)

@router.get("/product-by-id/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    return products_cruds.get_product_by_id(id, db)