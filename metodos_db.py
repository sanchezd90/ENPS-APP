import pymongo
import re
import os

cluster=os.environ.get("CLUSTER","mongoDB cluster")
db=cluster["ENPS"]

#NORMAS

def get_norms(prueba,autor):
    col=db["normas"]
    query={"autor":autor,"prueba":prueba}
    doc=col.find(query)
    return doc[0]

#EVS APP

def insert_doc(datos):
    col=db["evsApp"]
    doc=datos
    return col.insert_one(doc)

def update_doc(codigo,datos):
    mycol=db["evsApp"]
    myquery = { "cod_prueba": codigo }
    newvalues={ "$set": { "puntajes": datos } }
    mycol.update_one(myquery, newvalues)


def update_value(codigo,key,value):
    mycol=db["evsApp"]
    myquery = { "cod_prueba": codigo }
    newvalues={ "$set": { key: value } }
    mycol.update_one(myquery, newvalues)

def get_data(codigo,key):
    mycol=db["evsApp"]
    myquery = { "cod_prueba": codigo }
    field={"_id":0, key:1}
    q=mycol.find(myquery,field)
    return q[0]

def get_prueba(codigo):
    mycol=db["evsApp"]
    myquery = { "cod_prueba": codigo }
    q=mycol.find(myquery)
    return q[0]

def update_all(key,value):
    mycol=db["evsApp"]
    myquery = {}
    newvalues={ "$set": { key: value } }
    mycol.update_many(myquery, newvalues)

# EVENTOS APP

def update_reportes(codigo,datos):
    mycol=db["eventosApp"]
    myquery = { "cod_evento": codigo }
    newvalues={ "$set": { "reportes": datos } }
    mycol.update_one(myquery, newvalues)


def insert_event(nombre, apellido, dni, edad, educacion, sexo, codigo, fecha, fechaNac):
    col=db["eventosApp"]
    datos={
        "nombre":nombre,
        "apellido":apellido,
        "dni":dni,
        "edad":edad,
        "fechaNac":fechaNac,
        "educacion":educacion,
        "sexo":sexo,
        "cod_evento":codigo,
        "fecha":fecha,
        "pruebas_admin":None,
        "reportes":{}
        }
    doc=datos
    return col.insert_one(doc)

def get_event(codigo):
    mycol=db["eventosApp"]
    myquery = { "cod_evento": codigo }
    q=mycol.find(myquery)
    return q[0]

def get_from_event(cod_evento,key):
    mycol=db["eventosApp"]
    myquery = { "cod_evento": cod_evento }
    field= { "_id":0, key:1}
    q=mycol.find(myquery,field)
    return q[0][key]

def get_all_events():
    mycol=db["eventosApp"]
    out=[]
    for x in mycol.find({}):
        out.append(x)
    return out

def get_by_name(name):
    mycol=db["eventosApp"]
    out=[]
    myquery={ "apellido":  name }
    field={ "_id":0, "nombre":1, "apellido":1, "cod_evento":1, "fecha":1}
    for x in mycol.find(myquery,field):
        out.append(x)
    myquery={ "nombre":  name }
    field={ "_id":0, "nombre":1, "apellido":1, "cod_evento":1, "fecha":1}
    for x in mycol.find(myquery,field):
        if x in out:
            pass
        else:
            out.append(x)
    term="\A"+name
    myquery={ "apellido":  {"$regex": term} }
    field={ "_id":0, "nombre":1, "apellido":1, "cod_evento":1, "fecha":1}
    for x in mycol.find(myquery,field):
        if x in out:
            pass
        else:
            out.append(x)
    myquery={ "nombre":  {"$regex": term} }
    field={ "_id":0, "nombre":1, "apellido":1, "cod_evento":1, "fecha":1}
    for x in mycol.find(myquery,field):
        if x in out:
            pass
        else:
            out.append(x)
    return out


def relacionar(cod_evento,cod_prueba):
    eventos=db["eventosApp"]
    q=eventos.find({ "cod_evento": cod_evento },{"_id":0, "pruebas_admin":1})
    pruebas_admin=q[0]["pruebas_admin"]

    if pruebas_admin==None:
        pruebas_admin=[]

    pruebas_admin.append(cod_prueba)
    newvalues={ "$set": { "pruebas_admin": pruebas_admin } }
    eventos.update_one({ "cod_evento": cod_evento }, newvalues)


def update_all(key,value):
    mycol=db["eventosApp"]
    myquery = {}
    newvalues={ "$set": { key: value } }
    mycol.update_many(myquery, newvalues)

def update_event(cod_evento,key,value):
    mycol=db["eventosApp"]
    myquery = { "cod_evento": cod_evento }
    newvalues={ "$set": { key: value } }
    mycol.update_one(myquery, newvalues)

# APP DATA

def get_test_names():
    mycol=db["appData"]
    myquery = {}
    field={"_id":0, "nombres_pruebas":1}
    q=mycol.find(myquery,field)
    q=q[0]["nombres_pruebas"]
    return q

def get_pruebas_disp():
    mycol=db["appData"]
    q=mycol.find({},{"_id":0, "pruebas_disponibles":1})
    q=q[0]["pruebas_disponibles"]
    return q

def get_appData(prueba):
    mycol=db["appData"]
    q=mycol.find({},{"_id":0, prueba:1})
    q=q[0][prueba]
    return q
