from flask import Flask, render_template, redirect, url_for, request, Response, session
from metodos_ravlt import *
from metodos_db import *
from metodos_redaccion import *
from metodos_app import *
import datetime


app = Flask(__name__)
app.secret_key="a2S3d4F"

#
@app.route("/")
def inicio_www():
    return redirect(url_for("enps_www"))

#
@app.route("/enps", methods=["GET","POST"])
def enps_www():
    return render_template("enps.html")

#
@app.route("/enps/create", methods=["GET","POST"])
def create_www():
    return render_template("create.html")

#
@app.route("/enps/create/set", methods=["GET","POST"])
def enps_set_www():
    if request.method == "POST":
        nombre=request.form["nombre"]
        apellido=request.form["apellido"]
        dni=request.form["dni"]
        fechaNac=request.form["fechaNac"]
        edad=calculateAge(fechaNac)
        educacion=request.form["educacion"]
        sexo=request.form["sexo"]
        codigo_evento=round(datetime.datetime.now().timestamp())
        codigo_evento=str(dni)+"_"+str(codigo_evento)
        session["cod_evento"]=codigo_evento
        fecha=datetime.datetime.now()
        fecha=fecha.strftime("%d/%m/%y")
        insert_event(nombre, apellido, dni, edad, educacion, sexo, codigo_evento, fecha, fechaNac)
        return redirect(url_for("evento_www"))
    else:
        return redirect(url_for("create_www"))

#
@app.route("/enps/recover", methods=["GET","POST"])
def recover_www():
    all_events=get_all_events()
    return render_template("recover.html",eventos=all_events)

@app.route("/enps/recover/<codigo>", methods=["GET","POST"])
def recover_cod_www(codigo):
    session["cod_evento"]=codigo
    return redirect(url_for("evento_www"))

#
@app.route("/enps/evento", methods=["GET","POST"])
def evento_www():
    codigo_evento=session["cod_evento"]
    datos_evento=get_event(codigo_evento)
    nombre=datos_evento["nombre"]
    apellido=datos_evento["apellido"]
    dni=datos_evento["dni"]
    edad=datos_evento["edad"]
    fechaNac=datos_evento["fechaNac"]
    educacion=datos_evento["educacion"]
    sexo=datos_evento["sexo"]
    codigo=datos_evento["cod_evento"]
    fecha=datos_evento["fecha"]
    pruebas_admin=datos_evento["pruebas_admin"]
    if pruebas_admin==None:
        pruebas_admin=[]
    dic_pruebas_admin={}
    reportes={}
    for x in pruebas_admin:
        key=prueba_from_cod(x)
        dic_pruebas_admin[key]=x
        parrafo=get_data(x,"parrafo")
        reportes[key]=parrafo["parrafo"]
    update_reportes(codigo_evento, reportes)
    pruebas_disponibles=get_pruebas_disp()
    session["nombre"]=nombre
    session["apellido"]=apellido
    session["dni"]=dni
    session["edad"]=edad
    session["educacion"]=educacion
    session["sexo"]=sexo
    return render_template(
        "evento.html",
        nombre=nombre, 
        apellido=apellido, 
        dni=dni, 
        edad=edad,
        fechaNac=fechaNac, 
        educacion=educacion, 
        sexo=sexo,
        fecha=fecha, 
        pruebas=pruebas_admin,
        lista_pruebas_disp=pruebas_disponibles,
        dic_pruebas_admin=dic_pruebas_admin,
        dic_reportes=reportes
        )

#home para cargar los datos iniciales
@app.route("/enps/ravlt/config", methods=["GET","POST"])
def ravlt_config_www():
    return render_template("ravlt_config.html")

@app.route("/enps/ravlt/set", methods=["GET","POST"])
def ravlt_set_www():
    if request.method == "POST":
        #define qué lista se va a usar entre principal o alternativa
        ravlt_data=get_appData("ravlt")
        session["ravlt_tnames"]=ravlt_data["trialnames"]
        if request.form["lista"]=="0":
            session["listaA"]=ravlt_data["lista1A"]
            session["listaB"]=ravlt_data["lista1B"]
            session["listaRec"]=ravlt_data["rec1"]
        else:
            session["listaA"]=ravlt_data["lista2A"]
            session["listaB"]=ravlt_data["lista2B"]
            session["listaRec"]=ravlt_data["rec2"]
        #define qué normas se va a usar y las trae de mongoDB
        normas_name=request.form["normas"]
        normas=get_norms("RAVLT",normas_name)
        
        #se inician los diccionarios de sesión para almacenar los puntajes
        #targets, intrusiones, confab y repeticiones parten de 0. 
        #las matrices parten con una entrada por trial con valor None
        #raw_scores parten de 0
        #z_scores parten de con valor None
        session["puntajes"]={
            "targets":{
                "0":0,
                "1":0,
                "2":0,
                "3":0,
                "4":0,
                "5":0,
                "6":0,
                "7":0,
                "8":0,
                },
            "intrusiones":{
                "0":0,
                "1":0,
                "2":0,
                "3":0,
                "4":0,
                "5":0,
                "6":0,
                "7":0,
                "8":0,
                },
            "confab":{
                "0":0,
                "1":0,
                "2":0,
                "3":0,
                "4":0,
                "5":0,
                "6":0,
                "7":0,
                "8":0
                },
            "repeticiones":{
                "0":0,
                "1":0,
                "2":0,
                "3":0,
                "4":0,
                "5":0,
                "6":0,
                "7":0,
                "8":0
                },   
            "mainM":[None,None,None,None,None,None,None,None,None],
            "sideM":[None,None,None,None,None,None,None,None,None],
            "extrasL":[None,None,None,None,None,None,None,None,None],
            "repeticionesM":[None,None,None,None,None,None,None,None,None],
            "respuestasM":[None,None,None,None,None,None,None,None,None],  
            "raw_scores":{
                "t1":None,
                "t2":None,
                "t3":None,
                "t4":None,    
                "t5":None,
                "tB":None,
                "t6":None,
                "t7":None,
                "t8":None,
                "total_inmediato":None,
                },
            "z_scores":{
                "t1":None,
                "t2":None,
                "t3":None,
                "t4":None,    
                "t5":None,
                "tB":None,
                "t6":None,
                "t7":None,
                "t8":None,
                "total_inmediato":None,
                }
            }
        
        #set_index trae la lista de indices que se van a usar para buscar dentro de las normas los valores que le corresponden al sujeto
        index=set_index(normas,session["educacion"],session["sexo"],session["edad"])
        
        #get normas trae las normas del sujeto
        session["normas_sujeto"]=set_norms(normas,session["puntajes"]["raw_scores"],index)
        
        #current_trial es un registro para definir qué trial ya fue completado. El trial como número según la definición inicial de trialnames (linea 14)
        session["current_trial"]=0
        
        #input es un registro para las palabras que se ingresan por trial. Se sobreescribe en cada ejecución del trial
        session["input"]=None

        session["delayed_time"]=None
        session["timeUp_str"]=None

        dicc_session=dict(session)
        codigo_evento=session["cod_evento"]
        session["cod_evento"]=codigo_evento
        codigo_prueba=codigo_evento+"_ravlt"
        session["cod_prueba"]=codigo_prueba
        dicc_session["cod_prueba"]=codigo_prueba
        dicc_session["parrafo"]=""
        dicc_session["prueba"]="ravlt"
        insert_doc(dicc_session)
        relacionar(codigo_evento, codigo_prueba)

        return redirect(url_for("ravlt_www"))
    else:
        return redirect(url_for("ravlt_config_www"))

@app.route("/enps/ravlt/recover/<cod_prueba>", methods=["GET","POST"])
def ravlt_recover_www(cod_prueba):
    datos_prueba=get_prueba(cod_prueba)

    #define qué lista se va a usar entre principal o alternativa
    session["listaA"]=datos_prueba["listaA"]
    session["listaB"]=datos_prueba["listaB"]
    session["listaRec"]=datos_prueba["listaRec"]
    #se inician los diccionarios de sesión para almacenar los puntajes
    #targets, intrusiones, confab y repeticiones parten de 0. 
    #las matrices parten con una entrada por trial con valor None
    #raw_scores parten de 0
    #z_scores parten de con valor None
    session["puntajes"]=datos_prueba["puntajes"]

    #get normas trae las normas del sujeto
    session["normas_sujeto"]=datos_prueba["normas_sujeto"]
    
    #current_trial es un registro para definir qué trial ya fue completado. El trial como número según la definición inicial de trialnames (linea 14)
    session["current_trial"]=datos_prueba["current_trial"]
    
    #input es un registro para las palabras que se ingresan por trial. Se sobreescribe en cada ejecución del trial
    session["input"]=datos_prueba["input"]

    session["delayed_time"]=datos_prueba["delayed_time"]
    session["timeUp_str"]=datos_prueba["timeUp_str"]

    dicc_session=dict(session)
    codigo_evento=datos_prueba["cod_evento"]
    session["cod_evento"]=codigo_evento
    codigo_prueba=datos_prueba["cod_prueba"]
    session["cod_prueba"]=codigo_prueba
    dicc_session["cod_prueba"]=codigo_prueba
    parrafo=datos_prueba["parrafo"]
    dicc_session["parrafo"]=parrafo
    prueba=datos_prueba["prueba"]
    dicc_session["prueba"]=prueba

    return redirect(url_for("ravlt_www"))

@app.route("/enps/ravlt/trial/<string:trial_name>", methods=["GET","POST"])
def ravlt_t_www(trial_name):

    save_last()
    trialnames=session["ravlt_tnames"]
    #recibe (trial_name) y define el número de trial (trial_num) y cuál será el próximo trial con el que continúa
    short_name=trial_name[1]
    for k,v in trialnames.items():
        if v==trial_name:
            trial_num=int(k)
    session["current_trial"]=trial_num
    next_num=int(trial_num)+1
    if trial_num<8:
        next_name=trialnames[str(next_num)]
    else:
        next_name=None

    #cambia la lista target si se trata del trial_num 6 (trialB)
    if trial_num==6:
        listaA=session["listaB"]
        listaB=session["listaA"]
    else:
        listaA=session["listaA"]
        listaB=session["listaB"]
    
    #registra en sesión el trial previo
    normas_sujeto=session["normas_sujeto"]
    registrarTrial(listaA,listaB,trial_num,normas_sujeto)

    #variable para definir tiempo de toma
    timeUp_str=session["timeUp_str"]

    #variables necesarias para mostrar puntajes en pantalla
    raw_scores=session["puntajes"]["raw_scores"]
    z_scores=session["puntajes"]["z_scores"]
    any_score=any(raw_scores.values())
    
    answer=session["puntajes"]["respuestasM"][trial_num]
    try:
        answer=",".join(answer)
    except:
        answer=""
    
    registro=session["puntajes"]

    codigo=session["cod_prueba"]
    checkbox_dict=get_data(codigo,"puntajes.respuestasM")
    checkbox_list=checkbox_dict["puntajes"]["respuestasM"][8]
    if checkbox_list==None:
        checkbox_list=[]

    return render_template(
        "ravlt_trial.html", 
        short_name=short_name, 
        next_name=next_name,
        lista_rec=session["listaRec"],
        timeUp=timeUp_str,
        trial_num=trial_num,
        raw_scores=raw_scores,
        z_scores=z_scores,
        any_score=any_score,
        registro=registro,
        listaA=listaA,
        listaB=listaB,
        mainM=registro["mainM"],
        answer=answer,
        checkbox_list=checkbox_list
        )

@app.route("/enps/ravlt/last", methods=["GET","POST"])
def ravlt_last_www():
    
    edad=int(session["edad"])
    sexo=session["sexo"]
    nombre=session["nombre"]
    apellido=session["apellido"]
    educacion=session["educacion"]
    trial_num=session["current_trial"]
    listaA=session["listaA"]
    listaB=session["listaB"]
    
    normas_sujeto=session["normas_sujeto"]
    registrarTrial(listaA,listaB,trial_num,normas_sujeto,True)

    return redirect(url_for("ravlt_www"))

@app.route("/enps/ravlt", methods=["GET","POST"])
def ravlt_www():
    
    save_last()    
    
    edad=int(session["edad"])
    sexo=session["sexo"]
    nombre=session["nombre"]
    apellido=session["apellido"]
    educacion=session["educacion"]
    trial_num=session["current_trial"]
    listaA=session["listaA"]
    listaB=session["listaB"]

    #variable para definir tiempo de toma
    timeUp_str=session["timeUp_str"]

    #variables necesarias para mostrar puntajes en pantalla
    raw_scores=session["puntajes"]["raw_scores"]
    z_scores=session["puntajes"]["z_scores"]
    any_score=any(raw_scores.values())

    registro=session["puntajes"]

    try:
        p_ravlt=P_RAVLT(edad, sexo, nombre, apellido, registro)
        parrafo=p_ravlt.redactar()
        update_value(session["cod_prueba"], "parrafo", parrafo)
    except:
        parrafo=""

    return render_template(
        "ravlt.html",
        nombre=nombre,
        apellido=apellido, 
        edad=edad, 
        sexo=sexo, 
        educacion=educacion,
        trial_num=trial_num,
        timeUp=timeUp_str,
        raw_scores=raw_scores,
        z_scores=z_scores,
        any_score=any_score,
        registro=registro,
        listaA=listaA,
        mainM=registro["mainM"],
        parrafo=parrafo,
        cod_evento=session["cod_evento"]
        )


if __name__ == '__main__':
  app.run()

