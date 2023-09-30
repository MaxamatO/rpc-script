import json
import paho.mqtt.client as mqtt
from helpers.rpc_classes import RpcRequest, RpcResponse, _RequestData, _ResponseData
from helpers.commands import Commands

MQTT_TOPIC_ANOTHER = "udalo/sie/request"
MQTT_HOST = "IP"
MQTT_PORT = "PORT"
MQTT_TOPIC_BOX = "rpc/7a2d934f-a373-4b2f-83ab-6593ce5a4f6b/request"

response_functions = {
    MQTT_TOPIC_BOX: lambda json_payload, topic: handle_topic_box(json_payload, topic),
    MQTT_TOPIC_ANOTHER: lambda json_payload, topic: handle_another_topic_request(json_payload, topic)
}

def handle_create_topic(json_payload, topic: str):
    rpc_id: str = json_payload['id']
    cid_rid = rpc_id.split(":")
    cid = cid_rid[0]
    replaced_topic = topic.replace('/request', '/response')
    response_topic = f"{replaced_topic}/{cid}"
    return [response_topic, rpc_id]

def handle_topic_box(json_payload, topic):
    [response_topic, rpc_id] = handle_create_topic(json_payload=json_payload, topic=topic)
    response_data = _ResponseData(state=6, success=True, errorCode="320492").to_dict()
    rpc_response = RpcResponse(Commands.GetState, data=response_data)
    response = {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "result": json.dumps(rpc_response.__dict__)
    }
    return [response, response_topic]

def handle_another_topic_request(json_payload, topic):
    [response_topic, rpc_id] = handle_create_topic(json_payload=json_payload, topic=topic)
    response = {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "result": 6
    }

    return [response, response_topic]

def on_publish(client, userdata, mid):
    print("Przetworzone, wyslane response")

def on_message(client, userdata, message):
    json_payload = json.loads(message.payload)
    topic = json_payload['method'] + "/request"
    if topic in response_functions:
        [response, response_topic] = response_functions[topic](json_payload, topic)
        client_mqtt.publish(response_topic, json.dumps(response), qos=0)
    
client_mqtt = mqtt.Client()
client_mqtt.on_message = on_message
client_mqtt.on_publish = on_publish
client_mqtt.connect(MQTT_HOST, MQTT_PORT, 60)

client_mqtt.subscribe([(MQTT_TOPIC_BOX,2), (MQTT_TOPIC_ANOTHER, 2)])
client_mqtt.loop_forever()
