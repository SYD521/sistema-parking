import math
from datetime import datetime
from datetime import timezone

from app.core.config import TARIFA_POR_FRACCION
from app.models.parking import ParkingRecord
from app.repositories.parking_repository import ParkingRepository
from app.schemas.parking import ParkingCreate


def _ahora_utc():
    """
    Hora actual en UTC, sin tzinfo (naive), para guardar en la columna
    DATETIME de MySQL. Se usa SIEMPRE esta función -y nunca el
    CURRENT_TIMESTAMP de MySQL ni datetime.now() sin más- para que
    fecha_entrada y fecha_salida vengan del mismo reloj y sean
    directamente restables entre sí.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


class ParkingService:
    def __init__(self, repository: ParkingRepository):
        self.repository = repository

    def registrar_ingreso(self, data: ParkingCreate):
        placa = data.placa.strip().upper()

        if not placa:
            raise Exception("La placa es obligatoria.")

        nuevo_registro = ParkingRecord(
            placa=placa,
            fecha_entrada=_ahora_utc(),
            estado="ACTIVO"
        )
        return self.repository.create(nuevo_registro)

    def get_activos(self):
        return self.repository.get_activos()

    def get_all(self):
        return self.repository.get_all()

    def registrar_salida(self, record_id: int):
        record = self.repository.get_by_id(record_id)

        if record is None:
            raise Exception("Registro no encontrado.")

        if record.estado == "FINALIZADO":
            raise Exception("Este vehículo ya registró su salida.")

        fecha_salida = _ahora_utc()
        record.fecha_salida = fecha_salida

        # --- Cálculo de la tarifa: $0.50 por hora o fracción de hora ---
        minutos_transcurridos = (
            fecha_salida - record.fecha_entrada
        ).total_seconds() / 60

        # Toda fracción de hora (incluso 1 minuto) cuenta como una hora completa
        fracciones = max(1, math.ceil(minutos_transcurridos / 60))

        monto = round(fracciones * TARIFA_POR_FRACCION, 2)

        record.monto = monto
        record.estado = "FINALIZADO"

        self.repository.update()

        return record, fracciones