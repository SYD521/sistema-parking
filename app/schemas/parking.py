from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class ParkingCreate(BaseModel):
    """Datos requeridos para registrar el ingreso de un vehículo."""
    placa: str


class ParkingResponse(BaseModel):
    """Representación de un registro de estacionamiento."""
    id: int
    placa: str
    fecha_entrada: datetime
    fecha_salida: datetime | None
    monto: float | None
    estado: str

    model_config = ConfigDict(
        from_attributes=True
    )


class ParkingSalidaResponse(BaseModel):
    """Respuesta al procesar la salida: incluye la liquidación."""
    id: int
    placa: str
    fecha_entrada: datetime
    fecha_salida: datetime
    horas_o_fracciones: int
    monto: float
    estado: str

    model_config = ConfigDict(
        from_attributes=True
    )
