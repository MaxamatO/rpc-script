import json
import paho.mqtt.client as mqtt
# Topic na ktory bedziemy wysylac nasze wiadomosci. Musza byc spojne na backendzie i tutaj.
MQTT_TOPIC = "udalo/sie"
MQTT_HOST = "example.com"
MQTT_PORT = "Use 1883 for MQTT TCP/IP"

# Ta funkcja wywolac sie powinna, gdy on_message sie wykona prawidlowo
def on_publish(client, userdata, mid):
    print("Przetworzone, wyslane response")

# on_message ma za zadanie robic to, 
# co powinna funkcja rpc.register (w ogromnym uproszczeniu)
# z libki mqtt-json-rpc
def on_message(client, userdata, message):

    # Konwertujemy JSON na obiekt
    json_payload = json.loads(message.payload)
    method = json_payload['method']

    # Wyciagamy potrzebne informacje, zeby wyslac response na poprawny topic
    rpc_id: str = json_payload['id']
    rid_cid = rpc_id.split(":")
    cid = rid_cid[0]

    # Tworzymy response topic 
    response_topic = f"{method}/response/{cid}"

    # Tak wyglada przyjmowany JSON przez nasze mqtt-json-rpc
    response = {
        "jsonrpc": "2.0",
        "id": rpc_id,
        # Nasz result to response, który zostaje zwrócony przez rpc.call
        "result": 6
    }

    # Wysylamy wiadomosc na odpowiedni topic, z obiektem na JSON.
    client_mqtt.publish(response_topic, json.dumps(response), qos=0)
    
# Jakies ustawienia, zeby sie polaczyc z serwerem
client_mqtt = mqtt.Client()
client_mqtt.on_message = on_message
client_mqtt.on_publish = on_publish
client_mqtt.connect(MQTT_HOST, MQTT_PORT, 60)

# Subscribe, czyli oczekiwanie na topic o takiej postaci. Ta dwojka to qos=2
client_mqtt.subscribe(f"{MQTT_TOPIC}/request", 2)
client_mqtt.loop_forever()
