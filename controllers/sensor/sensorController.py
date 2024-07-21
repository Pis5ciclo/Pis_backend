from models.sensor import Sensor
from datetime import datetime
from flask import jsonify
from models.type_sensor import TypeSensor
from models.sensordata import SensorData
import uuid
from app import db
import re
from models.person import Person
from models.type_sensor import TypeSensor
class SensorController:

    validate_ip = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')


    def validate_latitude_longitude(self, latitude, longitude):
        latitude = float(latitude)
        longitude = float(longitude)
        if -90 <= latitude <= 90 and -180 <= longitude <= 180:
            return True
        else:
            return -21
        
    def listSensor(self):
        sensors = Sensor.query.all()
        sensorsList = []
        for sensor in sensors:
            sensorr = {
                "external_id": sensor.external_id,
                "ip": sensor.ip,
                "latitude": sensor.latitude,
                "longitude": sensor.longitude,
                "name": sensor.name,
                "status": sensor.status,
                "type_sensor": sensor.type_sensor.name if sensor.type_sensor else None,
            }
            sensorsList.append(sensorr)
        return sensorsList
    
    def listSensorName(self):
        active_sensors = Sensor.query.filter_by(status='activo').all()
        sensor_list = [{'id': sensor.id, 'name': sensor.name} for sensor in active_sensors]
        return sensor_list

    def save_sensor(self, data):
        repeated_ip = Sensor.query.filter_by(ip=data["ip"]).first()
        if repeated_ip:
            return -23
        
        if not self.validate_ip.match(data['ip']):
            return -10 
        
        latitude = data["latitude"]
        longitude = data["longitude"]
        validation_result = self.validate_latitude_longitude(latitude, longitude)
        if validation_result != True:
            return validation_result
        
        try:
            sensor = Sensor(
                name=data["name"],
                latitude=float(latitude),
                longitude=float(longitude),
                ip=data["ip"],
                type_sensor=data["type_sensor"],
                external_id=uuid.uuid4()
            )
            db.session.add(sensor)
            db.session.commit()
            return 2 
        except Exception as e:
            db.session.rollback()
            return -9


    def modify_sensor(self, external_id, data):
        sensor = Sensor.query.filter_by(external_id=external_id).first()
        repeated_ip = Sensor.query.filter_by(ip=data["ip"]).first()
        if repeated_ip:
            return -23
        if sensor:
            if not self.validate_ip.match(data.get('ip')):
                return {"error": "Invalid IP format"}, 400
            
            latitude = data.get("latitude", sensor.latitude)
            longitude = data.get("longitude", sensor.longitude)
            validation_result = self.validate_latitude_longitude(latitude, longitude)
            if validation_result is not True:
                return {"error": validation_result}, 400
            
            sensor.name = data.get("name", sensor.name)
            sensor.latitude = latitude
            sensor.longitude = longitude
            sensor.ip = data.get("ip", sensor.ip)
            sensor.type_sensor = data.get("type_sensor", sensor.type_sensor)
            
            db.session.commit()
            return sensor
        else:
            return -9


    
    def deactivate_sensor(self, external_id):
        sensor = Sensor.query.filter_by(external_id=external_id).first()
        if sensor:
            if sensor.status == "activo":
                sensor.status = "desactivo"
            else:
                sensor.status = "activo"
            db.session.commit()
            return 5
        else:
            return -20

        
    def search_sensor(self, name):
        name = Sensor.query.filter_by(name = name).first()
        if name:
            return name
        else:
            return -3
        
    def all_types(self):
        try:
            # Obtén la lista de todos los tipos de sensores
            sensors_data = TypeSensor.all_types()
            return sensors_data, 200  # Devuelve los datos y un código de estado 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500 
    def guardar_datos_sensor(self, data):
        tds_value = data.get('tds')
        ip_address = data.get('ip')
        timestamp = data.get('timestamp') 

        sensor = Sensor.query.filter_by(ip=ip_address).first()

        if not sensor:
            sensor = Sensor(ip=ip_address, type_sensor=TypeSensor.AGUA)
            db.session.add(sensor)
            db.session.commit()
        fecha, hora = timestamp.split('T')
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        hora_obj = datetime.strptime(hora, '%H:%M:%S').time()

            # Crear un nuevo dato para ese sensor
        new_dato = SensorData(data=tds_value, date=fecha_obj, hour=hora_obj, sensor_id=sensor.id)

            # Guardar en la base de datos
        db.session.add(new_dato)
        db.session.commit()

        return jsonify({'message': 'Datos guardados correctamente.'}), 200
    

    def guardar_datos_sensor_aire(self, data):
        valor_sensor = data.get('data')
        ip_address = data.get('ip')
        timestamp = data.get('timestamp')
        sensor = Sensor.query.filter_by(ip=ip_address).first()

        if not sensor:
            sensor = Sensor(ip=ip_address, type_sensor=TypeSensor.AIRE)
            db.session.add(sensor)
            db.session.commit()

        fecha, hora = timestamp.split('T')
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        hora_obj = datetime.strptime(hora, '%H:%M:%S').time()

        new_dato = SensorData(data=valor_sensor, date=fecha_obj, hour=hora_obj, sensor_id =sensor.id)

        db.session.add(new_dato)
        db.session.commit()

        return jsonify({'message': 'Datos guardados correctamente.'}), 200