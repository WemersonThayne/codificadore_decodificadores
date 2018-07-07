# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 14:25:04 2018

@author: wemerson
"""



from heapq import heappush, heappop, heapify
import collections
from io import StringIO
import base64

from collections import Counter
 
def cumulative_freq(freq):
    cf = {}
    total = 0
    for b in range(256):
        if b in freq:
            cf[b] = total
            total += freq[b]
    return cf
 
def arithmethic_coding(bytes, radix):
 
    # The frequency characters
    freq = Counter(bytes)
 
    # The cumulative frequency table
    cf = cumulative_freq(freq)
 
    # Base
    base = len(bytes)
 
    # Lower bound
    lower = 0
 
    # Product of all frequencies
    pf = 1
 
    # Each term is multiplied by the product of the
    # frequencies of all previously occurring symbols
    for b in bytes:
        lower = lower*base + cf[b]*pf
        pf *= freq[b]
 
    # Upper bound
    upper = lower+pf
 
    pow = 0
    while True:
        pf //= radix
        if pf==0: break
        pow += 1
 
    enc = (upper-1) // radix**pow
    return enc, pow, freq
 
def arithmethic_decoding(enc, radix, pow, freq):
 
    # Multiply enc by radix^pow
    enc *= radix**pow;
 
    # Base
    base = sum(freq.values())
 
    # Create the cumulative frequency table
    cf = cumulative_freq(freq)
 
    # Create the dictionary
    dict = {}
    for k,v in cf.items():
        dict[v] = k
 
    # Fill the gaps in the dictionary
    lchar = None
    for i in range(base):
        if i in dict:
            lchar = dict[i]
        elif lchar is not None:
            dict[i] = lchar
 
    # Decode the input number
    decoded = bytearray()
    for i in range(base-1, -1, -1):
        pow = base**i
        div = enc//pow
 
        c  = dict[div]
        fv = freq[c]
        cv = cf[c]
 
        rem = (enc - pow*cv) // fv
 
        enc = rem
        decoded.append(c)
 
    # Return the decoded output
    return bytes(decoded)

radix = 10    

imagem_original = open("imagem_original.jpg", "rb")


imagem_codificada = open("imagem_codificada.jpg", "wb")
	
for item in imagem_original:
	enc, pow, freq = arithmethic_coding(item, radix)
	dec = arithmethic_decoding(enc, radix, pow, freq)
	
	imagem_codificada.write(dec)
		
	if item != dec:
		raise Exception("\tHowever that is incorrect!")





