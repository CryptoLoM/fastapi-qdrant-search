from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import search
from service import search_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code executed at startup
    print("Starting up... Checking Qdrant collection.")
    search_service.recreate_collection()
    yield
    # Code executed when shutting down
    print("Shutting down...")

app = FastAPI(title="Semantic Search Service", lifespan=lifespan)

app.include_router(search.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Semantic Search Service is running"}