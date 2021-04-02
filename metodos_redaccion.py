class Parrafo():
	def __init__(self,edad,sexo,nombre,apellido):
		self.edad=edad
		if sexo==0:
			t_El="El paciente "
			t_el="el paciente "
			t_del="del paciente "
			t_El_Sr='El Sr. '+apellido+' '
			t_el_Sr='el Sr. '+apellido+' '
			t_del_Sr='del Sr. '+apellido+' '
		else:
			t_El='La paciente '
			t_el='la paciente '
			t_del='de la paciente '
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
		
		
p=Parrafo(30,0,"Daniel","Sanchez")
		

		
	