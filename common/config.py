import os

MQTT_BROKER: str = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT: int = int(os.getenv("MQTT_PORT", 1883))
CA_CERT: str = os.getenv("CA_CERT", "certs/ca.crt")
CLIENT_CERT: str = os.getenv("CLIENT_CERT", "certs/client.crt")
CLIENT_KEY: str = os.getenv("CLIENT_KEY", "certs/client.key")