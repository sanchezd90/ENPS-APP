import pymongo

cluster=pymongo.MongoClient("mongodb+srv://sanchezd90:dbuser-L6H6@cluster0.wwnbb.mongodb.net/<ENPS>?retryWrites=true&w=majority")
db=cluster["ENPS"]

def get_norms(prueba,autor):
    col=db["normas"]
    query={"autor":autor,"prueba":prueba}
    doc=col.find(query)
    return doc[0]



