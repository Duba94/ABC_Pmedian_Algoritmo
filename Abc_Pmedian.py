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
lim=6
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
evaxi=[0]*np
probxi=[0]*np
proAcumxi=[0]*np
contxi=[0]*np
mejorxiBin=[0]*d
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

#funcion que busca las medianas en una solucion
def buscarmedianas(lista):
    pmed=[0]*p
    cont=0
    for z in range(d):
        if(lista[z]==1):
            pmed[cont]=z
            cont=cont+1
    return pmed


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

def mejorarfuente(cand,evacad,fselect):
    if(evacad<evaxi[fselect]):
        remplazarfuente(cand,evacad,fselect)
    else:
        contxi[fselect]=contxi[fselect]+1

def remplazarfuente(nuevafuente,evafuente,fselect):
    for i in range(d):
        sol[fselect][i]=nuevafuente[i]
    evaxi[fselect]=evafuente
    contxi[fselect]=0

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
        sol.append([0] * d)
for i in range(np):
    for a in range(d):
        k=li+uniform(0,1)*(ls-li)
        sol[i][a]=k

#funcion para representar en medianas
def solPoblacionInicial():
    temp=[0]*d
    for i in range(np):
        temp=sol[i]
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
        mejorarfuente(cand,evaxit,i)
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
        print(evaxit)
        mejorarfuente(cand,evaxit,fselect)

def reemplazaragotados():
    temp=[0]*d
    for a in range(np): 
        if (contxi[a]==lim):
            for p in range(d):
              k=li+uniform(0,1)*(ls-li)
              temp[p]=k
            print("temporal:",temp)
            lisOrdenada = ordenamientoBurbuja(temp, len(temp))
            print("Ordenada:",lisOrdenada)
            lisBinaria=conversionBinaria(lisOrdenada,temp)
            print("binaria:",lisBinaria)
            evaxit=evaluacionSolucion(lisBinaria)
            print(evaxi)
            remplazarfuente(temp,evaxit,a)
            
def mejorglobal():
    global evaxi
    global mejorxiBin
    global mejoreva
    mejorsol=[0]*d
    pos = buscarmenor()
    mejorsol=sol[pos]
    lisOrdenada = ordenamientoBurbuja(mejorsol, len(mejorsol))
    mejorxiBin=conversionBinaria(lisOrdenada, mejorsol)
    mejoreva=evaxi[pos]
    
def busquedalocal():
    global mejorxiBin
    global mejoreva
    tempBin=[0]*d 
    tempBin=mejorxiBin[:]  
    pmed=buscarmedianas(tempBin)
    for a in range(p):
        pos=pmed[a]
        tempBin[pos]=0
        for n in range(d):
            if(mejorxiBin[n]==0):
                tempBin[n]=1
                evaxit=evaluacionSolucion(tempBin)
                if(evaxit < mejoreva):
                    mejorxiBin=tempBin[:]
                    mejoreva=evaxit
                tempBin[n]=0
    
                
#codigo principal    
iniciarPoblacion()
solPoblacionInicial()
imprimir()
print("---------------------------------------------------------")
while k< mcn:
    k=k+1
    solCandidatasEmp()
    calculoProbabilidad()
    imprimir()
    print("----------------------------------------------------------")
    solCandidatasObs()
    calculoProbabilidad()
    imprimir()
    print("----------------------------------------------------------")
    reemplazaragotados()
    calculoProbabilidad()
    imprimir()
    print("----------------------------------------------------------")
    mejorglobal()
    print("mejor global: ","medianas->",mejorxiBin,"evaluacion->",mejoreva)
    busquedalocal()
    print("mejor globalBuevo: ","medianas->",mejorxiBin,"evaluacion->",mejoreva)
    print("----------------------------------------------------------")
print("mejor final: ","medianas->",mejorxiBin,"evaluacion->",mejoreva)


