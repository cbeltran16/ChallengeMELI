import json
import os
import pytest
from email_manager import send_email, load_smtp_config

def test_load_smtp_config():
    # Crear un archivo de configuración SMTP de prueba
    smtp_config = {
        "host": "smtp.gmail.com",
        "port": 465,
        "username": "SGVsbG8gV29ybGQh",
        "password": "SGVsbG8gV29ybGQh"
    }
    with open('test_email_config.json', 'w') as f:
        json.dump(smtp_config, f)

    # Cargar la configuración SMTP
    loaded_config = load_smtp_config('test_email_config.json')

    # Verificar que la configuración cargada sea correcta
    assert loaded_config == smtp_config

    # Eliminar el archivo de configuración de prueba
    os.remove('test_email_config.json')

