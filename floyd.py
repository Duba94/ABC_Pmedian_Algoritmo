#!/usr/bin/env python
import sys
import os
import array
from io import open
from math import inf
from itertools import product


import numpy as np

#DECLARACION DE VARIABLES
path="problema.txt"
numaris=200
aristas=[]
nodos=100


os.system('clear')

#FUNCIONES
def leerArchivo(path):
    cont=0
    file = open(path,"r")
    for linea in file.readlines():
        x = linea[:-1].split(";")
        aristas.append([0] * len(x))
        for i in range(len(x)):
            aristas[cont][i]=int(x[i])
        cont=cont+1
    file.close
    

def floyd_warshall(n, edge):
    rn = range(n)
    dist = [[inf] * n for i in rn]
    for i in rn:
        dist[i][i] = 0
    for u, v, w in edge:
        dist[u-1][v-1] = w
        #dist[v-1][u-1]=w
    for k, i, j in product(rn, repeat=3):
        sum_ik_kj = dist[i][k] + dist[k][j]
        if dist[i][j] > sum_ik_kj:
            dist[i][j] = sum_ik_kj
            #dist[j][i] = sum_ik_kj

    return dist
    
#CODIGO PRINCIPAL
leerArchivo(path)
#for a in range(numaris):
  # print(aristas[a])
#print(aristas)
#resul=floyd_warshall(nodos, [[1, 2, 8], [2, 3, 5], [3, 4, 3], [4, 5, 4], [5, 6, 3],[1, 5, 2], [2, 6, 6], [3, 5, 6]])
resul=floyd_warshall(nodos,aristas)
for n in range(nodos):
    print(resul[n])




