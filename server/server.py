import datetime
import json
import subprocess
import re
import paho.mqtt.client as mqtt
import pyodbc

server = 'server.perivolaris.be'
database = 'IOT'
username = 'isib'
password = 'irisib'
driver = '{ODBC Driver 17 for SQL Server}'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("v3/isib-syn@ttn/devices/+/up")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    decodedPayload = json.loads(msg.payload)["uplink_message"]["decoded_payload"]
    payload = decodedPayload["str"]  # downlink_queued
    print(msg.topic + " " + str(payload))
    letter = payload[0].lower()
    match letter:
        case "t": type = "temperature"
        case "v": type = "vibration"
        case "h": type = "humidity"
        case "l": type = "light"
        case _:
            return
    insert = "INSERT  into " + type + " (valeur, date) values (" + payload[1:] + ",'" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +"')"
    with pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) as conn:
        with conn.cursor() as cursor:
            response = cursor.execute(insert)
        print(response)

def on_subscribe(client, qos=0, options=None, properties=None):
    print(client, qos, options, properties)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.username_pw_set("isib-syn",
                       "NNSXS.RHV2H4L42Z7EGNHOY6GNLLESIQOZIGKDFJUFGGQ.POV4PRL2XKVUQPN6MEVU7L67AQLHTJROVEQBAKYFE2I63WVDN7UQ")
client.connect("eu1.cloud.thethings.network", 1883, 60)

with pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT date from Temperature")

client.loop_forever()
