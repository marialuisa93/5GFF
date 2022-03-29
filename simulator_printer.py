import paho.mqtt.client as mqtt
import json
import time

mqtt_host = "10.0.2.15"
mqtt_port = 1883
mqtt_topic_state = "{ver}/State"
mqtt_topic_status = "{ver}/Printers/{Id}/Status"
mqtt_topic_current = "{ver}/Printers/{Id}/Task/Current"
mqtt_keepalive_interval = 60

mqtt_msg_state = json.dumps({"Network": 0, "Count":{"Total": 10, "Working": 5, "Idle": 3, "Alarm": 2}})
mqtt_msg_status = json.dumps({"Status": 0})
mqtt_msg_current = json.dumps({"Id": "1234", "Name": "task1", "LayerIndex": 0, "TotalLayer": 0, "MaterialCanPrintLayers": 100, "Times":{"Begin": 1970, "Remaining" : "10:00:00"}})

def on_publish(client, userdata, mid):
	print("Published")

def on_connect(client, userdata, flags, rc):
	client.subscribe(mqtt_topic_state, 0)
	client.publish(mqtt_topic_state, mqtt_msg_state)
	client.subscribe(mqtt_topic_status)
	client.publish(mqtt_topic_status, mqtt_msg_status)
	client.subscribe(mqtt_topic_current)
	client.publish(mqtt_topic_current, mqtt_msg_current)

def on_message(client, userdata, msg):
	print(msg.topic)
	print(msg.payload)
	payload = json.loads(msg.payload)
	print(payload)


mqttc = mqtt.Client()
mqttc.loop_start()
while True:
	mqttc.on_publish = on_publish
	mqttc.on_connect = on_connect
	mqttc.on_message = on_message
	mqttc.connect(mqtt_host, mqtt_port, mqtt_keepalive_interval)
	time.sleep(10)

