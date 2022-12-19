import datetime
import json
import subprocess
import re
import paho.mqtt.client as mqtt
import pyodbc
import numpy as np

server = 'server.perivolaris.be'
database = 'IOT'
username = 'isib'
password = 'irisib'
driver = '{ODBC Driver 18 for SQL Server}'

def getHumidity(temperature, resistor):
    # missing value have been estimated with excel
    table = [
        [0  ,   0,       5,      10,     15,     20,     25,     30,     35,     40,     45,     50],
        [20,    90000,  60000,  35000,  21000,  13500,  9800,   8000,   6300,   4600,   3800,   3200],
        [25,    25000,  19800,  16000,  10500,  6700,   4803,   3900,   3100,   2300,   1850,   1550],
        [30,    12000,  9800,   7200,   5100,   3300,   2500,   2000,   1500,   1100,   900,    750],
        [35,    5200,   4700,   3200,   2350,   1800,   1300,   980,    750,    575,    430,    350],
        [40,    2800,   2000,   1400,   1050,   840,    630,    470,    385,    282,    210,    170],
        [45,    720,    510,    386,    287,    216,    166,    131,    104,    80,     66,     51],
        [50,    384,    271,    211,    159,    123,    95,     77,     63,     52,     45,     38],
        [55,    200,    149,    118,    91,     70,     55,     44,     38,     32,     30,     24],
        [60,    108,    82,     64,     51,     40,     31,     25,     21,     17,     14,     12],
        [65,    64,     48,     38,     31,     25,     20,     17,     13,     11,     9,      8],
        [70,    38,     29,     24,     19,     16,     13,     10.5,   9,      8.2,    7.1,    6.0],
        [75,    23,     18,     15,     12,     10,     8.5,    7.2,    6.4,    5.8,    5.0,    4.1],
        [80,    16,     12,     10.2,   8.1,    7.2,    5.7,    5.0,    4.4,    4.0,    3.3,    2.9],
        [85,    10.2,   8.2,    6.9,    5.5,    4.7,    4.0,    3.6,    3.2,    2.9,    2.4,    2.0],
        [90,    6.9,    5.4,    4.7,    4.1,    3.2,    2.8,    2.5,    2.3,    2.1,    1.8,    1.5],
    ]

    table = np.array(table, np.double)

    def findColumns(temperature):
        tempTab = np.abs(table[0,:]-temperature)
        bestFit = tempTab.argmin()
        return table[:, bestFit:bestFit+2]

    def interpolate(tab, temp):
        ratioTemp = (temp - tab[0,0])/(tab[0,1] - tab[0,0])
        return tab[:, 0]-(tab[:, 0]-tab[:, 1])*ratioTemp


    def interpolateRh(tab, resistance):
        row = np.abs(tab - resistance).argmin()
        ratioRes = (resistance - tab[row])/(tab[row-1]-tab[row])
        return table[row, 0]-(table[row, 0]-table[row-1, 0])*ratioRes


    tab = (findColumns(22))
    resistancesTab = interpolate(tab, temperature)
    return int(interpolateRh(resistancesTab, resistor))
    
def log(txt):
    log = open("./log", "a")
    log.write("[" + str(datetime.datetime.now()) +"]"+ txt + "\n")
    print("[" + str(datetime.datetime.now()) +"]"+ txt)
    log.close()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("v3/isib-syn@ttn/devices/+/up")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global lastMesuredTemp  
    try:
        decodedPayload = json.loads(msg.payload)["uplink_message"]["decoded_payload"]
        sensor = str(decodedPayload["sensor"])
        light = str(decodedPayload["light"])
        temperature = decodedPayload["temperature"]
        vibration = str(decodedPayload["vibration"])
        humidity = str(getHumidity(temperature, int(decodedPayload["humidity"])))
        temperature = str(temperature)
    except:
        log("Format error")
        return
# Send to DB
    insertStmt = "INSERT  into Data (humidity, temperature, vibration, light, date, device) values (" + humidity + ", " + temperature + ", " + vibration + ", " + light + ",'" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +"', " + sensor + ")"
    with pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=1433;' + 'TrustServerCertificate=yes;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) as conn:
        with conn.cursor() as cursor:
            response = cursor.execute(insertStmt)
    if len(response.messages) > 0:
        log("DB errors : " + '\n'.join(response.messages))
    else:
        log("Inserted : humidity["+ humidity + "], light[" + light + "], temperature[" + temperature + "], vibration[" + vibration + "]")

def on_subscribe(client, qos=0, options=None, properties=None):
    print(client, qos, options, properties)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.username_pw_set("isib-syn",
                       "NNSXS.RHV2H4L42Z7EGNHOY6GNLLESIQOZIGKDFJUFGGQ.POV4PRL2XKVUQPN6MEVU7L67AQLHTJROVEQBAKYFE2I63WVDN7UQ")
client.connect("eu1.cloud.thethings.network", 1883, 60)

client.loop_forever()
