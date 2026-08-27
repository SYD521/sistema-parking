from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models
from app.api.parking import router as parking_router

app = FastAPI(
    title="Parking API",
    version="1.0.0",
    description="API para el control de ingreso, salida y tarifas "
                 "de un estacionamiento vehicular."
)

# Habilitado para que el frontend (index.html abierto por separado)
# pueda consumir la API sin bloqueos de CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parking_router)

@app.get("/")
def home():
    return {
        "message": "Parking API funcionando correctamente"
    }

# Servicio de prueba (Endpoint Ping)
@app.get("/api/v1/ping")
def ping():
    return {
    "status": "success",
    "message": "¡Conexión exitosa desde la API!",
    "version": "1.0.0"
    }