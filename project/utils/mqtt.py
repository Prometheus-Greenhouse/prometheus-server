from typing import Dict

import orjson
import paho.mqtt.client


def to_dict(data: bytes, force: bool = True) -> Dict:
    print(data[5:])
    try:
        return orjson.loads(data[5:])
    except orjson.JSONDecodeError:
        if force:
            return {"data": data[5:].decode("utf8")}


def to_str(data: bytes) -> str:
    return data[5:].decode("utf8")


def content_type(data) -> str:
    if isinstance(data, dict):
        return "json"
    if isinstance(data, str):
        return "text"
    if isinstance(data, (bytes, bytearray)):
        return "byte"
    if isinstance(data, (int, float)):
        return "numb"
    if data is None:
        return "null"


class Client(paho.mqtt.client.Client):
    def publish(self, topic, payload=None, qos=0, retain=False, properties=None):
        type_ = f"{content_type(payload)}:".encode("utf8")
        if type_ == b"json:":
            payload = type_ + orjson.dumps(payload)
        elif type_ == b"text:":
            payload = type_ + payload.encode("utf8")
        elif type_ == b"byte:":
            payload = type_ + payload
        elif type_ == b"numb:":
            payload = type_ + str(payload).encode("ascii")
        elif type == b"null:":
            payload = type_
        return super().publish(topic, payload, qos, retain, properties)
