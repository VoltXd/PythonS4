import sys
import numpy as np

f=open('header.txt')  
f1=open('balade.kml','w')
for x in f.readlines():
    f1.write(x)
f.close()



try :   
    file = open('balade_gps.txt')
except : 
    sys.exit(-1)

latitude=[]
longitude=[]
altitude=[]


for line in file :
    if '$GPGGA' in line :
        line=line.strip()
        line = line.split(',')
        if line [6]=='1':
            latitude.append(float(line [2]))
            if line[3] == "S":
                longitude.append(-float(line [4]))
            else:
                longitude.append(float(line [4]))
            if line[5] == "W" :
                altitude.append(-float(line [9]))
            else:
                altitude.append(float(line [9]))    
    
file.close()

Latitude=np.array(latitude)
Longitude=np.array(longitude)
Altitude=np.array(altitude)

for i in range (len(altitude)):
    f1.write("\n             ")
    degL=int(Longitude[i]/100)
    minutesL=(Longitude[i]-degL*100)/60
    Longitude[i]=degL+minutesL
    f1.write(str(Longitude[i]))
    degLa=int(Latitude[i]/100)
    minutesLa=(Latitude[i]-degLa*100)/60
    Latitude[i]=degLa+minutesLa
    f1.write(",")
    f1.write(str(Latitude[i]))
    f1.write(",")
    f1.write(str(Altitude[i]))
f1.write("\n")
f2=open('footer.txt') 
for x in f2.readlines():
    f1.write(x)
f2.close()
f1.close()