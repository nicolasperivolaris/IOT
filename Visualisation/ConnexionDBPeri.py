import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pypyodbc as odbc

config = (
    "DRIVER={SQL Server Native Client 11.0};"
    "SERVER=server.perivolaris.be;"
    "DATABASE=IOT;"
    "UID=isib;"
    "PWD=irisib;"
    "MARS_Connection=Yes"
)

# Create a connection to the database
connexion = odbc.connect(config)

plt.style.use('fivethirtyeight')

def animate(i):
    # Execute a query to get the new data from the database
    data = pd.read_sql("SELECT * FROM Temperature WHERE date >= '2022-12-13 16:40:00' ", connexion)
    data2 = pd.read_sql("SELECT * FROM Vibration WHERE date >= '2022-12-13 16:40:00'", connexion)
    data3 = pd.read_sql("SELECT * FROM Humidity WHERE date >= '2022-12-13 16:40:00'", connexion)
    data4 = pd.read_sql("SELECT * FROM Light WHERE date >= '2022-12-13 16:40:00'", connexion)
    finalist = []
    finalist2 =[]
    finalist3 =[]
    finalist4 =[]

    list_frame = [data,data2,data3,data4]
    list_finalist = [finalist,finalist2,finalist3,finalist4]
    i = 0
    for frame in list_frame:
        for temp in frame['date']:
            temp = "{}".format(temp)
            month = temp[5:7]
            day = temp[8:10]
            hour = temp[11:16]
            moment = day+'/'+month+' '+hour
            list_finalist[i].append(moment)
        i +=1

    x = finalist
    x2 = finalist2
    x3 = finalist3
    x4 = finalist4
    y1 = data['valeur']
    y2 = data2['valeur']
    y3 = data3['valeur']
    y4 = data4['valeur']

    #Visualisation de la Température
    plt.cla()
    plt.subplot(2, 2, 1)
    plt.plot(x, y1)
    #plt.legend(loc='upper left')
    plt.title('Temperature Variation',fontname="Times New Roman",size=30,fontweight="bold",color='darkblue')
    plt.xlabel('Time',color='darkblue', size=15)
    plt.ylabel('Temperature[°C]',color='darkblue', size=15)
    plt.xticks(finalist, rotation= 90, size=9)

    #Visualisation de la vibration
    plt.subplot(2, 2, 2)
    plt.plot(x2, y2)
    #plt.legend(loc='upper left')
    plt.title('Vibration Variation',fontname="Times New Roman",size=30,fontweight="bold",color='darkblue')
    plt.xlabel('Time',color='darkblue', size=15)
    plt.ylabel('Vibration[Hz]',color='darkblue', size=15)
    plt.xticks(finalist2, rotation= 90, size=9)

    #Visualisation de l'humidité
    plt.subplot(2, 2, 3)
    plt.plot(x3, y3)
    #plt.legend(loc='upper left')
    plt.title('Humidity Variation',fontname="Times New Roman",size=30,fontweight="bold",color='darkblue')
    plt.xlabel('Time',color='darkblue', size=15)
    plt.ylabel('Humidity[g/m³]',color='darkblue', size=15)
    plt.xticks(finalist3, rotation= 90, size=9)

    #Visualisation de la lumière
    plt.subplot(2, 2, 4)
    plt.plot(x4, y4)
    #plt.legend(loc='upper left')
    plt.title('Light Variation',fontname="Times New Roman",size=30,fontweight="bold",color='darkblue')
    plt.xlabel('Time',color='darkblue', size=15)
    plt.ylabel('Light[lux]',color='darkblue', size=15)
    plt.xticks(finalist4, rotation= 90, size=9)
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.tight_layout()
plt.show()