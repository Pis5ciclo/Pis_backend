schema_login = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["email", "password"],
}

schema_person = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "lastname": {"type": "string"},
        "phone": {"type": "string"},
        "identification": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["name", "lastname", "phone", "identification", "email", "password"],
}

schema_sensor = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'status': {'type': 'string'},
        'longitude': {'type': 'string'},
        'latitude': {'type': 'string'},
        "pi" : {'type':'string'},
        'type_sensor': {'type': 'string'}

    },
    'required': ['name', 'status', 'longitude', 'latitude', "pi", "type_sensor"]
}