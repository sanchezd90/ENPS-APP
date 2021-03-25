from flask import Flask, render_template, redirect, url_for, request, Response, session
from metodos_ravlt import *
import normas

app = Flask(__name__)
app.secret_key="a2S3d4F"

lista1A = ["tambor","cafe","tigre","caja","luna","primo","tiza","moda","pie","balde","pavo","color","planta","casa","rio"]
lista1B = ["mesa","campo","torre","nube","vaso","luz","cañon","boca","tinta","sapo","firma","templo","lado","bote","pez"]
lista2A = ["pasto","fuente","media","auto","papel","pais","tio","raton","cara","rosa","plato","jabon","niño","pera","libro"]
lista2B = ["playa","foca","rey","piano","saco","globo","vino","tierra","gato","frio","leche","menta","barba","mano","cama"]
#lista de 60 items
rec1 = ("forma", "moda", "bala", "sol", "paz", "saco", "lado", "tipo", "rojo", "planta", "leon", "voto", "vaso", "flor", "copa", "rana", "baile", "cañon", "tigre", "torre", "mesa", "modo", "firma", "color", "pez", "boca", "pavo", "cajon", "nube", "dado", "lunes", "primo", "hogar", "balde", "nariz", "luz", "silla", "pava", "bote", "cinta", "pie", "caja", "barco", "pierna", "tinta", "tambor", "luna", "vale", "sapo", "te", "rio", "lluvia", "paso", "casa", "bombo", "campo", "tiza", "templo", "calor", "cafe")

#lista de 50 items
rec2 = ["raton", "fiesta", "rata", "barba", "region", "jamon", "niño", "medio", "saco", "chico", "sierra", "ruta", "vino", "media", "rey", "playa", "texto", "menta", "jabon", "cama", "tierra", "rosa", "cosa", "piano", "taco", "pais", "fruta", "plato", "globo", "playa", "mano", "pato", "cara", "auto", "lio", "rostro", "gato", "pasto", "papel", "frio", "puente", "libro", "pelo", "pera", "costa", "foca", "tio", "leche", "ley", "fuente"]

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
            session["listaRec"]=rec1
        else:
            session["listaA"]=lista2A
            session["listaB"]=lista2B
            session["listaRec"]=rec2
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
        
        #get_index trae la lista de indices que se van a usar para buscar dentro de las normas los valores que le corresponden al sujeto
        index=get_index(normas,session["educacion"],session["sexo"],session["edad"])
        
        #get normas trae las normas del sujeto
        session["normas_sujeto"]=get_normas(normas,session["puntajes"]["raw_scores"],index)
        
        #current_trial es un registro para definir qué trial ya fue completado. El trial como número según la definición inicial de trialnames (linea 14)
        session["current_trial"]=0
        
        #input es un registro para las palabras que se ingresan por trial. Se sobreescribe en cada ejecución del trial
        session["input"]=None

        session["delayed_time"]=None
        session["timeUp_str"]=None

        return redirect(url_for("resumen_www"))
    else:
        return redirect(url_for("config_www"))

@app.route("/trial/<string:trial_name>", methods=["GET","POST"])
def t_www(trial_name):

    #recibe (trial_name) y define el número de trial (trial_num) y cuál será el próximo trial con el que continúa
    short_name=trial_name[1]
    for k,v in trialnames.items():
        if v==trial_name:
            trial_num=k
    session["current_trial"]=trial_num
    next_num=int(trial_num)+1
    if trial_num<8:
        next_name=trialnames[next_num]
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


    print(trial_num)

    return render_template(
        "trial.html", 
        short_name=short_name, 
        next_name=next_name,
        lista_rec=session["listaRec"],
        timeUp=timeUp_str,
        trial_num=trial_num,
        raw_scores=raw_scores,
        z_scores=z_scores,
        any_score=any_score,
        registro=registro,
        answer=answer
        )

@app.route("/last", methods=["GET","POST"])
def last_www():
    
    edad=session["edad"]
    sexo=session["sexo"]
    educacion=session["educacion"]
    trial_num=session["current_trial"]
    listaA=session["listaA"]
    listaB=session["listaB"]
    
    normas_sujeto=session["normas_sujeto"]
    registrarTrial(listaA,listaB,trial_num,normas_sujeto,True)

    timeUp_str=session["timeUp_str"]

    raw_scores=session["puntajes"]["raw_scores"]
    z_scores=session["puntajes"]["z_scores"]
    any_score=any(raw_scores.values())

    registro=session["puntajes"]

    return render_template(
        "resumen.html", 
        edad=edad, 
        sexo=sexo, 
        educacion=educacion,
        trial_num=trial_num,
        timeUp=timeUp_str,
        raw_scores=raw_scores,
        z_scores=z_scores,
        any_score=any_score,
        registro=registro
        )


@app.route("/resumen", methods=["GET","POST"])
def resumen_www():
    edad=session["edad"]
    sexo=session["sexo"]
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

    return render_template(
        "resumen.html", 
        edad=edad, 
        sexo=sexo, 
        educacion=educacion,
        trial_num=trial_num,
        timeUp=timeUp_str,
        raw_scores=raw_scores,
        z_scores=z_scores,
        any_score=any_score,
        registro=registro
        )


app.run(host="localhost", port=8080, debug=True)

