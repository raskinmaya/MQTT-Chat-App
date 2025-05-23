import os

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
CA_CERT = os.getenv("CA_CERT", "certs/ca.crt")
CLIENT_CERT = os.getenv("CLIENT_CERT", "certs/client.crt")
CLIENT_KEY = os.getenv("CLIENT_KEY", "certs/client.key")