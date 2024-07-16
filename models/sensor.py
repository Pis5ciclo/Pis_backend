from app import db
import uuid
from models.type_sensor import TypeSensor
from sqlalchemy import Enum as EnumSQL

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(15), default='activo')
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    ip = db.Column(db.String(20))
    type_sensor = db.Column(EnumSQL(TypeSensor))
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )
    datos = db.relationship('SensorData', backref='sensor', lazy=True)


    @property
    def serialize(self):
        return {
            "name": self.name,
            "status": self.status,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "ip": self.ip,
            "type_sensor": self.type_sensor.serialize if self.type_sensor else None,
            "external_id": self.external_id,
        }
    @property     
    def serialize(self):
            return {
                "name": self.name,
                "status": self.status,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "ip": self.ip,
                "type_sensor": self.type_sensor.serialize if self.type_sensor else None,
                "external_id": self.external_id,
            }