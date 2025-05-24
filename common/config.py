import os

MQTT_BROKER: str = os.getenv("MQTT_BROKER", "0.0.0.0")
MQTT_PORT: int = int(os.getenv("MQTT_PORT", 1883))