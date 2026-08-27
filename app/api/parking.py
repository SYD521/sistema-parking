from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.parking_repository import ParkingRepository
from app.schemas.parking import ParkingCreate
from app.schemas.parking import ParkingResponse
from app.schemas.parking import ParkingSalidaResponse
from app.services.parking_service import ParkingService

router = APIRouter(
    prefix="/parqueadero",
    tags=["Estacionamiento"]
)


@router.post(
    "/ingreso",
    response_model=ParkingResponse
)
def registrar_ingreso(
    data: ParkingCreate,
    db: Session = Depends(get_db)
):
    try:
        repository = ParkingRepository(db)
        service = ParkingService(repository)
        return service.registrar_ingreso(data)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get(
    "/activos",
    response_model=list[ParkingResponse]
)
def get_activos(
    db: Session = Depends(get_db)
):
    repository = ParkingRepository(db)
    service = ParkingService(repository)
    return service.get_activos()


@router.get(
    "/historial",
    response_model=list[ParkingResponse]
)
def get_historial(
    db: Session = Depends(get_db)
):
    repository = ParkingRepository(db)
    service = ParkingService(repository)
    return service.get_all()


@router.put(
    "/salida/{record_id}",
    response_model=ParkingSalidaResponse
)
def registrar_salida(
    record_id: int,
    db: Session = Depends(get_db)
):
    try:
        repository = ParkingRepository(db)
        service = ParkingService(repository)
        record, fracciones = service.registrar_salida(record_id)

        return ParkingSalidaResponse(
            id=record.id,
            placa=record.placa,
            fecha_entrada=record.fecha_entrada,
            fecha_salida=record.fecha_salida,
            horas_o_fracciones=fracciones,
            monto=float(record.monto),
            estado=record.estado
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
