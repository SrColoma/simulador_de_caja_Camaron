import requests
import json
import random
import time

# Endpoint para enviar la estructura
url_addValores = "https://daserldsli.execute-api.us-west-1.amazonaws.com/camaronAddValores"
url_getBoxConfig = "https://daserldsli.execute-api.us-west-1.amazonaws.com/camaronGetBoxConfig"

# Acceder a los valores del JSON
frecuencia = 120

# Valores iniciales de la estructura
values = {
  "OXDIX" : "8",
  "TEMP": "24.5",
  "SAL" : "0.3",
  "PH": "7.5",
  "TURBIDEZ": "1",
  "TDS": "1050",
  "LLUVIA": "0",
  "NIVEL": "1"
}

headers = {
    'Content-Type': 'application/json'
}

def cambiar_configuracion():
    global frecuencia
    resp = requests.get(url_getBoxConfig)

    # Obtener el JSON de la respuesta
    json_data = resp.json()

    # Acceder a los valores del JSON
    frecuencia = json_data['body']['frecuencia']

def enviar_datos():
    values["OXDIX"] = str(round(float(values["OXDIX"]) + random.uniform(-0.1, 0.1), 1))
    values["TEMP"] = str(round(float(values["TEMP"]) + random.uniform(-0.1, 0.1), 1))
    values["SAL"] = '0.0'
    values["PH"] = str(round(float(values["PH"]) + random.uniform(-0.1, 0.1), 1))
    values["TURBIDEZ"] = str(round(float(values["TURBIDEZ"]) + random.uniform(-0.1, 0.1), 1))
    values["TDS"] = str(round(float(values["TDS"]) + random.uniform(-100, 100), 1))
    values["LLUVIA"] = '0'
    values["NIVEL"] = '1'

    # Envía la estructura actualizada al endpoint
    try:
        response = requests.post(url_addValores, data=json.dumps(values), headers=headers)
    except requests.exceptions.RequestException as e:
        print("Error al enviar los datos:", e)

    # Verifica la respuesta del endpoint
    if response:
        print("Datos enviados correctamente:", values)
    else:
        print("Error al enviar los datos:", response.text)




# Iniciar un bucle infinito
while True:
    cambiar_configuracion()
    
    time.sleep(2 * 60)
    
    tiempo_inicio = time.time()
    
    while True:
        enviar_datos()
        
        time.sleep(frecuencia)
        
        if time.time() - tiempo_inicio > 2 * 60:
            break
