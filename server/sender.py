import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes 

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    client.publish("isib-syn@ttn", payload="co")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_publish(client, userdata, mid):
    print(client, userdata, mid)

properties = Properties(PacketTypes.CONNECT)
properties.MaximumPacketSize=20

client = mqtt.Client("isib-syn", protocol=4)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.username_pw_set("isib-syn@ttn", "NNSXS.RHV2H4L42Z7EGNHOY6GNLLESIQOZIGKDFJUFGGQ.POV4PRL2XKVUQPN6MEVU7L67AQLHTJROVEQBAKYFE2I63WVDN7UQ")
client.connect("eu1.cloud.thethings.network", 1883, 60)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()