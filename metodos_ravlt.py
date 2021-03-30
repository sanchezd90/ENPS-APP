from flask import Flask, render_template, redirect, url_for, request, Response, session
from collections import Counter
import re
import datetime
import pymongo
from metodos_db import *

cluster=pymongo.MongoClient("mongodb+srv://sanchezd90:dbuser-L6H6@cluster0.wwnbb.mongodb.net/<ENPS>?retryWrites=true&w=majority")
db=cluster["ENPS"]
col=db["normas"]
doc=col.find({"prueba":"RAVLT"})
normas=doc[0]

trialnames={
    0:"t1",
    1:"t2",
    2:"t3",
    3:"t4",    
    4:"t5",
    5:"tB",
    6:"t6",
    7:"t7",
    8:"t8",
    }

def set_index(normas,nse,sexo,edad):
    #definición de los índices para buscar los datos del sujeto en cada score dentro de las normas
    #output: lista con tres indices nse,sexo y edad
    for y in normas["nse"]:
        if normas["nse"][y][0] <= int(nse) <= normas["nse"][y][1]:
            nse_index=int(y)

    sex_index=int(sexo)

    for x in normas["edad"]:
        if normas["edad"][x][0] <= int(edad) <= normas["edad"][x][1]:
            edad_index=int(x)

    return [nse_index,sex_index,edad_index]


def set_norms(normas, raw_scores, index):
    #definición de la media y desvío de cada score para el sujeto
    #output: diccionario con un key por score. Cada value es una lista de [media,desvio]
    nse_index=index[0]
    sex_index=index[1]
    edad_index=index[2]
    normas_sujeto={}
    for x in raw_scores:
        normas_sujeto[x]=[normas["normas"][x][nse_index][0][sex_index][edad_index],normas["normas"][x][nse_index][1][sex_index][edad_index]]
    return normas_sujeto

           
def limpiarEntrada(entrada):
    #entrada es un string
    #saca los espacios y saca tilde a las vocales
    entrada=entrada.split(",")
    output=[]
    for palabra in entrada:
        palabra = palabra.strip().lower().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
        if len(palabra)>0:
            output.append(palabra)
        else:
            output.append(None)
    return output


def sort(entrada,tipo,listaA,listaB):
    #entrada es una palabra
    #clasifica 
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

def convert_scores():
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
        "t8":targets[8],
        "total_inmediato":targets[0]+targets[1]+targets[2]+targets[3]+targets[4],
        }

def puntuarTrial(trial,repeticiones,side,main,extras):
    aciertos=0
    intrusiones=0
    confabulaciones=0
    reps=sum(repeticiones[0])+sum(repeticiones[1])+repeticiones[2]
    for x in main:
        if x:
            aciertos+=1
    for x in side:
        if x:
            intrusiones+=1 
    for x in extras:
        if x != None:
            confabulaciones+=1

    return(aciertos,intrusiones,confabulaciones,reps)    
    #convert_scores()


def codificarInput(entrada,listaA,listaB):
    #entrada es una string
    #toma el input
    #lo limpia a través de limpiarEntrada()
    #clasifica cada palabra a traves de sort()
    #y arma un conteo de cuantas veces aparece una palabra target, contratarget, extra y repetida
    #output es una tupla con cuatro listas

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

    return (main_count, side_count, extras, repeticiones_conj,palabras)


def registrarTrial(listaA,listaB,trial_num,normas_sujeto,last=False):

    #ajuste para que en el trial_num 6 y 8 ubique los datos en el lugar indicado (porque lo hace desde resumen)
    #recupera el input del trial anterior desde la sesión
    if last:
        trial_num=trial_num+1
        checkbox_list=request.form.getlist("respuesta")
        t_input=""
        for x in checkbox_list:
            if t_input=="":
                t_input=x
            else:
                t_input=t_input+","+x
    else:
        t_input=request.form.get("respuesta")

    if t_input==None:
        pass
    else:
        #--CARGA DE MATRICES--#
        
        #recupera las matrices de recuentos en sesión
        main_M=session["puntajes"]["mainM"]
        side_M=session["puntajes"]["sideM"]
        extras_L=session["puntajes"]["extrasL"]
        repeticiones_M=session["puntajes"]["repeticionesM"]
        respuestas_M=session["puntajes"]["respuestasM"]
        
        #obtiene la lista de recuentos (main, side, extras, repeticiones)
        registro_trial=codificarInput(t_input,listaA,listaB)
        main=registro_trial[0]
        side=registro_trial[1]
        extras=registro_trial[2]
        repeticiones=registro_trial[3]
        palabras=registro_trial[4]
        
        #se carga en el lugar correspondiente cada lista de recuentos del trial actual
        main_M[trial_num-1]=main
        side_M[trial_num-1]=side
        extras_L[trial_num-1]=extras
        repeticiones_M[trial_num-1]=repeticiones
        respuestas_M[trial_num-1]=palabras

        #se actualiza las matrices en sesión con los recuentos del trial actual    
        session["puntajes"]["mainM"]=main_M
        session["puntajes"]["sideM"]=side_M
        session["puntajes"]["extrasL"]=extras_L
        session["puntajes"]["repeticionesM"]=repeticiones_M
        session["puntajes"]["respuestasM"]=respuestas_M

        #--CARGA DE PUNTAJES--#

        #trae los registros en sesión de puntajes
        aciertos_S=session["puntajes"]["targets"]
        intrusiones_S=session["puntajes"]["intrusiones"]
        confab_S=session["puntajes"]["confab"]
        repeticiones_S=session["puntajes"]["repeticiones"]

        #calcula los puntajes del trial
        puntuaciones=puntuarTrial(trial_num,repeticiones,side,main,extras)
        aciertos=puntuaciones[0]
        intrusiones=puntuaciones[1]
        confabulaciones=puntuaciones[2]
        repeticiones=puntuaciones[3]

        #se carga en el lugar correspondiente cada puntaje del trial actual
        key=str(trial_num-1)
        aciertos_S[key]=aciertos
        intrusiones_S[key]=intrusiones
        confab_S[key]=confabulaciones
        repeticiones_S[key]=repeticiones

        #se actualizan los puntajes en sesión con los recuentos del trial actual 
        session["puntajes"]["targets"]=aciertos_S
        session["puntajes"]["intrusiones"]=intrusiones_S
        session["puntajes"]["confab"]=confab_S
        session["puntajes"]["repeticiones"]=repeticiones_S

        #--CALCULO DE Z-SCORES--#
        
        #trae los puntajes de sesión
        raw_scores_S=session["puntajes"]["raw_scores"]
        z_scores_S=session["puntajes"]["z_scores"]

        #ajuste de num trial
        trial_num=trial_num-1

        #esta definición tiene que quedar acá luego del ajuste del num trial
        for k,v in trialnames.items():
            if k==trial_num:
                trial_name=v

        #registrar raw_scores de trials y convertir en z scores
        raw_scores_S[trial_name]=aciertos
        z_scores_S[trial_name]=(aciertos-normas_sujeto[trial_name][0])/normas_sujeto[trial_name][1]
        
        #registrar raw_scores de otros scores y convertir en z scores
        try:
            if trial_num==4:
                raw_scores_S["total_inmediato"]=raw_scores_S["t1"]+raw_scores_S["t2"]+raw_scores_S["t3"]+raw_scores_S["t4"]+raw_scores_S["t5"]
                z_scores_S["total_inmediato"]=(aciertos-normas_sujeto["total_inmediato"][0])/normas_sujeto["total_inmediato"][1]
        except:
            pass

            
        #guardar scores en sesión
        session["puntajes"]["raw_scores"]=raw_scores_S
        session["puntajes"]["z_scores"]=z_scores_S

        #definir tiempo de toma del trial diferido
        if trial_num==6:
            now=datetime.datetime.now()
            dead = now+datetime.timedelta(minutes=20)
            minute=str(dead.minute)
            if len(minute)==1:
                minute="0"+minute
            timeUp=str(dead.hour)+":"+minute
            session["timeUp_str"]=timeUp

        codigo=session["codigo"]
        datos=session["puntajes"]
        update_doc(codigo,datos)


