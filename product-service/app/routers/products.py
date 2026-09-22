from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/stores", tags=["Stores & Products"])


# ---------------- Store Endpoints ----------------
@router.post("/", response_model=schemas.StoreOut)
def create_store(store: schemas.StoreCreate, db: Session = Depends(get_db)):
    db_store = models.Store(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


@router.get("/", response_model=List[schemas.StoreOut])
def get_stores(db: Session = Depends(get_db)):
    return db.query(models.Store).all()


@router.get("/{store_id}", response_model=schemas.StoreOut)
def get_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.put("/{store_id}", response_model=schemas.StoreOut)
def update_store(store_id: int, store: schemas.StoreUpdate, db: Session = Depends(get_db)):
    db_store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    for key, value in store.dict(exclude_unset=True).items():
        setattr(db_store, key, value)
    db.commit()
    db.refresh(db_store)
    return db_store


@router.delete("/{store_id}")
def delete_store(store_id: int, db: Session = Depends(get_db)):
    db_store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    db.delete(db_store)
    db.commit()
    return {"message": "Store deleted successfully"}


# ---------------- Product Endpoints ----------------
@router.post("/{store_id}/products", response_model=schemas.ProductOut)
def create_product(store_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    db_product = models.Product(store_id=store_id, **product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/{store_id}/products", response_model=List[schemas.ProductOut])
def get_products(store_id: int, db: Session = Depends(get_db)):
    return db.query(models.Product).filter(models.Product.store_id == store_id).all()


@router.get("/{store_id}/products/{product_id}", response_model=schemas.ProductOut)
def get_product(store_id: int, product_id: int, db: Session = Depends(get_db)):
    product = (
        db.query(models.Product)
        .filter(models.Product.store_id == store_id, models.Product.id == product_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found in this store")
    return product


@router.put("/{store_id}/products/{product_id}", response_model=schemas.ProductOut)
def update_product(
    store_id: int, product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)
):
    db_product = (
        db.query(models.Product)
        .filter(models.Product.store_id == store_id, models.Product.id == product_id)
        .first()
    )
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found in this store")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{store_id}/products/{product_id}")
def delete_product(store_id: int, product_id: int, db: Session = Depends(get_db)):
    db_product = (
        db.query(models.Product)
        .filter(models.Product.store_id == store_id, models.Product.id == product_id)
        .first()
    )
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found in this store")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}


# ---------------- Stock Endpoint (used internally by Order Service) ----------------
@router.put("/{store_id}/products/{product_id}/stock", response_model=schemas.ProductOut)
def update_stock(
    store_id: int, product_id: int, stock: schemas.StockUpdate, db: Session = Depends(get_db)
):
    db_product = (
        db.query(models.Product)
        .filter(models.Product.store_id == store_id, models.Product.id == product_id)
        .first()
    )
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found in this store")

    new_quantity = db_product.stock_quantity + stock.quantity_change
    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    db_product.stock_quantity = new_quantity
    db.commit()
    db.refresh(db_product)
    return db_product
