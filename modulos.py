import re

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
    8:"Rec",
}

class Revisor():
    def __init__(self,lista1A,lista1B):
        self.lista1A=lista1A
        self.lista1B=lista1B
        self.targets={
            0:{},
            1:{},
            2:{},
            3:{},
            4:{},
            5:{},
            6:{},
            7:{},
            8:{},
            }
        self.intrusiones={
            5:{},
            6:{},
            7:{},
            8:{},
            }
        self.confab={
            0:{},
            1:{},
            2:{},
            3:{},
            4:{},
            5:{},
            6:{},
            7:{},
            8:{}
            } 
        self.mainM=[]
        self.sideM=[]
        self.extrasL=[]   

    #entrada es un string           
    def limpiarEntrada(self,entrada):
        self.entrada=entrada.split(",")
        output=[]
        for palabra in self.entrada:
            palabra = palabra.strip().lower().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
            output.append(palabra)
        return output

    #entrada es una palabra
    def sort(self,entrada,tipo):
        out=[]
        if tipo=="main":    
            for x in entrada:
                if x in self.lista1A:
                    out.append(x)
        elif tipo=="side":
            for x in entrada:
                if x in self.lista1B:
                    out.append(x)
        else:
            for x in entrada:
                if x not in self.lista1A and x not in self.lista1B:
                    out.append(x)
        return out

    #entrada es una string
    def registrarTrial(self,entrada):
        palabras=self.limpiarEntrada(entrada)
        main=self.sort(palabras,"main")
        main_count=[]
        for x in self.lista1A:
            c=main.count(x)
            main_count.append(c)
        side=self.sort(palabras,"side")
        side_count=[]
        for x in self.lista1B:
            c=side.count(x)
            side_count.append(c)
        extras=self.sort(palabras,"extra")
        self.mainM.append(main_count)
        self.sideM.append(side_count)
        self.extrasL.append(extras)

    def puntuarTrial(self,trial):
        aciertos=0
        if trial == 5:
            for x in self.sideM[5]:
                if x:
                    aciertos+=1
        else:
            for x in self.mainM[trial]:
                if x > 0:
                    aciertos+=1  
        self.targets[trial]=aciertos

ejt1=""
ejt2="balde, mesa , loco, luna"
ejt3="balde, mesa , loco, café, tigre, pavo, río, tiza"
ejt4="tambor, mesa, loco, café, tigre, sapo, templo, perro"
ejt5="tambor, café, balde, rio, taza, luna, pie, color, perro"
      

revisor=Revisor(lista1A,lista1B)

revisor.registrarTrial(ejt1)
revisor.registrarTrial(ejt2)
revisor.registrarTrial(ejt3)
revisor.registrarTrial(ejt4)
revisor.registrarTrial(ejt5)
revisor.puntuarTrial(1)
print(revisor.targets[1])









