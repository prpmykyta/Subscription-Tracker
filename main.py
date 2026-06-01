from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.v1.users import router as users_router
from app.api.v1.subscriptions import router as subscriptions_router

from app.database import engine
from app.create_tables import create_tables


@asynccontextmanager
async def lifespan(app):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan, title="SubTrack")

def custom_generate_unique_id(route: APIRoute):
    return route.name
app.router.generate_unique_id_function = custom_generate_unique_id

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(subscriptions_router, prefix="/api/v1", tags=["subscriptions"])

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("app/static/index.html")