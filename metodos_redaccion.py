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
	def __init__(self,edad,sexo,nombre,apellido,t1,reci,prim,curva,inm,tb,retro,pro,dif,dif_r,rec,rec_r,repe,conf):
		super().__init__(edad,sexo,nombre,apellido)
		self.t1=t1
		self.t1_valores=self.valores_z(t1)
		self.reci=reci
		self.prim=prim
		self.curva=curva
		self.inm=inm
		self.tb=tb
		self.tb_valores=self.valores_z(tb)
		self.retro=retro
		self.pro=pro
		self.dif=dif
		self.dif_r=dif_r
		self.dif_valores=self.valores_z(dif)
		self.max=max(curva)
		self.rec=rec
		self.rec_r=rec_r
		self.rec_valores=self.valores_z(rec)
		self.repe=repe
		self.conf=conf
	def redactar(self):
		out=f'''{self.t_El}presentó valores {self.t1_valores}en el recuerdo de una lista de 15 palabras. INT_RECPRIM. Con la exposición repetida al material, {self.t_el}retuvo INT_CURVA. Su performance en el aprendizaje de una lista distractora presentó valores {self.tb_valores}.INT_INTER. En cuanto a la habilidad del paciente para evocar a largo plazo la información inicialmente presentada, presentó valores {self.dif_valores}, logrando evocar {self.dif_r} de las {self.max} palabras inicialmente aprendidas. En la fase de reconocimiento {self.t_el}obtuvo valores {self.rec_valores},BENEFICIO,recuperando {self.rec_r} de las 15 palabras inicialmente presentadas.'''
		return out
		

p=P_RAVLT(30,0,'Daniel','Sanchez',-2.5,False,False,[1,2,3,4,5],-1.5,0.5,3,4,1.5,12,-3,13,10,15)

print(p.redactar())