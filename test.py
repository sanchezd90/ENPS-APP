import pymongo

diccA={"A":"a","B":"b"}

cluster=pymongo.MongoClient("mongodb+srv://sanchezd90:dbuser-L6H6@cluster0.wwnbb.mongodb.net/<ENPS>?retryWrites=true&w=majority")
db=cluster["ENPS"]
mycol=db["evsApp"]
myquery = { "dni": "123" }
newvalues={ "$set": { "puntajes": diccA } }
mycol.update_one(myquery, newvalues)

