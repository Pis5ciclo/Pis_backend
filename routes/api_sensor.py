from controllers.authenticateController import token_requeird
from utils.utilities.schemas import schema_sensor
from flask import Blueprint, jsonify, jsonify, make_response, request
from controllers.sensor.sensorController import SensorController
from controllers.sensor.sensordataController import SensorDataController
from utils.utilities.errors import Errors
from utils.utilities.success import Success
from utils.utilities.response_http import make_response_error, make_response_ok

api_sensor = Blueprint("api_sensor", __name__)
sensorController = SensorController()
sensorDataController = SensorDataController()
@api_sensor.route("/list_sensor", methods=["GET"])
# @token_requeird
def listSensor():
        return make_response_ok(sensorController.listSensor())

@api_sensor.route("/sensor/save", methods=["POST"])
# @token_requeird
def createSensor():
    data = request.json
    result = sensorController.save_sensor(data)
    
    if result == -23:
        return make_response(jsonify({"error": "La IP ya está registrada"}), 400)
    elif result == -10:
        return make_response_error(Errors.error["-10"], 400)
    elif result == -21:
        return make_response_error(Errors.error["-21"], 400)
    elif result == 2:
        return make_response_ok({"success": Success.success["2"]})
    elif result == -9:
        return make_response_error(Errors.error["-9"], 400)   

@api_sensor.route('/modify_sensor/<external_id>', methods=['POST'])
def modify_sensor(external_id):
    data = request.json
    result = sensorController.modify_sensor(external_id, data)
    if result == -23:
        return make_response(jsonify({"error": "La IP ya está registrada"}), 400)
    elif  result == -10:
        return make_response_error(Errors.error["-10"], 400)
    if result == -21:
        return make_response_error(Errors.error["-21"], 400)
    elif result == -9:
        return make_response_error(Errors.error["-9"], 400)
    else:
        return make_response_ok({"success": Success.success["4"]})   
    
@api_sensor.route("/sensor/status/<external_id>", methods=["GET"])
def desactivateSensor(external_id):
    result = sensorController.deactivate_sensor(external_id)
    if result == 5:
        return make_response_ok({"success": Success.success["5"]})
    elif result == -20:
        return make_response_error(Errors.error["-20"], 404)
    
@api_sensor.route('/api/simulacion/<id>', methods=['GET'])
def api_get_sensor_data(id):
    data, status_code = sensorDataController.get_sensor_data(id)
    return jsonify(data), status_code

@api_sensor.route('/api/simulacion/date/<id>', methods=['GET'])
def search_sensor_date(id):
    return sensorDataController.search_data_date(id)

@api_sensor.route('/api/simulacion/interpolate/<id>', methods=['GET'])
def api_get_sensor_data_interpolate(id):
    data, status_code = sensorDataController.get_interpolated_sensor_data(id)
    return jsonify(data), status_code

@api_sensor.route('/api/sensor_interpolacion/<int:sensor_id>/<fecha_inicio>/<fecha_fin>', methods=['GET'])
def api_sensor_interpolacion(sensor_id, fecha_inicio, fecha_fin):
    try:
        resultados_interpolados = sensorDataController.interpolacion_sensor(sensor_id, fecha_inicio, fecha_fin)
        return jsonify(resultados_interpolados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api_sensor.route('/data_sensor', methods=['POST'])
def data_sensor():
    data = request.get_json()
    return sensorController.guardar_datos_sensor(data)

@api_sensor.route('/data_sensor_aire', methods=['POST'])
def data_sensor_agua():
    data = request.get_json()
    return sensorController.guardar_datos_sensor_aire(data)

@api_sensor.route('/data/sensor', methods = ["GET"])
def listSensorData():
    return make_response_ok(sensorDataController.listSensorData())


@api_sensor.route("/sensor/list_sensor_name", methods=["GET"])
# @token_requeird
def listNameSensor():
        return make_response_ok(sensorController.listSensorName())
    
@api_sensor.route('/data/latest_air1', methods=['GET'])
def api_get_data_latest():
    data, status_code = sensorDataController.get_data_latest_air1()
    return jsonify(data), status_code

@api_sensor.route('/data/latest_air1/average', methods=['GET'])
def api_get_data_average():
    data, status_code = sensorDataController.get_sensor_data_average()
    return jsonify(data), status_code

@api_sensor.route('/types', methods=['GET'])
def all_type():
    data, status_code = sensorController.all_types()
    return jsonify(data), status_code