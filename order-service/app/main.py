from fastapi import FastAPI

from . import models
from .database import engine
from .routers import orders

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quick Commerce - Order Service")

app.include_router(orders.router)


@app.get("/")
def root():
    return {"service": "Order Service", "status": "running"}
