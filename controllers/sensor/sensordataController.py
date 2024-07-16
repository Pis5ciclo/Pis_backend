from datetime import datetime, timedelta
from decimal import Decimal 

from flask import jsonify, request
from models.sensor import Sensor
from models.sensordata import SensorData
from app import db


class SensorDataController:
    def get_sensor_data(self):
        sensor_data = SensorData.query.filter_by(sensor_id=1).all()  # Filtra por el ID del sensor que deseas mostrar
        if not sensor_data:
            return jsonify({"msg": "Sensor data not found", "code": 404}), 404

        data = []
        for sensor in sensor_data:
            data.append({
                'id': sensor.id,
                'data': sensor.data,
                'date': sensor.date.strftime('%Y-%m-%d'),
                'hour': sensor.hour.strftime('%H:%M:%S') if sensor.hour else None
            })
        return data, 200
    
    def search_data_date(self):
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        if not start_date_str or not end_date_str:
            return jsonify({"msg": "Start date and end date are required", "code": 400}), 400

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({"msg": "Invalid date format", "code": 400}), 400

        sensor_data = SensorData.query.filter(SensorData.sensor_id == 1, SensorData.date >= start_date, SensorData.date <= end_date).all()
        
        if not sensor_data:
            return jsonify({"msg": "Sensor data not found", "code": 404}), 404

        data = []
        for sensor in sensor_data:
            data.append({
                'id': sensor.id,
                'data': sensor.data,
                'date': sensor.date.strftime('%Y-%m-%d'),
                'hour': sensor.hour.strftime('%H:%M:%S') if sensor.hour else None
            })
        return jsonify(data), 200

    def get_interpolated_sensor_data(self):
        data, status_code = self.get_sensor_data()

        if status_code != 200:
            return data, status_code

        interpolated_data = self.linear_interpolation(data)
        return interpolated_data, 200

    def linear_interpolation(self, data):
        if not data:
            return []

        interpolated_data = []

        data = sorted(data, key=lambda x: (x['date'], x['hour']))

        for i in range(len(data) - 1):
            current = data[i]
            next_data = data[i + 1]

            if isinstance(current['date'], str):
                current_date = datetime.strptime(current['date'], '%Y-%m-%d').date()
            else:
                current_date = current['date']

            if isinstance(next_data['date'], str):
                next_date = datetime.strptime(next_data['date'], '%Y-%m-%d').date()
            else:
                next_date = next_data['date']

            delta_days = (next_date - current_date).days
            num_points = delta_days if delta_days > 0 else 1  

            for j in range(num_points):
                interp_date = current_date + timedelta(days=j)

                if 'hour' in current and 'hour' in next_data:
                    current_time = datetime.strptime(current['hour'], '%H:%M:%S').time()
                    next_time = datetime.strptime(next_data['hour'], '%H:%M:%S').time()
                    interp_time = (datetime.combine(datetime.min, current_time) + (datetime.combine(datetime.min, next_time) - datetime.combine(datetime.min, current_time)) * (j / num_points)).time()
                    interp_datetime = datetime.combine(interp_date, interp_time)
                else:
                    interp_datetime = interp_date

                # Interpolación lineal para el valor
                interp_value = float(current['data']) + (float(next_data['data']) - float(current['data'])) * (j / num_points)

                interpolated_data.append({
                    'data': interp_value,
                    'date': interp_datetime.strftime('%Y-%m-%d'),
                    'hour': interp_datetime.strftime('%H:%M:%S') if 'hour' in current and 'hour' in next_data else None
                })

        return interpolated_data
    
    def list_sensor_data(self):
        today_date = datetime.now().date()
        sensors = (db.session.query(Sensor).join(SensorData).filter(SensorData.date == today_date).all())
        data = []
        for sensor in sensors:
            sensor_info = {
                "name": sensor.name,
                "latitude": sensor.latitude,
                "longitude": sensor.longitude,
                "ip": sensor.ip,
                "type_sensor": sensor.type_sensor.serialize,
                "datoRecolectado": []
            }
            
            for sensor_data in sensor.dato_recolectado:
                sensor_info["datoRecolectado"].append(
                    {
                        "data": sensor_data.data,
                        "date": str(sensor_data.date),
                        "hour": str(sensor_data.hour),
                    }
                )
            data.append(sensor_info)
        return data
    
    def list_sensor_type(self, value):
        list = Sensor.query.filter_by(type_sensor=value).all()
        if not list:
            return -20
        datos = []
        for sensor in list:
            data_sensor = {
                "name": sensor.name,
                "latitude": sensor.latitude,
                "longitude": sensor.longitude,
                "type_sensor": sensor.type_sensor.serialize,
                "dato_recolectado": [
                    {
                        "data": str(dato.data),
                        "date": str(dato.date),
                        "hour": dato.hour
                    } for dato in sensor.dato_recolectado
                ]
            }
            datos.append(data_sensor)
        return datos

    def list_sensor_name(self, value):
        list = Sensor.query.filter_by(name=value).all()
        if not list:
            return -20
        datos = []
        for sensor in list:
            data_sensor = {
                "name": sensor.name,
                "latitude": sensor.latitude,
                "longitude": sensor.longitude,
                "type_sensor": sensor.type_sensor.serialize,
                "dato_recolectado": [
                    {
                        "data": str(dato.data),
                        "date": str(dato.date),
                        "hour": dato.hour
                    } for dato in sensor.dato_recolectado
                ]
            }
            datos.append(data_sensor)
        return datos

    def listSensorData(self):
        sensors = Sensor.query.all()
        sensor_data_list = []

        for sensor in sensors:
            for data in sensor.datos:
                sensor_data = {
                    "sensor_name": sensor.name,
                    "sensor_type": sensor.type_sensor.name if sensor.type_sensor else None,
                    "data": data.data,
                    "date": data.date.isoformat() if data.date else None,
                    "hour": data.hour.strftime("%H:%M:%S") if data.hour else None,
                }
                sensor_data_list.append(sensor_data)
    
        return sensor_data_list
    
    def listSensorDataByType(self, sensor_type_name):
    # Buscar sensores que coincidan con el tipo de sensor proporcionado
        sensors = Sensor.query.filter(Sensor.type_sensor.has(name=sensor_type_name)).all()
        sensor_data_list = []

        for sensor in sensors:
            for data in sensor.datos:
                sensor_data = {
                    "sensor_name": sensor.name,
                    "sensor_type": sensor.type_sensor.name if sensor.type_sensor else None,
                    "data": data.data,
                    "date": data.date.isoformat() if data.date else None,
                    "hour": data.hour.strftime("%H:%M:%S") if data.hour else None,
                }
                sensor_data_list.append(sensor_data)

        return sensor_data_list
