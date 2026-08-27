from sqlalchemy.orm import Session
from app.models.parking import ParkingRecord


class ParkingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, record: ParkingRecord):
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_by_id(self, record_id: int):
        return (
            self.db.query(ParkingRecord)
            .filter(ParkingRecord.id == record_id)
            .first()
        )

    def get_activos(self):
        return (
            self.db.query(ParkingRecord)
            .filter(ParkingRecord.estado == "ACTIVO")
            .order_by(ParkingRecord.fecha_entrada.desc())
            .all()
        )

    def get_all(self):
        return (
            self.db.query(ParkingRecord)
            .order_by(ParkingRecord.fecha_entrada.desc())
            .all()
        )

    def update(self):
        self.db.commit()
