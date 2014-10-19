from openmdao.main.api import Component, convert_units
from openmdao.lib.datatypes.api import Float, Int, Enum
import math

class Parasitic_drag(Component):
	 """Generating Cd_p (parasitic drag coefficient)"""

	 # Inputs

	 

	 Len_fuse = Float(40, iotype='in', units='inch', desc='Fuselage length (inches)')

	 Wid_fuse = Float(8, iotype='in', units='inch', desc='Fuselage width (inches)')

	 Hgt_fuse = Float(10, iotype='in', units='inch', desc='Fuselage height (inches)')
	 
	 S_wing = Float(12, iotype='in', units='ft**2', desc='Wing area')

	 c_wr = Float(19, iotype='in', units='inch', desc='Wing root chord (inches)')


	 c_ht = Float(6, iotype='in', units='inch', desc='horizontal tail chord (inches)')

	 c_vt = Float(6, iotype='in', units='inch', desc='vertical tail chord  (inches)')
		 
	 Airfoil_t_over_c_wing = Float(0.123, iotype='in', desc='wing airfoil t/c ratio')

	 Airfoil_t_over_c_tail = Float(0.123, iotype='in', desc='tail airfoil t/c ratio')

	 S_ht = Float(2, iotype='in', units='ft**2', desc='horizontal tail area')

	 S_vt = Float(0.7, iotype='in', units='ft**2', desc='vertical tail area')
	
	 
	 # Outputs

	 Cd_p = Float(iotype='out', desc='Parasitic drag coefficient')
	
	 

	 def execute(self):
	
	    Velocity = 35.0 #assume 35ft/s
	    Len_fuse = self.Len_fuse
	    Wid_fuse = self.Wid_fuse
	    Hgt_fuse = self.Hgt_fuse
	    S_ref = self.S_wing   # reference area = wing area for small twist & dihedral
	    c_wr = self.c_wr
	    c_ht = self.c_ht
	    c_vt = self.c_vt
	    Airfoil_t_over_c_wing = self.Airfoil_t_over_c_wing
	    Airfoil_t_over_c_tail = self.Airfoil_t_over_c_tail
	
		# Wetted surfaces
	    Swet_wing = self.S_wing*2.0*(1+0.2*Airfoil_t_over_c_wing) # wetted area for wing
	    Swet_ht = self.S_ht*2.0*(1+0.2*Airfoil_t_over_c_tail)
	    Swet_vt = self.S_vt*2.0*(1+0.2*Airfoil_t_over_c_tail)
	    Swet_fuse = Len_fuse * (Wid_fuse + Hgt_fuse)*2  # in**3
	    Swet_fuse = convert_units(Swet_fuse, 'inch**3', 'ft**3')
        


		# form factors
	    k_wing = 1 + 2*1.1*(Airfoil_t_over_c_wing) + 1.1**2*(Airfoil_t_over_c_wing)**2*(1+5)/2
	    k_tail = 1 + 2*1.1*(Airfoil_t_over_c_tail) + 1.1**2*(Airfoil_t_over_c_tail)**2*(1+5)/2
	    d = (Wid_fuse**2+Hgt_fuse**2)**0.5/Len_fuse
	    D = (1-d**2)**0.5
	    a = 2*d**2/(D**3*(math.atanh(D)-D))
	    k_fuse = (1 + 2.3*(a/(2-a)))**2



		# skin friction coefficient
	    cf_fuse = 1.328/((Len_fuse/12)*Velocity/(1.58*10**-4))**.5
	    cf_w = 1.328/((c_wr/12)*Velocity/(1.58*10**-4))**.5
	    cf_ht = 1.328/((c_ht/12)*Velocity/(1.58*10**-4))**.5
	    cf_vt = 1.328/((c_vt/12)*Velocity/(1.58*10**-4))**.5

	
	    self.Cd_p = (k_wing*cf_w*Swet_wing+k_fuse*cf_fuse*Swet_fuse+k_tail*cf_ht*Swet_ht+k_tail*cf_vt*Swet_vt)/S_ref


	    print 'cdp', self.Cd_p	









	 """def list_deriv_vars(self):

	    return ('S_wing','S_ht','S_vt'),('Cd_p')



	 def provideJ(self):

	    V = self.V
	    Len_fuse = self.Len_fuse
	    Wid_fuse = self.Wid_fuse
	    Hgt_fuse = self.Hgt_fuse
	    S_ref = self.S_wing   # reference area = wing area for small twist & dihedral
	    c_wr = self.c_wr
	    c_ht = self.c_ht
	    c_vt = self.c_vt
	    Airfoil_t_over_c_wing = self.Airfoil_t_over_c_wing
	    Airfoil_t_over_c_tail = self.Airfoil_t_over_c_tail
	    Swet_wing = self.S_wing*2.0*(1+0.2*Airfoil_t_over_c_wing) # wetted area for wing
	    Swet_ht = self.S_ht*2.0*(1+0.2*Airfoil_t_over_c_tail)
            



	    dCdp_dSw = -(k_fuse*cf_fuse*Swet_fuse+k_tail*cf_ht*Swet_ht+k_tail*cf_vt*Swet_vt)/(self.S_wing)**2
	    dCdp_dSht = k_tail*cf_ht*2.0*(1+0.2*Airfoil_t_over_c_tail)/S_ref
	    dCdp_dSvt = k_tail*cf_vt*2.0*(1+0.2*Airfoil_t_over_c_tail)/S_ref




	    J = array([[dCdp_dSw, dCdp_dSht, dCdp_dSvt]])

	    return J"""
