from collections import Counter
from normas import normas_Geffen
import re

#definición de los índices para buscar los datos del sujeto en cada score dentro de las normas
#output: lista con tres indices nse,sexo y edad
def get_index(normas,nse,sexo,edad):
    for y in normas["nse"]:
        if normas["nse"][y][0] <= int(nse) <= normas["nse"][y][1]:
            nse_index=y

    sex_index=int(sexo)

    for x in normas["edad"]:
        if normas["edad"][x][0] <= int(edad) <= normas["edad"][x][1]:
            edad_index=x

    return [nse_index,sex_index,edad_index]

#definición de la media y desvío de cada score para el sujeto
#output: diccionario con un key por score. Cada value es una lista de [media,desvio]
def get_normas(normas, raw_scores, index):
    nse_index=index[0]
    sex_index=index[1]
    edad_index=index[2]
    normas_sujeto={}
    for x in raw_scores:
        normas_sujeto[x]=[normas["norms"][x][nse_index][0][sex_index][edad_index],normas["norms"][x][nse_index][1][sex_index][edad_index]]
    return normas_sujeto

#entrada es un string           
def limpiarEntrada(entrada):
    entrada=entrada.split(",")
    output=[]
    for palabra in entrada:
        palabra = palabra.strip().lower().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
        if len(palabra)>0:
            output.append(palabra)
        else:
            output.append(None)
    return output

#entrada es una palabra
def sort(entrada,tipo,listaA,listaB):
    out=[]
    if tipo=="main":    
        for x in entrada:
            if x in listaA:
                out.append(x)
    elif tipo=="side":
        for x in entrada:
            if x in listaB:
                out.append(x)
    else:
        for x in entrada:
            if x not in listaA and x not in listaB:
                out.append(x)
    return out

def convert_scores(self):
    for x in raw_scores:
        z_scores[x]=(raw_scores[x]-normas_sujeto[x][0])/normas_sujeto[x][1]

def update_raw(self):
    raw_scores={
        "t1":targets[0],
        "t2":targets[1],
        "t3":targets[2],
        "t4":targets[3],    
        "t5":targets[4],
        "tB":targets[5],
        "t6":targets[6],
        "t7":targets[7],
        "rec":targets[8],
        "total_inmediato":targets[0]+targets[1]+targets[2]+targets[3]+targets[4],
        }

def puntuarTrial():
    trial=len(mainM)-1
    aciertos=0
    intrusiones=0
    confabulaciones=0
    reps=sum(repeticionesM[trial][0])+sum(repeticionesM[trial][1])+repeticionesM[trial][2]
    if trial == 5:
        for x in sideM[5]:
            if x:
                aciertos+=1
        for x in mainM[5]:
            if x:
                intrusiones+=1
        for x in extrasL[5]:
            if x != None:
                confabulaciones+=1
    else:
        for x in mainM[trial]:
            if x:
                aciertos+=1
        for x in sideM[trial]:
            if x:
                intrusiones+=1 
        for x in extrasL[trial]:
            if x != None:
                confabulaciones+=1
        
    targets[trial]=aciertos
    intrusiones[trial]=intrusiones
    confab[trial]=confabulaciones
    repeticiones[trial]=reps
    update_raw()
    convert_scores()

#entrada es una string
def registrarTrial(entrada,listaA,listaB):
    palabras=limpiarEntrada(entrada)
    main=sort(palabras,"main",listaA,listaB)
    main_count=[]
    for x in listaA:
        c=main.count(x)
        main_count.append(c)
    side=sort(palabras,"side",listaA,listaB)
    side_count=[]
    for x in listaB:
        c=side.count(x)
        side_count.append(c)
    extras=sort(palabras,"extra",listaA,listaB)
    extras_dict= dict(Counter(extras))
    repeticiones_main=[]
    for x in main_count:
        if x>1:
            repeticiones_main.append(x-1)
        else:
            repeticiones_main.append(0)
    repeticiones_side=[]
    for x in side_count:
        if x>1:
            repeticiones_side.append(x-1)
    else:
        repeticiones_side.append(0)

    repeticiones_extra=sum(extras_dict.values())-len(extras_dict)
    repeticiones_conj=[repeticiones_main,repeticiones_side,repeticiones_extra]
   
    return (main_count, side_count, extras, repeticiones_conj)