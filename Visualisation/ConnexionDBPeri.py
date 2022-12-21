import pandas as pd
import matplotlib.pyplot as plt
import pypyodbc as odbc
from matplotlib import dates
import mpld3
import http.server
import time

lastTime = time.time()


class MyRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if not self.path in ["/", "/1", "/2"] : return
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        global lastTime
        if time.time() - lastTime > 30:
            makeIndex()
            lastTime = time.time()
        if self.path == "/":
            with open("./Show.html", "r") as f:
                self.wfile.write(f.read().encode())
        elif self.path == "/1":
            with open("./device1.html", "r") as f:
                self.wfile.write(f.read().encode())
        elif self.path == "/2":
            with open("./device2.html", "r") as f:
                self.wfile.write(f.read().encode())



def makeIndex():
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

    data = pd.read_sql("SELECT * FROM Data WHERE date >= '2022-12-18 13:00:00' AND device = 1", connexion)
    data2 = pd.read_sql("SELECT * FROM Data WHERE date >= '2022-12-18 13:00:00' AND device = 0", connexion)
    print(data) 

    def ma_fonction(x):
        if x > 0:
            return 1
        else:
            return x
    

    frames = [data,data2]
    for frame in frames:
        for type in ["light", "temperature", "humidity"]:
            frame[type] = frame[type].rolling(30).mean()  # rolling mean to smooth every thing
        frame['vibration'] = frame['vibration'].apply(ma_fonction)
    
    data['date'] = pd.to_datetime(data['date'])
    data = data.drop(columns=['id','device'])
    print(data)

    # Create a figure with 2 rows and 2 columns of subplots
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(data['date'], data['vibration'])
    axs[0, 0].set_title("Vibration Variation")
    axs[0, 0].set_ylabel("Vibration")
    axs[0, 0].set_xlabel("Time")
    axs[0, 1].plot(data['date'], data['temperature'])
    axs[0, 1].set_title("Temperature Variation")
    axs[0, 1].set_ylabel("Temperature [°C]")
    axs[0, 1].set_xlabel("Time")
    axs[1, 0].plot(data['date'], data['humidity'])
    axs[1, 0].set_title("Humidity Variation")
    axs[1, 0].set_ylabel("Humidity")
    axs[1, 0].set_xlabel("Time")
    axs[1, 1].plot(data['date'], data['light'])
    axs[1, 1].set_title("Light Variation")
    axs[1, 1].set_ylabel("Light")
    axs[1, 1].set_xlabel("Time")


    # Set the x-axis labels for all subplots
    for ax in axs.flat:
        ax.xaxis.set_major_locator(dates.DayLocator())
        ax.xaxis.set_major_formatter(dates.DateFormatter('%d\n\n%a'))

    fig.set_size_inches(10, 5)
    mpld3.save_html(fig=fig,  fileobj="./device1.html")
    #mpld3.show(fig)


    fig2, axs2 = plt.subplots(2, 2)

    axs2[0, 0].plot(data2['date'], data2['vibration'])
    axs2[0, 0].set_title("Vibration Variation")
    axs2[0, 0].set_ylabel("Vibration")
    axs2[0, 0].set_xlabel("Time")
    axs2[0, 1].plot(data2['date'], data2['temperature'])
    axs2[0, 1].set_title("Temperature Variation")
    axs2[0, 1].set_ylabel("Temperature [°C]")
    axs2[0, 1].set_xlabel("Time")
    axs2[1, 0].plot(data2['date'], data2['humidity'])
    axs2[1, 0].set_title("Humidity Variation")
    axs2[1, 0].set_ylabel("Humidity")
    axs2[1, 0].set_xlabel("Time")
    axs2[1, 1].plot(data2['date'], data2['light'])
    axs2[1, 1].set_title("Light Variation")
    axs2[1, 1].set_ylabel("Light")
    axs2[1, 1].set_xlabel("Time")

    # Set the x-axis labels for all subplots
    for ax in axs2.flat:
        ax.xaxis.set_major_locator(dates.DayLocator())
        ax.xaxis.set_major_formatter(dates.DateFormatter('%d\n\n%a'))

    fig2.set_size_inches(10, 5)
    mpld3.save_html(fig=fig2,  fileobj="./device2.html")
    #mpld3.show(fig2)

server = http.server.HTTPServer(("0.0.0.0", 80), MyRequestHandler)
server.serve_forever()