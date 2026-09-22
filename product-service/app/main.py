from fastapi import FastAPI

from . import models
from .database import engine
from .routers import products

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quick Commerce - Product & Inventory Service")

app.include_router(products.router)


@app.get("/")
def root():
    return {"service": "Product Service", "status": "running"}
