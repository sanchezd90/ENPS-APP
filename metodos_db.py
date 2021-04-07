import pymongo

cluster=pymongo.MongoClient("mongodb+srv://sanchezd90:dbuser-L6H6@cluster0.wwnbb.mongodb.net/<ENPS>?retryWrites=true&w=majority")
db=cluster["ENPS"]

def get_norms(prueba,autor):
    col=db["normas"]
    query={"autor":autor,"prueba":prueba}
    doc=col.find(query)
    return doc[0]

def insert_doc(datos):
    col=db["evsApp"]
    doc=datos
    return col.insert_one(doc)

def update_doc(codigo,datos):
    mycol=db["evsApp"]
    myquery = { "cod_prueba": codigo }
    newvalues={ "$set": { "puntajes": datos } }
    mycol.update_one(myquery, newvalues)

def get_data(codigo,key):
    mycol=db["evsApp"]
    myquery = { "cod_prueba": codigo }
    field={"_id":0, key:1}
    q=mycol.find(myquery,field)
    return q[0]

def insert_event(nombre, apellido, dni, edad, educacion, sexo, codigo, fecha):
    col=db["eventosApp"]
    datos={
        "nombre":nombre,
        "apellido":apellido,
        "dni":dni,
        "edad":edad,
        "educacion":educacion,
        "sexo":sexo,
        "cod_evento":codigo,
        "fecha":fecha,
        "pruebas_admin":None
        }
    doc=datos
    return col.insert_one(doc)

def get_event(codigo):
    mycol=db["eventosApp"]
    myquery = { "cod_evento": codigo }
    q=mycol.find(myquery)
    return q[0]

def get_all_events():
    mycol=db["eventosApp"]
    out=[]
    for x in mycol.find({}):
        out.append(x)
    return out

def get_pruebas_disp():
    mycol=db["appData"]
    q=mycol.find({},{"_id":0, "pruebas_disponibles":1})
    q=q[0]["pruebas_disponibles"]
    return q
