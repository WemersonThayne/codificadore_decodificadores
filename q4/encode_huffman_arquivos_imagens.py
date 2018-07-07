# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 14:15:27 2018

@author: wemerson
"""

#cabeçalhos de todos os programas
from heapq import heappush, heappop, heapify
import collections
from io import StringIO
import base64

# função do codificador de Huffman
def encode(simbolos_frequencia):
	#Huffman encode the given dict mapping symbols to weights
	#Huffman codifica os símbolos de mapeamento dict para pesos

	lista_prioridade = [[freq, [simbolo, ""]] for simbolo, freq in simbolos_frequencia.items()]

	heapify(lista_prioridade)

	while len(lista_prioridade) > 1:

		primeiro_item = heappop(lista_prioridade)
		segundo_item = heappop(lista_prioridade)

		for pair in primeiro_item[1:]:
			pair[1] = '0' + pair[1]

		for pair in segundo_item[1:]:
			pair[1] = '1' + pair[1]

		heappush(lista_prioridade, [primeiro_item[0] + segundo_item[0]] + primeiro_item[1:] + segundo_item[1:])

	return sorted(heappop(lista_prioridade)[1:], key=lambda p: (len(p[-1]), p))

def convert(frase, bits):

	frase_codificada = ''

	for c in frase:
		for bit in bits:
			if c == bit[0]:
				frase_codificada += bit[1]

	return frase_codificada

def decode(frase_codificada, bits):
	
	frase_decodificada = ''

	temp = ''

	inicio = 0

	for fim in range(len(frase_codificada) + 1):
		igual = 0
		for bit in bits:
			if frase_codificada[inicio:fim] == bit[1] and inicio != len(frase_codificada) - 1:
				igual += 1
				temp = bit[0]

			elif frase_codificada[inicio:fim] == bit[1] and inicio == len(frase_codificada) - 1:
				igual += 1
				temp = bit[0]

		if igual == 1:
			frase_decodificada += temp
			inicio = fim
		else:
			continue

	return frase_decodificada

imagem_original = open("imagem_original.jpg", "rb")
imagem_texto = base64.b64encode(imagem_original.read()).decode("utf8")

arquivo_imagem_texto_original = open("texto_original.txt", "w").writelines(imagem_texto)


simbolos_frequencia = collections.Counter(imagem_texto)

bits = encode(simbolos_frequencia)
frase_codificada = convert(imagem_texto, bits)

frase_decodificada = decode(frase_codificada, bits)

arquivo_imagem_texto_codificado = open("imagem_texto_codificado.txt", "w").writelines(frase_codificada)

imagem_codificada = open("arquivos_imagem_codificada.jpg", "wb")
imagem_codificada.write(base64.b64decode(frase_decodificada))
imagem_codificada.close()

