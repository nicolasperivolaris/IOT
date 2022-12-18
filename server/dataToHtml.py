import datetime
from matplotlib import dates
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
import re

with open("./log", "r") as f:
    dataStrings = f.readlines()

dataList = []

typeRegex = re.compile(r"(\w+)\[")
dataRegex = re.compile(r"\[(-?\d+)\]")
types = typeRegex.findall(dataStrings[0])
dateFormat = "%Y-%m-%d %H:%M:%S.%f"
dateRegex = re.compile(r"\[(.+?)\]")

for dataString in dataStrings:
    data = dataRegex.findall(dataString)
    date = dateRegex.findall(dataString)[0]

    dataDict = {}
    for i in range(len(types)):
        dataDict[types[i]] = pd.to_numeric(data[i])

    dataDict["date"] = date
    dataList.append(dataDict)

df = pd.DataFrame(dataList)
df['date'] = pd.to_datetime(df['date'])
for type in types:
    df[type] = df[type].rolling(30).mean() #rolling mean to smooth every thing

df.plot(x="date")

plt.gca().xaxis.set_major_locator(dates.DayLocator())
plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%d\n\n%a'))
figure = plt.gcf()
figure.set_size_inches(15, 8)
mpld3.save_html(fig=figure,  fileobj="./index.html")