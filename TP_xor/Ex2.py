# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 15:28:09 2020

@author: Andre
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 08:37:26 2020

@author: geii
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import Ex1


def hystogram(filename, begin=0, step=1):
    try:
        f = open(filename, 'rb')
    except FileNotFoundError:
        print('unable to open ', filename)
        sys.exit(-1)
    
    #Compute the hystogram of the file
    i = 0
    hystogramArray = np.zeros((256), int)
    while 1:
        f.seek(begin + i * step)
        data = f.read(1)
        if data == b'':
            break
        dataInt = int.from_bytes(data, byteorder='big')
        hystogramArray[dataInt] += 1
        i+=1
    f.close()
    return hystogramArray


#Plot the hystogram
def plotHystogram(hystogramList):
    for hyst in hystogramList:    
        plt.plot(hyst)
    plt.show()
    return



#We search the key, knowing that the most used key is space (32 in ASCII)
def findKeyFromHystogramList(hystogramList):
    keyString = ''
    for hyst in hystogramList:
        index = int(np.argmax(hyst))
        keyChar = index ^ 32
        key = keyChar.to_bytes(1, byteorder='big')
        keyString += key.decode('latin-1')
    return keyString




if __name__ == '__main__':
    #Retrieval of the first key
    key1Length = 12
    hyst1List = []
    for i in range(key1Length):
        hyst1List.append(hystogram('question1.enc', begin=i, step=key1Length))
    plotHystogram(hyst1List)
    key1 = findKeyFromHystogramList(hyst1List)
    
    
    #Retrieval of the second key
    key2Length = 37
    hyst2List = []
    for i in range(key2Length):
        hyst2List.append(hystogram('question2.enc', begin=i, step=key2Length))
    plotHystogram(hyst2List)
    key2 = findKeyFromHystogramList(hyst2List)
    
    #Decoding of the second file
    Ex1.encodingDecodingFromFile('question2.enc', 'ResultatQuestion2.txt', key2)
    