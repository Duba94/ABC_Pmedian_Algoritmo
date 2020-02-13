#!/usr/bin/env python
import sys
import os
from random import uniform,randint
import array

#matriz de menores distancias entre los nodos del grafo
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
k=0
p=2

#almacenadores
sol=[]
evaxi=[0]*np
probxi=[0]*np
proAcumxi=[0]*np
contxi=[0]*np
mejoreva=0
mejorxi=[0]*d
mejorEvaLocal=0
mejorxiLocal=[]*d
mejorevaglobal=0
mejorxiglobal=[0]*d



#----------FUNCIONES AUXILIARES--------------

#Funcion para ordenar la solucion de menor a mayor
def ordenamientoBurbuja(listaTem,tam):
    listaord=listaTem[:]
    for i in range(1,tam):
        for j in range(0,tam-i):
            if(listaord[j] > listaord[j+1]):
                k = listaord[j+1]
                listaord[j+1] = listaord[j]
                listaord[j] = k
    return listaord

#funcion para convertir menores p en 1 y otros en 0
def conversionBinaria(listaOrd,listaSol):
    listaxi=[0]*d
    for m in range(p):
        for j in range(d):   
            if (listaOrd[m]==listaSol[j]):
                listaxi[j]=1
    return  listaxi

#funcion que busca las medianas en una solucion
def buscarmedianas(listaxi):
    pmed=[0]*p
    cont=0
    for j in range(d):
        if(listaxi[j]==1):
            pmed[cont]=j
            cont=cont+1
    return pmed

#funcion para evaluar una solucion
def evaluacionSolucion(listaxi):
    suma=0
    for n in range(d):
        menor=10000
        for j in range(d):
            if(listaxi[j]==1 and M[n][j]< menor):
                menor=M[n][j]
        suma=suma+menor
    return suma

#funcion para crear una solucion candidata 
def CrearSolucionCandidata(i):
    cand=[0]*d
    for j in range(d):
        fi=uniform(-1,1)
        k=randint(0,np-1)
        xk=sol[k][j]
        xi=sol[i][j]
        r=xi+fi*(xi-xk)
        if(r>ls):
            r=ls
        if(r<li):
            r=li
        cand[j]=r
    return cand

#funcion que retorna la sumatoria de la evaluacion de cada una las soluciones 
def sumarevasol():
    sum=0
    for i in range(np):
        sum=sum+evaxi[i]
    return sum

#funcion que selecciona una fuente por el metodo de la ruleta
def selectFuente():
    rulect=uniform(0,1)
    print("valor ruleta: ",rulect)
    for i in range(np):
        if(proAcumxi[i] > rulect):
            return i

#funcion que remplaza una fuente selecionada  de la solucion por una  fuente nueva
def remplazarfuente(xinuevafuente,evanuevafuente,xiselect):
    for i in range(d):
        sol[xiselect][i]=xinuevafuente[i]
    evaxi[xiselect]=evanuevafuente
    contxi[xiselect]=0

#funcion que determina si una fuente candidata mejora a una fuente de la solucion,
#si no es asi, el contador de la fuente de la solucion aumenta
def mejorarfuente(cand,evacad,xiselect):
    if(evacad<evaxi[xiselect]):
        remplazarfuente(cand,evacad,xiselect)
    else:
        contxi[xiselect]=contxi[xiselect]+1

#funcion que busca la posicion del la menor evaluacion de las fuentes de la solucion
def buscarmenor():
    menor=evaxi[0]
    pos=0
    for i in range(np):
        val=evaxi[i]
        if(val<menor):
            menor=val
            pos=i
    return pos

#funcion que imprime la solucion, la evaluacion de las soluciones y sus contadores de fallo
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
    for j in range(d):
        sol[i][j]=li+uniform(0,1)*(ls-li)

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
        print("f(xi): ",evaxi[i])

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
    for i in range(np):
        prob=evaxi[i]/sumxi
        probxi[i]=prob
        proAcumxi[i]=aux+prob
        aux=proAcumxi[i]
    print("prob:",probxi)
    print("probAcum:",proAcumxi)

#funcion para selecionar una fuente a mejorar
def solCandidatasObs():
    for i in range(np):
        xiselect=selectFuente()
        print("fuente selecionada:",xiselect)
        cand=CrearSolucionCandidata(xiselect)
        print("cand:",cand)
        lisOrdenada = ordenamientoBurbuja(cand, len(cand))
        print("Ordenada:",lisOrdenada)
        lisBinaria=conversionBinaria(lisOrdenada,cand)
        print("binaria:",lisBinaria)
        evaxit=evaluacionSolucion(lisBinaria)
        print(evaxit)
        mejorarfuente(cand,evaxit,xiselect)
#funcion que busca los agotados y los remplaza con una nueva solucion
def reemplazaragotados():
    temp=[0]*d
    for i in range(np): 
        if (contxi[i]>=lim):
            for j in range(d):
                temp[j]=li+uniform(0,1)*(ls-li)
            print("temporal:",temp)
            lisOrdenada = ordenamientoBurbuja(temp, len(temp))
            print("Ordenada:",lisOrdenada)
            lisBinaria=conversionBinaria(lisOrdenada,temp)
            print("binaria:",lisBinaria)
            evaxit=evaluacionSolucion(lisBinaria)
            print(evaxi)
            remplazarfuente(temp,evaxit,i)
            contxi[i]=0

#funcion que busca la mejor solucion basica             
def mejorSolucion():
    global evaxi
    global mejorxi
    global mejoreva
    mejorsol=[0]*d
    pos = buscarmenor()
    mejorsol=sol[pos]
    lisOrdenada = ordenamientoBurbuja(mejorsol, len(mejorsol))
    mejorxi=conversionBinaria(lisOrdenada, mejorsol)
    mejoreva=evaxi[pos]

#funcion que busca la mejor solucion Local    
def busquedalocal():
    global mejorxi
    global mejoreva
    global mejorxiLocal
    global mejorEvaLocal
    tempxi=[0]*d 
    tempxi=mejorxi[:] 
    mejorEvaLocal=mejoreva
    mejorxiLocal=mejorxi[:] 
    pmed=buscarmedianas(tempxi)
    for m in range(p):
        pos=pmed[m]
        tempxi[pos]=0
        for j in range(d):
            if(mejorxi[j]==0):
                tempxi[j]=1
                evaxit=evaluacionSolucion(tempxi)
                if(evaxit < mejorEvaLocal):
                    mejorxiLocal=tempxi[:]
                    mejorEvaLocal=evaxit
                tempxi[j]=0

#funcion donde se determina el mejor global entre el el actual mejor global y el mejor local
def mejorglobal():
    global mejorevaglobal
    global mejorxiglobal
    if(mejorEvaLocal < mejorevaglobal):
        mejorevaglobal=mejorEvaLocal
        mejorxiglobal=mejorxiLocal[:]   
                
#   CODIGO PRINCIPAL 
print("")  
print("*************************** ABC-PMEDIAN ALGORITMO ************************")
iniciarPoblacion()
solPoblacionInicial()
mejorSolucion()
mejorevaglobal=mejoreva
mejorxiglobal=mejorxi
imprimir()
while k < mcn:  
    k=k+1
    print(">>>>>>>>>>>>>>>> CICLO:",k," <<<<<<<<<<<<<<<<<")
    print("")
    print("------SOLUCIONES CANDIDATAS EMP------")
    solCandidatasEmp()
    calculoProbabilidad()
    imprimir()
    print("------SOLUCIONES CANDIDATAS OBS-------")
    solCandidatasObs()
    calculoProbabilidad()
    imprimir()
    print("------REMPLAZO FUENTES AGOTADAS-------")
    reemplazaragotados()
    calculoProbabilidad()
    imprimir()
    print("------MEMORIZA MEJOR SOLUCION----------")
    mejorSolucion()
    print("mejor Basico: ","medianas->",mejorxi,"evaluacion->",mejoreva)
    busquedalocal()
    print("mejor Local: ","medianas->",mejorxiLocal,"evaluacion->",mejorEvaLocal)
    mejorglobal()
    print("mejor Global: ","medianas->",mejorxiglobal,"evaluacion->",mejorevaglobal)
    print("")


