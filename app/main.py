from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import api_routers
from db.session import create_db_and_tables
from exception.exception_handler import add_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    print("Application is shutting down...")

app = FastAPI(
    title="item mgmt service",
    description="",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"]
)

app.include_router(api_routers)
add_exception_handler(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
