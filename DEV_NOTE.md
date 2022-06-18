
systemctl status mosquitto

mosquitto_sub -h 127.0.0.1 -t topic
mosquitto_pub -h 127.0.0.1 -t topic -m "Hello"