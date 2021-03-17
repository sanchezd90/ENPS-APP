from flask import Flask, render_template, redirect, url_for, request, Response, session
from metodos_ravlt import *
import normas

app = Flask(__name__)
app.secret_key="a2S3d4F"

lista1A = ["tambor","cafe","tigre","caja","luna","primo","tiza","moda","pie","balde","pavo","color","planta","casa","rio"]
lista1B = ["mesa","campo","torre","nube","vaso","luz","cañon","boca","tinta","sapo","firma","templo","lado","bote","pez"]
lista2A = ["pasto","fuente","media","auto","papel","pais","tio","raton","cara","rosa","plato","jabon","niño","pera","libro"]
lista2B = ["playa","foca","rey","piano","saco","globo","vino","tierra","gato","frio","leche","menta","barba","mano","cama"]
rec1 = ['forma', 'moda', 'bala', 'sol', 'paz', 'saco', 'lado', 'tipo', 'rojo', 'planta', 'leon', 'voto', 'vaso', 'flor', 'copa', 'rana', 'baile', 'cañon', 'tigre', 'torre', 'mesa', 'modo', 'firma', 'color', 'pez', 'boca', 'pavo', 'cajon', 'nube', 'dado', 'lunes', 'primo', 'hogar', 'balde', 'nariz', 'luz', 'silla', 'pava', 'bote', 'cinta', 'pie', 'caja', 'barco', 'pierna', 'tinta', 'tambor', 'luna', 'vale', 'sapo', 'te', 'rio', 'lluvia', 'paso', 'casa', 'bombo', 'campo', 'tiza', 'templo', 'calor', 'cafe']
rec2 = ['raton', 'fiesta', 'rata', 'barba', 'region', 'jamon', 'niño', 'medio', 'saco', 'chico', 'sierra', 'ruta', 'vino', 'media', 'rey', 'playa', 'texto', 'menta', 'jabon', 'cama', 'tierra', 'rosa', 'cosa', 'piano', 'taco', 'pais', 'fruta', 'plato', 'globo', 'playa', 'mano', 'pato', 'cara', 'auto', 'lio', 'rostro', 'gato', 'pasto', 'papel', 'frio', 'puente', 'libro', 'pelo', 'pera', 'costa', 'foca', 'tio', 'leche', 'ley', 'fuente']
trialnames={
    0:"t1",
    1:"t2",
    2:"t3",
    3:"t4",    
    4:"t5",
    5:"tB",
    6:"t6",
    7:"t7",
    8:"rec",
    }
 

#home para cargar los datos iniciales
@app.route("/", methods=["GET","POST"])
def config_www():
    return render_template("config.html")

@app.route("/set", methods=["GET","POST"])
def set_www():
    if request.method == "POST":
        session["edad"]=request.form["edad"]
        session["educacion"]=request.form["educacion"]
        session["sexo"]=request.form["sexo"]
        if request.form["lista"]=="0":
            session["listaA"]=lista1A
            session["listaB"]=lista1B
        else:
            session["listaA"]=lista2A
            session["listaB"]=lista2B
        if request.form["lista"]=="0":
            normas=normas_Geffen
        session["puntajes"]={
            "targets":{
                0:0,
                1:0,
                2:0,
                3:0,
                4:0,
                5:0,
                6:0,
                7:0,
                8:0,
                },
            "intrusiones":{
                0:0,
                1:0,
                2:0,
                3:0,
                4:0,
                5:0,
                6:0,
                7:0,
                8:0,
                },
            "confab":{
                0:0,
                1:0,
                2:0,
                3:0,
                4:0,
                5:0,
                6:0,
                7:0,
                8:0
                },
            "repeticiones":{
                0:0,
                1:0,
                2:0,
                3:0,
                4:0,
                5:0,
                6:0,
                7:0,
                8:0
                },   
            "mainM":[None,None,None,None,None,None,None,None,None],
            "sideM":[None,None,None,None,None,None,None,None,None],
            "extrasL":[None,None,None,None,None,None,None,None,None],
            "repeticionesM":[None,None,None,None,None,None,None,None,None],  
            "raw_scores":{
                "t1":0,
                "t2":0,
                "t3":0,
                "t4":0,    
                "t5":0,
                "tB":0,
                "t6":0,
                "t7":0,
                "rec":0,
                "total_inmediato":0,
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
                "rec":None,
                "total_inmediato":None,
                }
            }
        index=get_index(normas,session["educacion"],session["sexo"],session["edad"])
        session["normas_sujeto"]=get_normas(normas,session["puntajes"]["raw_scores"],index)
        session["current_trial"]=None
        session["input"]=None
        return redirect(url_for("resumen_www"))
    else:
        return redirect(url_for("config_www"))


@app.route("/<string:trial_name>", methods=["GET","POST"])
def t_www(trial_name):

    if trial_name[0]=="t":
        short_name=trial_name[1]
        for k,v in trialnames.items():
            if v==trial_name:
                trial_num=k
        session["current_trial"]=trial_num
        next_num=int(trial_num)+1
        if trial_num==6:
            next_name="resumen"
        else:
            next_name=trialnames[next_num]
    else:
        short_name="Reconocimiento"
        trial_num=8
        session["current_trial"]=trial_num
        next_num=None
        next_name="resumen"
    
    if trial_num==6:
        listaA=session["listaB"]
        listaB=session["listaA"]
    else:
        listaA=session["listaA"]
        listaB=session["listaB"]
    
    if trial_num==0 or trial_num==7: 
        t_input=None
    else:
        t_input=request.form["input"]
        main_M=session["puntajes"]["mainM"]
        side_M=session["puntajes"]["sideM"]
        extras_L=session["puntajes"]["extrasL"]
        repeticiones_M=session["puntajes"]["repeticionesM"]
        registro_trial=registrarTrial(t_input,listaA,listaB)
        main_M[trial_num-1]=registro_trial[0]
        side_M[trial_num-1]=registro_trial[1]
        extras_L[trial_num-1]=registro_trial[2]
        repeticiones_M[trial_num-1]=registro_trial[3]
        session["puntajes"]["mainM"]=main_M
        session["puntajes"]["sideM"]=side_M
        session["puntajes"]["extrasL"]=extras_L
        session["puntajes"]["repeticionesM"]=repeticiones_M
    return render_template("trial.html", short_name=short_name, next_name=next_name)


@app.route("/resumen", methods=["GET","POST"])
def resumen_www():
    edad=session["edad"]
    sexo=session["sexo"]
    educacion=session["educacion"]
    trial_num=session["current_trial"]
    listaA=session["listaA"]
    listaB=session["listaB"]
    session["input7"]=None
    
    if trial_num==6 or trial_num==8:
        t_input=request.form["input"]
        main_M=session["puntajes"]["mainM"]
        side_M=session["puntajes"]["sideM"]
        extras_L=session["puntajes"]["extrasL"]
        repeticiones_M=session["puntajes"]["repeticionesM"]
        registro_trial=registrarTrial(t_input,listaA,listaB)
        main_M[trial_num]=registro_trial[0]
        side_M[trial_num]=registro_trial[1]
        extras_L[trial_num]=registro_trial[2]
        repeticiones_M[trial_num]=registro_trial[3]
        session["puntajes"]["mainM"]=main_M
        session["puntajes"]["sideM"]=side_M
        session["puntajes"]["extrasL"]=extras_L
        session["puntajes"]["repeticionesM"]=repeticiones_M
        session["input7"]=t_input

    mainM=session["puntajes"]["mainM"]

    return render_template("resumen.html", edad=edad, sexo=sexo, educacion=educacion, mainM=mainM)


app.run(host="localhost", port=8080, debug=True)

