# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 17:17:34 2020

@author: Andre
"""

import sys
import Ex2 
import numpy as np

def repetitions(s, le=3):
    repetitionDictionary = {}
    keyList = []
    stringLength = len(s)
    
    #Creates a dictionary of every repetition and get their index
    for i in range(stringLength - le+1):
        stringSlice = s[i:i+le]
        if stringSlice in repetitionDictionary:
            continue
        
        repetitionsIndex = []
        j = s.find(stringSlice, i+le)
        
        if j != -1:
            repetitionsIndex.append(i)
            keyList.append(stringSlice)
        while j != -1:            
            repetitionsIndex.append(j)
            j = s.find(stringSlice, j+le)
            if j == -1:
                repetitionDictionary[stringSlice] = repetitionsIndex
                
    return repetitionDictionary, keyList
    
#Create a dictionary of the "PGCD" to know which one is the most frequent
def sortByPGCD(pgcdList):
    pgcdDictionary = {}
    for pgcd in pgcdList:
        if pgcd in pgcdDictionary:
            pgcdDictionary[pgcd] += 1
            continue
        else:
            pgcdDictionary[pgcd] = 1
    return pgcdDictionary
    
    
    
    
    
    
if __name__ == '__main__':
    filename = 'question3.enc'
    try:
        f = open(filename, 'rb')
    except FileNotFoundError:
        sys.exit(-1)
        
    text = f.read()
    dictionary, keys = repetitions(text)
    pgcd = []
    
    #Calculate the gap between redundant words. Then calculate the "PGCD" of these gaps to know the length of the key.
    for key in keys:
        gap = []
        for i in range(1, len(dictionary[key])):
            gap.append(dictionary[key][i] - dictionary[key][i-1])
        tempPGCD = np.gcd.reduce(gap)
        if tempPGCD != 1:
            pgcd.append(tempPGCD)
    sortedPgcd = sortByPGCD(pgcd)
    key3Length = max(sortedPgcd, key=sortedPgcd.get)

    #Now it's done, it's just as the last exercice.    
    hyst3List = []
    for i in range(key3Length):
        hyst3List.append(Ex2.hystogram(filename, begin=i, step=key3Length))
    Ex2.plotHystogram(hyst3List)
    key3 = Ex2.findKeyFromHystogramList(hyst3List)
    
    #Decoding of the last file
    Ex2.Ex1.encodingDecodingFromFile(filename, 'ResultatQuestion3.txt', key3)
    