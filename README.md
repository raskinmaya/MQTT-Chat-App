# MQTT Chat App

This is an MQTT-based chat application.
The goal behind this project was to build a messaging system using MQTT while following clean, scalable design practices.

---

## What's Done
- **Server and Client Architecture**: The project uses a Model-Service-Controller (MSC) architecture for better separation of concerns and maintainability. Both the server and client follow this pattern.
- **Message Handling**: Created types for server and client messages for better clarity and to avoid any confusion when parsing or handling data.
- **Schema Validation**: Implemented custom decorators to handle schema validation and message parsing.
- **Topic Handling Decorator**: Created a specialized decorator to simplify and streamline handling of MQTT topics, ensuring cleaner code and easier management of topic-specific actions.
- **MQTT Broker**: Used Mosquitto as the messaging broker to manage the publish-subscribe system.

---

## What's Missing
- 💔 The client is **non-functional** for now – there’s no graphical interface (ran out of time for this part).
- Missing response handling on the client side as well (needs a GUI to interact with).

---

While there’s still a lot left to do, the structure is in place to make it happen.
