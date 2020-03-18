# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 19:23:36 2020

@author: Andre
"""

import sys
import numpy as np

def degreeMinuteToDecimalDegree(DMvalue):
    degree = int(DMvalue/100)
    minute = DMvalue - degree * 100
    decimalDegree = degree + minute / 60
    if decimalDegree > 180.0:
        decimalDegree -= 360.0
    else:
        if decimalDegree < -180.0:
            decimalDegree += 360.0
    return decimalDegree

def getCoordinatesWithSpeed(longitude, latitude, altitude, velocity):
    body = ''
    length = len(longitude)
    maxSpeed = max(velocity)
    for i in range(1, length):
        #Compute the RGB color from HSV's Hue. Hue is proportional with the speed
        H = 240.0 - velocity[i] * 240.0 / maxSpeed
        S = 255.0
        V = 255.0
        
        Hi = int((H / 60.0) % 6)
        F = H/60.0 - Hi
        l = V  * (1.0 - S/255)
        m = V * (1.0 - F * S/255)
        n = V * (1.0 - (1.0 - F) * S/255)
        
        R = 0
        G = 0
        B = 0
        
        if Hi == 0:
            R = V
            G = n
            B = l
        if Hi == 1:
            R = m
            G = V
            B = l
        if Hi == 2:
            R = l
            G = V
            B = n
        if Hi == 3:
            R = l
            G = m
            B = V
        if Hi == 4:
            R = n
            G = l
            B = V
        if Hi == 5:
            R = V
            G = l
            B = m
            
        #Fill the body, one line is made of only two points
        colorString = '7f' + '{:02x}'.format(int(R)) + '{:02x}'.format(int(G)) + '{:02x}'.format(int(B))
        body += '\t\t<Placemark>\n'
        body += '\t\t\t<Style>\n'
        body += '\t\t\t\t<LineStyle>\n'
        body += '\t\t\t\t\t<color>' + colorString +'</color>\n'
        body += '\t\t\t\t\t<width>8</width>\n'
        body += '\t\t\t\t</LineStyle>\n'
        body += '\t\t\t</Style>\n'
        body += '\t\t\t<LineString>\n'
        body += '\t\t\t\t<extrude>1</extrude>\n'
        body += '\t\t\t\t<tessellate>1</tessellate>\n'
        body += '\t\t\t\t<altitudeMode>absolute</altitudeMode>\n'
        body += '\t\t\t\t<coordinates>\n'
        body += '\t\t\t\t\t' + str(longitude[i-1]) + ',' + str(latitude[i-1]) + ',' + str(altitude[i-1]) + '\n'
        body += '\t\t\t\t\t' + str(longitude[i]) + ',' + str(latitude[i]) + ',' + str(altitude[i]) + '\n'
        body += '\t\t\t\t</coordinates>\n'
        body += '\t\t\t</LineString>\n'
        body += '\t\t</Placemark>\n'
    return body



if __name__ == '__main__':
    try:
        f = open('balade_gps.txt', 'r')
    except FileNotFoundError:
        print('File not found')
        sys.exit(-1)
    
    try:
        fw = open('balade.kml', 'w')
    except FileNotFoundError:
        print('Unable to find file or folder')
        sys.exit(-1)
    except PermissionError:
        print('Permission denied')
        sys.exit(-1)
        
    try:
        fH = open('head.txt', 'r')
    except FileNotFoundError:
        print('File not found')
        sys.exit(-1)
        
    try:
        fF = open('foot.txt', 'r')
    except FileNotFoundError:
        print('File not found')
        sys.exit(-1)
        
        
    #Put the header first
    fw.write(fH.read() + '\n')
    
    earthRadius = 6371000 #in meter
    
    longitude = []
    latitude = []
    altitude = []
    x = []
    y = []
    z = []
    t = []
    v = []
    
    #Analyze the frames (GPGGA only)
    for line in f:
        if '$GPGGA' not in line:
            continue
        line = line.strip()
        liste = line.split(',')
        if liste[6] == '0':
            continue
        
        #Get spheric coordinates 
        sideFactor = 1
        if liste[5] == 'W':
            sideFactor = -1
        try:
            longitude.append(sideFactor * degreeMinuteToDecimalDegree(float(liste[4])))
        except ValueError:
            longitude.append(float('nan'))
        
        sideFactor = 1
        if liste[3] == 'S':
            sideFactor = -1
        try:
            latitude.append(sideFactor * degreeMinuteToDecimalDegree(float(liste[2])))
        except ValueError:
            latitude.append(float('nan'))
        
        try:
            altitude.append(float(liste[9]))
        except ValueError:
            altitude.append(float('nan'))
        
        #Calculate current frame time
        currentTime = float(liste[1])
        currentHour = int(currentTime / 10000)
        currentMinute = int((currentTime - currentHour*10000) / 100)
        currentSecond = currentTime - currentMinute*100 - currentHour*10000
        currentTime = currentHour * 3600 + currentMinute * 60 + currentSecond
        
        #Compute the cartesian coordinates
        x.append((earthRadius + altitude[-1]) * np.cos(longitude[-1] * np.pi / 180) * np.cos(latitude[-1] * np.pi / 180))
        y.append((earthRadius + altitude[-1]) * np.cos(longitude[-1] * np.pi / 180) * np.sin(latitude[-1] * np.pi / 180))
        z.append((earthRadius + altitude[-1]) * np.sin(longitude[-1] * np.pi / 180))
        t.append(currentTime)
        
        #Compute the current speed
        if len(x) < 2:
            v.append(0)
            continue
        v.append(np.sqrt((x[-1] - x[-2])**2 + (y[-1] - y[-2])**2 + (z[-1] - z[-2])**2) / (t[-1] - t[-2]))
    
    #Write the coordinates and add color according to current speed, also write the foot
    fw.write(getCoordinatesWithSpeed(longitude, latitude, altitude, v))
    fw.write(fF.read())
        
    f.close()
    fw.close()
    fH.close()
    fF.close()