from openmdao.main.api import Component, convert_units
from openmdao.lib.datatypes.api import Float, Int, Enum
import math
from math import pi, sin
import numpy


class Weight_buildup_rect(Component):
    """ Generating mass & c.g. position of the aircraft (rectangular wing & conventional tail)"""

    # Inputs

    W_payload = Float(0, iotype='in', units='lb', desc='payload weight (pounds)')
	 
    x_cg_payload = Float(8.8,iotype='in', units='inch')


    Len_fuse = Float(40, iotype='in', units='inch', desc='Fuselage length (inches)')
    Wid_fuse = Float(8, iotype='in', units='inch', desc='Fuselage width (inches)')
    Hgt_fuse = Float(10, iotype='in', units='inch', desc='Fuselage height (inches)')
     
    b_w = Float(106, iotype='in', units='inch', desc='Wingspan (inches)')
    c_w = Float(19, iotype='in', units='inch', desc='Wing chord (inches)')
    x_wLE = Float(0, iotype='in', units='inch', desc='x-coordinate of wing leading edge')
    x_tLE = Float(24, iotype='in', units='inch', desc='x-coordinate of tail leading edge')
    x_engine_cg = Float(1.2, iotype='in', units='inch', desc='x-coordinate of engine c.g.')
    c_ht = Float(10, iotype='in', units='inch', desc='horizontal tail chord (inches)')
    c_vt = Float(5, iotype='in', units='inch', desc='vertical tail chord (inches)')
    b_ht = Float(30, iotype='in', units='inch', desc='horizontal tail span (inches)')
    b_vt = Float(12, iotype='in', units='inch', desc='vertical tail span (inches)')
	 
    S_wing = Float(12, iotype='in', units='ft**2', desc='Wing area')
    S_ht = Float(2, iotype='in', units='ft**2', desc='horizontal tail area')
    S_vt = Float(0.7, iotype='in', units='ft**2', desc='vertical tail area')
    Airfoil_t_over_c_wing = Float(0.123, iotype='in', desc='wing airfoil t/c ratio')
    Airfoil_t_over_c_tail = Float(0.123, iotype='in', desc='tail airfoil t/c ratio')
	 
	
    EngWeight = Float(0.88, iotype='in', units='lb')
    BatteryWeight = Float(1.01, iotype='in', units='lb')
    ESCWeight = Float(0.32, iotype='in', units='lb')
    BalsaDens = Float(0.00653, iotype='in', units='lb/inch**3')
    SpruceDens = Float(0.015, iotype='in', units='lb/inch**3')
    BassDens = Float(0.0165, iotype='in', units='lb/inch**3')
    Alum2024Dens = Float(0.1, iotype='in', units='lb/inch**3')
	
	 
    # Outputs

    W_empty = Float(iotype='out', units='lb', desc='Empty weight (pounds)')
    W_0 = Float(iotype='out', units='lb', desc='Total weight (pounds)')
    x_cg_empty = Float(iotype='out', units='inch', desc='x-coordinate of empty c.g.')
    x_cg = Float(iotype='out', units='inch', desc='x-coordinate of c.g.')
    I_y = Float(iotype='out', units='slug*ft**2')
    
     
    def execute(self):
		 
		 NumRibs = 26/8.9375* self.b_w/12
		 Airfoil_t_over_c_wing = self.Airfoil_t_over_c_wing
		 Airfoil_t_over_c_tail = self.Airfoil_t_over_c_tail
		 BalsaDens = self.BalsaDens
		 SpruceDens = self.SpruceDens
		 BassDens = self.BassDens
		 Len_fuse = self.Len_fuse
		 Wid_fuse = self.Wid_fuse
		 Hgt_fuse = self.Hgt_fuse
		 EngWeight = self.EngWeight
		 ESCWeight = self.ESCWeight
		 BatteryWeight = self.BatteryWeight
		 Alum2024Dens = self.Alum2024Dens
		 W_payload = self.W_payload
		 x_cg_payload = self.x_cg_payload
		 x_wLE = self.x_wLE
		 c_w = self.c_w
		 c_ht = self.c_ht
		 c_vt = self.c_vt
		 b_vt = self.b_vt


		 RibArea = Airfoil_t_over_c_wing*(self.c_w)**2   #inch**2
		 RibWeight = BalsaDens*RibArea*.125    #lb
		 
		 FrontWeight = EngWeight + BatteryWeight + ESCWeight
		 FrontCG = float(3)  

		 #FuseVolume = Len_fuse*Wid_fuse*Hgt_fuse #inch**3
		 #FuseWeight = (FuseVolume*BassDens)  #lb
		 FuseWeight = 1.7 
		 FuseCG = Len_fuse / 2  #inch
		 
		 TailBoomLen = self.x_tLE - (self.x_wLE+self.c_w*0.25)   #inch
		 TailBoomVol = TailBoomLen*(pi*(3.0/4.0)**2/4)   #in**3
		 SparLen = self.b_w * 0.25
		 SparVol = SparLen*(pi*(7.0/8.0)**2/4 + pi*(3.0/8.0)**2/4)
		 TailBoomSparAssemWeight = (TailBoomVol +  SparVol  ) * Alum2024Dens #lb
		 TailBoomSparAssemCG = ((TailBoomLen/2+(self.x_wLE+self.c_w*0.25))*TailBoomVol + (self.x_wLE+self.c_w*0.25)*SparLen*(pi*(7.0/8.0)**2/4) + (self.x_wLE+self.c_w*0.66)* SparLen*(pi*(3.0/8.0)**2/4))/(TailBoomVol + SparVol)

		 W_wing = (NumRibs*RibWeight+2*self.b_w*SpruceDens*.5*.25*2+self.b_w*BalsaDens*Airfoil_t_over_c_wing*(self.c_w)*.125)+.1080851064*self.S_wing
		 W_ht = self.S_ht*0.245614035
		 W_vt = self.S_vt*0.245614035
		 x_cg_w = self.x_wLE + 0.35*self.c_w  #inch
		 x_cg_ht = self.x_tLE + (0.35*self.c_ht)
		 x_cg_vt = self.x_tLE + (0.35*self.c_vt)
		 x_cg_t = self.x_tLE + (0.35*self.c_ht*W_ht+0.35*self.c_vt*W_vt)/(W_ht+W_vt)  #inch
		 
		 x_cg_payload = self.x_cg_payload  	#inch


		 self.W_empty = W_wing + W_ht + W_vt + FrontWeight + FuseWeight + TailBoomSparAssemWeight
	     
		 self.x_cg_empty = (FrontWeight*FrontCG + W_wing*x_cg_w + (W_ht+W_vt)*x_cg_t + FuseWeight*FuseCG + TailBoomSparAssemWeight*TailBoomSparAssemCG)/self.W_empty

		 self.W_0 = self.W_empty + self.W_payload

		 self.x_cg = x_cg = (self.W_empty*self.x_cg_empty + self.W_payload*x_cg_payload)/self.W_0





		 print 'W_wing', W_wing
		 print 'W_ht', W_ht
		 print 'W_vt', W_vt
		 print 'TailBoomLen', TailBoomLen
		 print 'TailBoomSparAssemWeight', TailBoomSparAssemWeight
		 print 'TailBoomSparAssemCG', TailBoomSparAssemCG
		 print 'FuseCG', FuseCG
		 print 'Len_fuse', Len_fuse
		 print 'Wid_fuse', Wid_fuse
		 print 'Hgt_fuse', Hgt_fuse
		 print 'W_empty', self.W_empty
		 print 'W_payload', self.W_payload
		 print 'W_0', self.W_0
		 print 'x_cg_w', x_cg_w
		 print 'x_cg_t', x_cg_t
		 print 'x_cg_payload', self.x_cg_payload
		 print 'x_cg', self.x_cg










		 # I_y calculation


		 FrontCG = convert_units(FrontCG, 'inch','ft')
		 FuseCG = convert_units(FuseCG,'inch','ft')
		 x_cg_w = convert_units(x_cg_w,'inch','ft')
		 x_cg_ht = convert_units(x_cg_ht,'inch','ft')
		 x_cg_vt = convert_units(x_cg_vt,'inch','ft')

		 
		 TailBoomLen = convert_units(TailBoomLen,'inch','ft')
		 x_cg_payload = convert_units(x_cg_payload,'inch','ft')
		 x_cg = convert_units(x_cg,'inch','ft')
		 c_w = convert_units(c_w,'inch','ft')
		 c_ht = convert_units(c_ht,'inch','ft')
		 c_vt = convert_units(c_vt,'inch','ft')
		 b_vt = convert_units(b_vt,'inch','ft')




		 # I_y_front
		 I_y_front = (FrontWeight/32.1740)*(FrontCG - x_cg)**2

		 # I_y_fuse
		 I_y_fuse = (1.0/12.0)*(FuseWeight/32.1740)*(Len_fuse**2+Hgt_fuse**2)+(FuseWeight/32.1740)*(FuseCG - x_cg)**2

		 #I_y_wing
		 I_y_wing = (1.0/12.0)*(W_wing/32.1740)*(c_w**2+(Airfoil_t_over_c_wing*c_w*0.5)**2)+(W_wing/32.1740)*(x_cg_w - x_cg)**2

		 #I_y_spar
		 I_y_spar = 0.5*(SparLen*(pi*(7.0/8.0)**2/4)*Alum2024Dens)/32.1740*((7.0/8.0)/12/2)**2 + (SparLen*(pi*(7.0/8.0)**2/4)*Alum2024Dens)/32.1740*((x_wLE+c_w*0.25) - x_cg)**2 + 0.5*(SparLen*(pi*(3.0/8.0)**2/4)*Alum2024Dens)/32.1740*((3.0/8.0)/12/2)**2 + (SparLen*(pi*(3.0/8.0)**2/4)*Alum2024Dens)/32.1740*((x_wLE+c_w*0.66) - x_cg)**2

		 #I_y_tail
		 I_y_tail = (1.0/12.0)*(W_ht/32.1740)*(c_ht**2+(Airfoil_t_over_c_tail*c_ht*0.5)**2)+(W_ht/32.1740)*(x_cg_ht - x_cg)**2 + (1.0/12.0)*(W_vt/32.1740)*(c_vt**2+b_vt**2)+(W_vt/32.1740)*((x_cg_vt - x_cg)**2+(b_vt/2)**2)

		 #I_y_tailboom
		 I_y_tailboom = (1.0/12.0)*(TailBoomVol*Alum2024Dens)/32.1740*(TailBoomLen)**2 + (TailBoomVol*Alum2024Dens)/32.1740*((TailBoomLen/2+(x_wLE+c_w*0.25)) - x_cg)**2






		 self.I_y = I_y = I_y_front + I_y_fuse + I_y_wing + I_y_spar + I_y_tail + I_y_tailboom
		 #self.I_y = I_y = W_payload/32.1740*(x_cg_payload - x_cg)**2 + FrontWeight/32.1740*(FrontCG - x_cg)**2 + W_wing/32.1740*(x_cg_w - x_cg)*2 + (W_ht+W_vt)/32.1740*(x_cg_t - x_cg)**2 + FuseWeight/32.1740*(FuseCG - x_cg)**2 + TailBoomSparAssemWeight/32.1740*(TailBoomSparAssemCG - x_cg)**2

		 print 'I_y', I_y











		

		
