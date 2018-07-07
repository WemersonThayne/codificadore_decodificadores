# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 16:03:45 2018

@author: wemerson
"""


from heapq import heappush, heappop, heapify
import collections
from io import StringIO
import base64

#codificador
def compress(uncompressed):
    """Compress a string to a list of output symbols."""
 
    # Build the dictionary.
    dict_size = 256
    #dictionary = dict((chr(i), i) for i in xrange(dict_size))
    dictionary = {chr(i): i for i in range(dict_size)}
 
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
 
    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return result

def decompress(compressed):
    """Decompress a list of output ks to a string."""
 
    # Build the dictionary.
    dict_size = 256
#     dictionary = dict((i, chr(i)) for i in xrange(dict_size))
    dictionary = {i: chr(i) for i in range(dict_size)}
 
    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = StringIO()
    w = chr(compressed.pop(0))
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)
 
        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
 
        w = entry
    return result.getvalue()
#Essa função tem como objetivo pegar um arquivo de texto, recuperar as informações dentro dele, codificar em um arquivo diferente ultilizando 
#os codificados e decodificadores de Lempel-Ziv
def leituraArquivo():
    
    texto_plano = open("texto_original.txt", "r").read()
    print(texto_plano)
    compressed = compress(texto_plano)
    codificado_lzv=str(compressed)
    texto_compactado = open("texto_codificado_lzv.txt", "w").writelines(codificado_lzv)
    texto_compactado=open("_texto_codificado_lzv.txt", "r").read()
    print(texto_compactado)
#Essa função tem como objetivo pegar uma imagem, recuperar as informações dentro dele, codificar em um arquivo diferente ultilizando 
#os codificados e decodificadores de Lempel-Ziv 
def leituraImagem():
    imagem = open("imagem_original.jpg", "rb")
    texto_imagem = base64.b64encode(imagem.read()).decode("utf8")
    imagem_codificada_LZV=compress(str(texto_imagem))
    imagem_codificada_LZV=str(imagem_codificada_LZV)
    #print(imagem_codificada_LZV)
    arquivo_imagem_cod_LZV = open("arquivo_imagem_codificada_lzv.txt", "w").writelines(imagem_codificada_LZV)
    arquivo_imamgem_cod=open("arquivo_imagem_codificada_lzv.txt", "r").read()
    print(arquivo_imamgem_cod)
    
def main():
    leituraArquivo()
    leituraImagem()

if __name__=="__main__":
    main()
