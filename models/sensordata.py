from app import db
import uuid
from datetime import datetime
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DECIMAL(10, 2), default=0.0)
    date = db.Column(db.Date, default=datetime.now().date)
    hour = db.Column(db.Time)
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    
    @property
    def serialize(self):
        return {
            "data": self.data,
            "date": self.date,
            "hour": self.hour,
            "external_id": str(self.external_id),
            "id_sensor": self.sensor_id
        }
