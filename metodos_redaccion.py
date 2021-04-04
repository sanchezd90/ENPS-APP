class Parrafo():
	def __init__(self,edad,sexo,nombre,apellido):
		self.edad=edad
		if sexo==0:
			self.t_El="El paciente "
			self.t_el="el paciente "
			self.t_del="del paciente "
			t_El_Sr='El Sr. '+apellido+' '
			t_el_Sr='el Sr. '+apellido+' '
			t_del_Sr='del Sr. '+apellido+' '
		else:
			self.t_El='La paciente '
			self.t_el='la paciente '
			self.t_del='de la paciente '
			t_El_Sr='La Sra. '+apellido+' '
			t_el_Sr='la Sra. '+apellido+' '
			t_del_Sr='de la Sra. '+apellido+' '
		if edad <30:
			self.ref_init=nombre+' '
			self.ref_mid=nombre+' '
			self.ref_de="de "+nombre+' '
		else:
			self.ref_init=t_El_Sr
			self.ref_mid=t_el_Sr
			self.ref_de=t_del_Sr
			
	def rendimiento_z(self,z):
		out=None
		if z > 2:
			out='alto '
		elif z> 1:
			out='normal-alto '
		elif z> -1:
			out='normal '
		elif z>-2:
			out='bajo '
		else:
			out="deficitario "
		return out
			
	def valores_z(self,z):
		out=None
		if z > 2:
			out='altos '
		elif z> 1:
			out='normales '
		elif z> -1:
			out='normales '
		elif z>-2:
			out='bajos '
		else:
			out="deficitarios "
		return out
		
	def rendimiento_esc(self,z):
		out=None
		if z > 16:
			out='alto '
		elif z> 13:
			out='normal-alto '
		elif z> 7:
			out='normal '
		elif z>4:
			out='bajo '
		else:
			out="deficitario "
		return out
				
	def valores_esc(self,z):
		out=None
		if z > 16:
			out='altos '
		elif z> 13:
			out='normales '
		elif z> 7:
			out='normales '
		elif z>4:
			out='bajos '
		else:
			out="deficitarios "
		return out
		
	def rendimiento_est(self,z):
		out=None
		if z > 130:
			out='alto '
		elif z> 115:
			out='normal-alto '
		elif z> 85:
			out='normal '
		elif z>70:
			out='bajo '
		else:
			out="deficitario "
		return out
			
	def valores_est(self,z):
		out=None
		if z > 130:
			out='altos '
		elif z> 115:
			out='normales '
		elif z> 85:
			out='normales '
		elif z>-70:
			out='bajos '
		else:
			out="deficitarios "
		return out
	
	def concatenar(self, lista):
		out=""
		if len(lista) <= 1:
			out=lista
		elif len(lista) == 2:
			out=lista[0]+' y '+lista[1]
		else:
			for x in range(0,len(lista)-2):
				out=out+lista[x]+', '
			out=out+lista[-2]+' y '+lista[-1]
		return out
			
class P_RAVLT(Parrafo):
	def __init__(self,edad,sexo,nombre,apellido,t1,reci,prim,curva,inm,tb,t6,dif,dif_r,rec,rec_r,repe,conf):
		super().__init__(edad,sexo,nombre,apellido)
		self.t1=t1
		self.t1_valores=self.valores_z(t1)
		self.reci=reci
		self.prim=prim
		self.curva=curva
		self.inm=inm
		self.tb=tb
		self.tb_valores=self.valores_z(tb)
		self.t6=t6
		self.dif=dif
		self.dif_r=dif_r
		self.dif_valores=self.valores_z(dif)
		self.max=max(curva)
		self.rec=rec
		self.rec_r=rec_r
		self.rec_valores=self.valores_z(rec)
		self.repe=repe
		self.conf=conf
		
		if reci==True and prim==True:
			self.int_recprim="Presentó un efecto de primacía y de recencia, logrando evocar las palabras iniciales y finales de la lista"
		elif reci==False and prim==True:
			self.int_recprim="Presentó un efecto de primacía aunque no así de recencia, sin lograr evocar las palabras finales de la lista"
		elif reci==True and prim==False:
			self.int_recprim="Presentó un efecto de recencia aunque no así de primacía, sin lograr evocar las palabras iniciales de la lista"
		else:
			self.int_recprim="No presentó un efecto de primacía ni de recencia, sin lograr evocar las palabras iniciales y finales de la lista"
			
		if self.inm>-1:
			self.apren="retuvo suficiente información adicional, "
		else:
			self.apren="no retuvo suficiente informacional adicional, "
		
		if self.curva[4]>self.curva[2]>self.curva[0]:
			self.int_curva="ascendente"
		else:
			self.int_curva="fluctuante"
			
		if self.inm<-1 and self.int_curva=="ascendente" or self.inm>=-1 and self.int_curva !="ascendente" :
			self.sal_curva="aunque "
		else:
			self.sal_curva=""
		
		if self.tb<self.t1 and (self.t1-self.tb)>1:
			self.pro='Se observó labilidad a la interferencia de material previamente aprendido en la generación de nuevos aprendizajes.'
		else:
			self.pro=''
			
		if self.t6<self.max and self.max-self.t6>2:
			self.retro="Se observó labilidad a la interferencia de nueva información en la consolidación de información previamente adquirida."
		else:
			self.retro=""
			
		if self.rec>self.dif and self.rec-self.dif>1:
			self.benef="obteniendo un beneficio de las opciones múltiples"
		else:
			self.benef="sin obtener un beneficio de las opciones múltiples"
		
		if self.rec<-1 and self.benef[0]=="o":
			self.sal_benef="aunque "
		else:
			self.sal_benef=""
	
		if self.dif_r<self.max:
			self.t_max=" "+str(self.max)
		else:
			self.t_max=""
		
		if self.repe>5 and self.conf>5:
			self.t_repconf="Cabe destacar que se observó una gran cantidad de repeticiones y confabulaciones a lo largo de la prueba."
		elif self.repe>5 and self.conf<5:
			self.t_repconf="Cabe destacar que se observó una gran cantidad de repeticiones a lo largo de la prueba."
		elif self.repe<5 and self.conf>5:
			self.t_repconf="Cabe destacar que se observó una gran cantidad de confabulaciones a lo largo de la prueba."
		else:
			self.repconf=""
			
	def redactar(self):
		out=f'''{self.t_El}presentó valores {self.t1_valores}en el recuerdo de una lista de 15 palabras. {self.int_recprim}. Con la exposición repetida al material {self.t_el}{self.apren}{self.sal_curva}presentando una curva de aprendizaje {self.int_curva}. Su performance en el aprendizaje de una lista distractora presentó valores {self.tb_valores}{self.pro}{self.retro}. En cuanto a la habilidad del paciente para evocar a largo plazo la información inicialmente presentada, presentó valores {self.dif_valores}, logrando evocar {self.dif_r} de las{self.t_max} palabras inicialmente aprendidas. En la fase de reconocimiento {self.t_el}obtuvo valores {self.rec_valores}, {self.benef}, {self.sal_benef}recuperando {self.rec_r} de las 15 palabras inicialmente presentadas. {self.t_repconf}'''
		out=out.replace(" . ",". ").replace(" , ",", ")
		return out
		

p=P_RAVLT(30,0,'Daniel','Sanchez',-2.5,False,False,[1,2,3,4,5],-1.5,0.5,3,1.5,12,-3,13,10,15)

print(p.redactar())