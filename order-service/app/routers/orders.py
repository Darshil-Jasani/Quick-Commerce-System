import os
from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

# Other services' base URLs (overridable via environment variables)
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://127.0.0.1:8001")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://127.0.0.1:8002")


@router.post("/", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # 1. Verify the user exists (User Service)
    try:
        user_resp = requests.get(f"{USER_SERVICE_URL}/users/{order.user_id}", timeout=5)
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="User Service unavailable")
    if user_resp.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Verify the product exists in that store (Product Service)
    try:
        product_resp = requests.get(
            f"{PRODUCT_SERVICE_URL}/stores/{order.store_id}/products/{order.product_id}",
            timeout=5,
        )
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Product Service unavailable")
    if product_resp.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found in this store")

    product = product_resp.json()

    # 3. Check stock availability
    if product["stock_quantity"] < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock for this product")

    # 4. Calculate total price
    total_price = product["price"] * order.quantity

    # 5. Reserve stock by decrementing it in the Product Service
    stock_resp = requests.put(
        f"{PRODUCT_SERVICE_URL}/stores/{order.store_id}/products/{order.product_id}/stock",
        json={"quantity_change": -order.quantity},
        timeout=5,
    )
    if stock_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to reserve stock")

    # 6. Save the order
    db_order = models.Order(
        user_id=order.user_id,
        store_id=order.store_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total_price,
        status="PLACED",
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/", response_model=List[schemas.OrderOut])
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()


@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=schemas.OrderOut)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.status = order.status
    db.commit()
    db.refresh(db_order)
    return db_order


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted successfully"}
