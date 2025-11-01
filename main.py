from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.auth_endpoints import router as auth_router

# Crear aplicación FastAPI
app = FastAPI(
    title="API de Gestión de Torneos de Ajedrez",
    description="API REST para gestionar torneos de ajedrez con autenticación JWT y sistema de roles",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_router)


# Ruta raíz
@app.get("/")
async def root():
    """
    Ruta raíz de la API.
    """
    return {
        "message": "API de Gestión de Torneos de Ajedrez",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
