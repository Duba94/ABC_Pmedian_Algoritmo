#!/usr/bin/env python
import sys
import os
from random import uniform,randint
import array

print("ABC-PMEDIAN ALGORITMO")
M=[[0,8,8,6,2,5],
   [8,0,5,8,9,6],
   [8,5,0,3,6,9],
   [6,8,3,0,4,7],
   [2,9,6,4,0,3],
   [5,6,9,7,3,0]]

#Parametros iniciales 
l=6
cs=6
np=3
d=6
ls=5.0
li=-5.0
mcn=5
K=0
p=2

#almacenadores
sol=[]
evaxi=[]
probxi=[]
proAcumxi=[]
contxi=[]
mejorxi=[]
mejoreva=0



#----------FUNCIONES AUXILIARES--------------

#Funcion para ordenar la solucion de menor a mayor
def ordenamientoBurbuja(listaTem,tam):
    ord=listaTem[:]
    for i in range(1,tam):
        for j in range(0,tam-i):
            if(ord[j] > ord[j+1]):
                k = ord[j+1]
                ord[j+1] = ord[j]
                ord[j] = k
    return ord
#funcion para convertir menores p en 1 y otros en 0
def conversionBinaria(listaOrd,listaSol):
    bin=[0]*d
    for b in range(p):
        for z in range(d):   
            if (listaOrd[b]==listaSol[z]):
                bin[z]=1
    return  bin

#funcion para evaluar una solucion
def evaluacionSolucion(listaBin):
    suma=0
    for z in range(d):
        menor=10000
        for s in range(d):
            if(listaBin[s]==1 and M[z][s]< menor):
                menor=M[z][s]
        suma=suma+menor
    return suma

#funcion para crear una solucion candidata 
def CrearSolucionCandidata(i):
    temp=[0]*d
    for j in range(d):
        fi=uniform(-1,1)
        k=randint(0,np-1)
        xk=sol[k][j]
        xi=sol[i][j]
        r=xi+fi*(xi-xk)
        #print("fi:",fi,"/ k:",k,"/ xk:",xk,"/ xi:",xi,"/ r:",r)
        if(r>ls):
            r=ls
        if(r<li):
            r=li
        temp[j]=r
    return temp

def sumarevasol():
    sum=0
    for a in range(np):
        sum=sum+evaxi[a]
    return sum

def selectFuente():
    rulect=uniform(0,1)
    print("valor ruleta: ",rulect)
    for i in range(np):
        if(proAcumxi[i] > rulect):
            return i

def remplazarfuente(cand,evacad,fselect):
    if(evacad<evaxi[fselect]):
        for n in range(d):
            sol[fselect][n]=cand[n]
        evaxi[fselect]=evacad
        contxi[fselect]=0
    else:
        contxi[fselect]=contxi[fselect]+1
def buscarmenor():
    menor=evaxi[0]
    pos=0
    for i in range(np):
        val=evaxi[i]
        if(val<menor):
            menor=val
            pos=i
    return pos

def imprimir():
    print("Solucion: ",sol)
    print("Evaluacion: ",evaxi)
    print("Contadores: ",contxi)



#---------------FUNCIONES PRINCIPALES--------------------

#funcion para inicializar la poblacion inicial
def iniciarPoblacion():
    print("iniciando Poblacion....")    
for i in range(np):
        evaxi=[0] * np
        probxi=[0]* np
        mejorxi=[0]* d
        proAcumxi=[0]* np
        contxi=[0]* np
        sol.append([0] * d)
for i in range(np):
    for a in range(d):
        k=li+uniform(0,1)*(ls-li)
        sol[i][a]=k

#funcion para representar en medianas
def solPoblacionInicial():
    temp=[0]*d

    for i in range(np):
        for a in range(d):
            temp[a]=sol[i][a]
        print("temp:",temp)
        lisOrdenada=ordenamientoBurbuja(temp,len(temp))
        print("ordeMin:",lisOrdenada)
        lisBinaria=conversionBinaria(lisOrdenada,temp)
        print("binario:",lisBinaria)
        evaxi[i]=evaluacionSolucion(lisBinaria)

#funcion para buscar soluciones candicatas para las empleadas 
def solCandidatasEmp():
    evaxit=[0]*np
    for i in range(np):
        cand=CrearSolucionCandidata(i)
        print("cand:",cand)
        lisOrdenada = ordenamientoBurbuja(cand, len(cand))
        print("Ordenada:",lisOrdenada)
        lisBinaria=conversionBinaria(lisOrdenada,cand)
        print("binaria:",lisBinaria)
        evaxit=evaluacionSolucion(lisBinaria)
        remplazarfuente(cand,evaxit,i)
        print("f(xi): ",evaxit)

#funcion para calcular las probabilidades
def calculoProbabilidad():
    aux=0
    sumxi=sumarevasol()
    for a in range(np):
        prob=evaxi[a]/sumxi
        probxi[a]=prob
        proAcumxi[a]=aux+prob
        aux=proAcumxi[a]
    print("prob:",probxi)
    print("probAcum:",proAcumxi)

#funcion para selecionar una fuente a mejorar
def solCandidatasObs():
    for c in range(np):
        fselect=selectFuente()
        print("fuente selecionada:",fselect)
        cand=CrearSolucionCandidata(fselect)
        print("cand:",cand)
        lisOrdenada = ordenamientoBurbuja(cand, len(cand))
        print("Ordenada:",lisOrdenada)
        lisBinaria=conversionBinaria(lisOrdenada,cand)
        print("binaria:",lisBinaria)
        evaxit=evaluacionSolucion(lisBinaria)
        remplazarfuente(cand,evaxit,fselect)

def reemplazaragotados():
    temp=[0]*d
    for a in range(np): 
        if (contxi[a]==l):
            for p in range(d):
              k=li+uniform(0,1)*(ls-li)
              temp[p]=k
            lisOrdenada = ordenamientoBurbuja(temp, len(temp))
            print("Ordenada:",lisOrdenada)
            lisBinaria=conversionBinaria(lisOrdenada,temp)
            print("binaria:",lisBinaria)
            evaxit=evaluacionSolucion(lisBinaria)
            remplazarfuente(temp,evaxit,a)
            


def mejorglobal():
    pos = buscarmenor()
    for z in range(d):
        mejorxi[z]=sol[pos][z]
    mejoreva=evaxi[pos]
    print("mejor global",mejorxi,"->",mejoreva) 
    
def busquedalocal():
    print("busqueda local")        


#codigo principal    
iniciarPoblacion()
solPoblacionInicial()
imprimir()
k=k+1
print("---------------------------------------------------------")
solCandidatasEmp()
imprimir()
calculoProbabilidad()
print("----------------------------------------------------------")
solCandidatasObs()
imprimir()
calculoProbabilidad()
mejorglobal()

