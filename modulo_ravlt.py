from collections import Counter
from normas import normas_Geffen
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
    8:"rec",
}


class Revisor():
    def __init__(self,lista1A,lista1B,edad,sexo,nse,normas):
        #variables con datos de incio del sujeto, normas y prueba
        self.edad=edad
        self.sexo=sexo
        self.nse=nse
        self.normas=normas
        self.lista1A=lista1A
        self.lista1B=lista1B
        
        #variables para puntajes
        self.targets={
            0:0,
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
            6:0,
            7:0,
            8:0,
            }
        self.intrusiones={
            0:0,
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
            6:0,
            7:0,
            8:0,
            }
        self.confab={
            0:0,
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
            6:0,
            7:0,
            8:0
            }
        self.repeticiones={
            0:0,
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
            6:0,
            7:0,
            8:0
        } 
        self.mainM=[]
        self.sideM=[]
        self.extrasL=[]
        self.repeticionesM=[]  
        
        self.raw_scores={
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
        }
        
        self.z_scores={
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

        
        
        #definición de los índices de búsqueda para normas
        for y in self.normas["nse"]:
            if self.normas["nse"][y][0] <= self.nse <= self.normas["nse"][y][1]:
                nse_index=y
        
        sex_index=self.sexo
        
        for x in self.normas["edad"]:
            if self.normas["edad"][x][0] <= self.edad <= self.normas["edad"][x][1]:
                edad_index=x

        #definición de la media y desvío de cada score para el sujeto
        self.normas_sujeto={}
        for x in self.raw_scores:
            self.normas_sujeto[x]=[self.normas["norms"][x][nse_index][0][sex_index][edad_index],self.normas["norms"][x][nse_index][1][sex_index][edad_index]]
            

    #entrada es un string           
    def limpiarEntrada(self,entrada):
        self.entrada=entrada.split(",")
        output=[]
        for palabra in self.entrada:
            palabra = palabra.strip().lower().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
            if len(palabra)>0:
                output.append(palabra)
            else:
                output.append(None)
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

    def convert_scores(self):
        for x in self.raw_scores:
            self.z_scores[x]=(self.raw_scores[x]-self.normas_sujeto[x][0])/self.normas_sujeto[x][1]

    def update_raw(self):
        self.raw_scores={
            "t1":self.targets[0],
            "t2":self.targets[1],
            "t3":self.targets[2],
            "t4":self.targets[3],    
            "t5":self.targets[4],
            "tB":self.targets[5],
            "t6":self.targets[6],
            "t7":self.targets[7],
            "rec":self.targets[8],
            "total_inmediato":self.targets[0]+self.targets[1]+self.targets[2]+self.targets[3]+self.targets[4],
        }

    def puntuarTrial(self):
        trial=len(self.mainM)-1
        aciertos=0
        intrusiones=0
        confabulaciones=0
        reps=sum(self.repeticionesM[trial][0])+sum(self.repeticionesM[trial][1])+self.repeticionesM[trial][2]
        if trial == 5:
            for x in self.sideM[5]:
                if x:
                    aciertos+=1
            for x in self.mainM[5]:
                if x:
                    intrusiones+=1
            for x in self.extrasL[5]:
                if x != None:
                    confabulaciones+=1
        else:
            for x in self.mainM[trial]:
                if x:
                    aciertos+=1
            for x in self.sideM[trial]:
                if x:
                    intrusiones+=1 
            for x in self.extrasL[trial]:
                if x != None:
                    confabulaciones+=1
         
        self.targets[trial]=aciertos
        self.intrusiones[trial]=intrusiones
        self.confab[trial]=confabulaciones
        self.repeticiones[trial]=reps
        self.update_raw()
        self.convert_scores()

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
        extras_dict= dict(Counter(extras))
        repeticiones_main=[]
        for x in main_count:
            if x>1:
                repeticiones_main.append(x-1)
            else:
                repeticiones_main.append(0)
        repeticiones_side=[]
        for x in side_count:
            if x>1:
                repeticiones_side.append(x-1)
            else:
                repeticiones_side.append(0)
        repeticiones_extra=sum(extras_dict.values())-len(extras_dict)
        repeticiones_conj=[repeticiones_main,repeticiones_side,repeticiones_extra]
        self.mainM.append(main_count)
        self.sideM.append(side_count)
        self.extrasL.append(extras)
        self.repeticionesM.append(repeticiones_conj)
        self.puntuarTrial()



ejt0="tigre, tigre, mesa, mesa"
ejt1="balde, mesa , loco, luna"
ejt2="balde, mesa , loco, café, tigre, pavo, loco, tiza"
ejt3="tambor, mesa, loco, café, tigre, sapo, templo, perro"
ejt4="tambor, café, balde, rio, taza, luna, pie, color, perro"
ejt5="balde, mesa , loco, café, tigre, pavo, río, tiza"
      

revisor=Revisor(lista1A,lista1B,30,0,18,normas_Geffen)

revisor.registrarTrial(ejt0)
revisor.registrarTrial(ejt1)
revisor.registrarTrial(ejt2)
revisor.registrarTrial(ejt3)
revisor.registrarTrial(ejt4)
revisor.registrarTrial(ejt5)

print(revisor.z_scores)








