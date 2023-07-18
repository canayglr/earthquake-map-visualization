import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv("database.csv")
print(data.columns) # CSV deki başlıkları yazdır
data=data[["Date","Time","Latitude","Longitude","Depth","Magnitude"]]
print(data.head())

import datetime,time
timeSet=[]
for d,t in zip(data["Date"], data["Time"]): # Gruplama yap
    try:
        ts=datetime.datetime.strptime(d+" "+t,"%m-%d-%Y %H:%M:%S") # zamanr formatını yeniden ayarlama 
        timeSet.append(time.mktime(ts.utctimetuple())) # verileri demet içerisine alma
        # time.mktime süreyi makine süresine çeviriyor
        
    except ValueError:
        timeSet.append("Hata") # tabloya ekleme işlemi

timeSet=pd.Series(timeSet) # tablo formatına çeviriyoruz
data["Timestamp"]=timeSet.values # yeni sütun oluşturup verileri içeri atıyoruz
final_data=data.drop(["Date","Time"], axis=1) # drop ile silme işlemi yapıyoruz
final_data=final_data[final_data.Timestamp!="Hata"]
print(final_data.head())

from mpl_toolkits.basemap import Basemap
m = Basemap(projection='mill',llcrnrlat=-80,urcrnrlat=80, llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

enlem = data["Longitude"].tolist()
boylam = data["Latitude"].tolist() # listeye çeviriyoruz

x,y = m(enlem,boylam) # ortalama değer
figur = plt.figure(figsize=(12,10))
plt.title("Deprem Haritası")
m.plot(x, y, "o", markersize = 2, color = 'blue')
m.drawcoastlines()
m.fillcontinents(color='coral',lake_color='aqua')
m.drawmapboundary()
m.drawcountries()
plt.show()