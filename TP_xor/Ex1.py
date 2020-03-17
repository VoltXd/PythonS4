# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 08:37:26 2020

@author: geii
"""

import sys

def encodingDecodingFromFile(filename, wFilename, key):
    try:
        f = open(filename, 'rb')
    except FileNotFoundError:
        print('unable to open ', filename)
        sys.exit(-1)
        
    try:
        fw = open(wFilename, 'wb')
    except FileNotFoundError:
        print('No such file or directory: ', wFilename)
        sys.exit(-1)    
    except PermissionError:
        print('unauthorized to open ', wFilename)
        sys.exit(-1)
    
    keyLength = len(key)
    i = 0
    while 1:
        data = f.read(1)
        if data == b'':
            break
        data = int.from_bytes(data, byteorder='big')
        bKey = key[i%keyLength].encode('latin-1')
        iKey= int.from_bytes(bKey, byteorder='big')
        code = data ^ iKey
        code = code.to_bytes(1, byteorder='big')
        if code == b'\n':
            fw.write(b'\r')
        fw.write(code)
        i+=1
    return 
    
encodingDecodingFromFile('question1.enc', 'ResultatQuestion1.txt', 'z}ed!/?fG/YX')
    