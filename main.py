from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.empleados import empleados
from config.openapi import tags_metadata

app = FastAPI(
    title="Comercios Empleados API",
    description="Una REST API usando fastapi y sqlalchemy",
    version="0.0.1",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )

app.include_router(empleados)
