from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from backend.app.core.config import settings
from backend.app.routers.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "API REST para el Sistema Bibliotecario de la Universidad Politécnico de la Costa Atlántica (PCA). "
        "Construida con arquitectura limpia modular de 3 capas (Routers, Services, Repositories)."
    ),
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montaje de rutas de la API bajo /api/v1
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.middleware("http")
async def add_utf8_header(request: Request, call_next) -> Response:
    """Garantiza que todas las respuestas JSON incluyan charset=utf-8."""
    response = await call_next(request)
    if "application/json" in response.headers.get("content-type", ""):
        response.headers["content-type"] = "application/json; charset=utf-8"
    return response


@app.get("/", tags=["Salud del Sistema"], summary="Verificación del estado de la API")
def root():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "documentation": "/docs"
    }
