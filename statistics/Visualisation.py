"------Visualisation des donées récupérées des Raspberrypi------"

import pandas as pd
import seaborn as sns
# On commence par importer la librairie maptplotlib
import matplotlib.pyplot as plt

black_friday = pd.read_csv("data(inside).csv", sep=',', encoding='latin-1')
#black_friday.info()
print(black_friday.to_string())

distance =["30m(Inside)", "200m(Outside)", "270m(Outside)"]
data = ["data(inside).csv", "data(outside)1.csv", "data(outside)2.csv"]
#distance =["200m(Outside)"]
#data = ["data(outside)2.csv"]
ratio = []
recu =0
paquet=0
perdu=0

for i in range(0,3):
    dataframe = pd.read_csv(data[i], sep=',', encoding='latin-1')
    x = distance[i]
    energie = dataframe['Energie'].tolist() # converting column data to list
    for element in energie:
        if element != " N/A":
            recu+=1
            paquet+=1
        else:
            perdu+=1
            paquet+=1
    pourc_rec = recu/paquet
    print("Le ratio est : ",pourc_rec)
    ratio.append(pourc_rec)

print(ratio)

#Création de l'Histogramme

df = pd.DataFrame(list(zip(ratio, distance)), columns =['Ratio', 'Distance'])
print(df)

plt.figure(figsize=(5,6))
sns.barplot(x=df['Distance'], y=df['Ratio'], palette="Reds_r")
plt.xlabel('\nDistance Sender-Receiver', fontsize=15, color='#c0392b')
plt.ylabel("Ratio Received packets/Sent packets\n", fontsize=15, color='#c0392b')
plt.title("Histogram showing the number of packets received and lost\n", fontsize=18, color='#e74c3c')
plt.xticks(rotation= 45)
plt.tight_layout()
plt.show()