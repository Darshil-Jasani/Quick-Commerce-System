from fastapi import FastAPI

from . import models
from .database import engine
from .routers import users

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quick Commerce - User Service")

app.include_router(users.router)


@app.get("/")
def root():
    return {"service": "User Service", "status": "running"}
