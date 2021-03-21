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
        #define qué lista se va a usar entre principal o alternativa
        if request.form["lista"]=="0":
            session["listaA"]=lista1A
            session["listaB"]=lista1B
        else:
            session["listaA"]=lista2A
            session["listaB"]=lista2B
        #define qué normas se va a usar
        if request.form["normas"]=="0":
            normas=normas_Geffen
        
        #se inician los diccionarios de sesión para almacenar los puntajes
        #targets, intrusiones, confab y repeticiones parten de 0. 
        #las matrices parten con una entrada por trial con valor None
        #raw_scores parten de 0
        #z_scores parten de con valor None
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
        
        #get_index trae la lista de indices que se van a usar para buscar dentro de las normas los valores que le corresponden al sujeto
        index=get_index(normas,session["educacion"],session["sexo"],session["edad"])
        
        #get normas trae las normas del sujeto
        session["normas_sujeto"]=get_normas(normas,session["puntajes"]["raw_scores"],index)
        
        #current_trial es un registro para definir qué trial ya fue completado. El trial como número según la definición inicial de trialnames (linea 14)
        session["current_trial"]=0
        
        #input es un registro para las palabras que se ingresan por trial. Se sobreescribe en cada ejecución del trial
        session["input"]=None

        return redirect(url_for("resumen_www"))
    else:
        return redirect(url_for("config_www"))


@app.route("/<string:trial_name>", methods=["GET","POST"])
def t_www(trial_name):

    #recibe (trial_name) y define el número de trial (trial_num) y cuál será el próximo trial con el que continúa
    if trial_name[0]=="t":
        short_name=trial_name[1]
        for k,v in trialnames.items():
            if v==trial_name:
                trial_num=k
        session["current_trial"]=trial_num
        next_num=int(trial_num)+1
        next_name=trialnames[next_num]

    #la excepción es reconocimiento porque el trial_name que recibe no sigue la lógica "tn" y además su próximo paso es volver a resumen
    else:
        short_name="Reconocimiento"
        trial_num=8
        session["current_trial"]=trial_num
        next_num=None
        next_name="resumen2"
    
    #cambia la lista target si se trata del trial_num 6 (trialB)
    if trial_num==6:
        listaA=session["listaB"]
        listaB=session["listaA"]
    else:
        listaA=session["listaA"]
        listaB=session["listaB"]
    
    normas_sujeto=session["normas_sujeto"]
    registrarTrial(listaA,listaB,trial_num,normas_sujeto)

    #variables para hacer tests. Eliminar al finalizar
    test=session["puntajes"]
    
    return render_template("trial.html", short_name=short_name, next_name=next_name,test=test)

@app.route("/resumen2", methods=["GET","POST"])
def resumen2_www():
    edad=session["edad"]
    sexo=session["sexo"]
    educacion=session["educacion"]
    trial_num=session["current_trial"]
    listaA=session["listaA"]
    listaB=session["listaB"]

    if trial_num==8:
        normas_sujeto=session["normas_sujeto"]
        registrarTrial(listaA,listaB,trial_num,normas_sujeto,True)
  
    test=session["puntajes"]

    return render_template("resumen.html", edad=edad, sexo=sexo, educacion=educacion, test=test)

@app.route("/resumen", methods=["GET","POST"])
def resumen_www():
    edad=session["edad"]
    sexo=session["sexo"]
    educacion=session["educacion"]
    trial_num=session["current_trial"]
    listaA=session["listaA"]
    listaB=session["listaB"]

    test=session["puntajes"]

    return render_template("resumen.html", edad=edad, sexo=sexo, educacion=educacion,test=test)


app.run(host="localhost", port=8080, debug=True)

