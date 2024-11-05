# src/main.py
from fastapi import FastAPI
import friends, database
from database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(friends.router, prefix="/api/v1")
