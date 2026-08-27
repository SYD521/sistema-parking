from sqlalchemy import DECIMAL
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class ParkingRecord(Base):
    __tablename__ = "estacionamiento"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    placa: Mapped[str] = mapped_column(
        String(10)
    )
    # Sin server_default a propósito: el valor SIEMPRE se fija de forma
    # explícita en ParkingService (en UTC), para que fecha_entrada y
    # fecha_salida provengan del mismo reloj y el cálculo de la tarifa
    # sea consistente, sin depender de la zona horaria configurada en MySQL.
    fecha_entrada: Mapped[DateTime] = mapped_column(
        DateTime
    )
    fecha_salida: Mapped[DateTime | None] = mapped_column(
        DateTime,
        nullable=True
    )
    monto: Mapped[float | None] = mapped_column(
        DECIMAL(10, 2),
        nullable=True
    )
    estado: Mapped[str] = mapped_column(
        Enum("ACTIVO", "FINALIZADO"),
        default="ACTIVO"
    )