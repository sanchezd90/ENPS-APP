import pymongo

diccA={"A":{"B":"C"}}

cluster=pymongo.MongoClient("mongodb+srv://sanchezd90:dbuser-L6H6@cluster0.wwnbb.mongodb.net/<ENPS>?retryWrites=true&w=majority")
db=cluster["ENPS"]

def get_data(codigo,key):
    mycol=db["evsApp"]
    myquery = { "codigo": codigo }
    field={"_id":0, key:1}
    q=mycol.find(myquery,field)
    q=q[0]
    return q

q=get_data("2224_1617148483","puntajes.respuestasM")
q=q["puntajes"]["respuestasM"][8]
print(q)

j=[]
for x in q:
    x='"'+x+'"'
    j.append(x)

print(j)
