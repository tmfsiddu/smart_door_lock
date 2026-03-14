import requests

ESP32_IP = "http://192.168.1.50/unlock"

def unlock_door():

    try:
        requests.get(ESP32_IP)
        return True
    except:
        return False