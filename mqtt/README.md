# MQTT subsystem

This folder contains a runner for the Mosquitto MQTT docker container.
All other systems will connect to this container. The container has a
network configured for host and so no port forwarding is done. The
containers MQTT server is accessed at the host devices IP and port 1883.

To start the container we can run `./mossie`
