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
    products = products_cruds.get_products_by_category(category, db)
    if not products:
        raise HTTPException(status_code=404, detail="Products not found for this category")
    return products

@router.get("/products-by-maker/{maker}")
def get_products_by_maker(maker: str, db: Session = Depends(get_db)):
    products = products_cruds.get_cpu_by_maker(maker, db)
    if not products:
        raise HTTPException(status_code=404, detail="Products not found for this maker")
    return products