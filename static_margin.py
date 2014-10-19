from openmdao.main.api import Component, convert_units
from openmdao.lib.datatypes.api import Float, Int, Enum
from math import pi, sqrt


class Static_margin(Component):
		""" Generating the S.M. value  (rectangular wing)"""
		# Inputs
		AR_w = Float(5, iotype='in', desc='wing aspect ratio')
		AR_ht = Float(5, iotype='in', desc='horizontal tail aspect ratio')
		x_wLE = Float(1, iotype='in', units='ft', desc='x-coordinate of wing leading edge')
		x_cg = Float(2, iotype='in', units='ft', desc='x-coordinate of cg')
		x_tLE = Float(4, iotype='in', units='ft', desc='x-coordinate of tail leading edge')
		c_w = Float(1, iotype='in', units='ft', desc='wing chord (ft)')
		c_ht = Float(0.5, iotype='in', units='ft', desc='horizontal tail chord (ft)')
		S_wing = Float(12, iotype='in', units='ft**2', desc='Wing area')
		S_ht = Float(2, iotype='in', units='ft**2', desc='horizontal tail area')
		Len_fuse = Float(3.33, iotype='in', units='ft', desc='Fuselage length (inches)')
		Wid_fuse = Float(0.666, iotype='in', units='ft', desc='Fuselage width (inches)')
		
		
	# Output
		SM = Float(iotype='out', desc='static margin (chord %)')
		
		
		def execute(self):
	

			AR_w = self.AR_w
			AR_ht = self.AR_ht
			S_wing = self.S_wing
			S_ht = self.S_ht
			x_wLE = self.x_wLE
			Len_fuse = self.Len_fuse
			Wid_fuse = self.Wid_fuse
			x_cg = self.x_cg
			x_tLE = self.x_tLE
			c_w = self.c_w
			c_ht = self.c_ht
	
	
	
			C_L_alpha_w = 2*pi*AR_w/(2+sqrt((AR_w/0.97)**2+4))
			C_L_alpha_ht0 = 2*pi*AR_ht/(2+sqrt((AR_ht/0.97)**2+4))
			C_L_alpha_ht = C_L_alpha_ht0*(1-(2*C_L_alpha_w/pi/AR_w))*0.95
	
			postition_025chord = (x_wLE+0.25*c_w)/Len_fuse 
		
			
			k_f = 1.5012*postition_025chord**2 + .538*postition_025chord+.0331
			
		
			self.SM = -(x_cg-(x_wLE+c_w*0.25))/c_w + (x_tLE+c_ht*0.25-x_cg)/c_w*(S_ht/S_wing)*(C_L_alpha_ht/C_L_alpha_w) - (k_f*Wid_fuse**2*Len_fuse)/(S_wing*c_w*C_L_alpha_w)



			print 'SM', self.SM
		
		