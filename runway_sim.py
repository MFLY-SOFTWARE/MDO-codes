from openmdao.main.api import Component, convert_units
from openmdao.lib.datatypes.api import Float, Int, Enum
from rk4 import RK4
import math
from math import pi, sin, sqrt
import numpy
from CLCDi import CLCDiSolver

class Runway_sim(Component):
	""" Get Lift """


	# Inputs
	
	Cd_p = Float(0.0088, iotype='in', desc='Parasitic drag coefficient')
	x_cg = Float(1,iotype='in', units='ft', desc='x-coordinate of c.g.')
	W_0 = Float(50, iotype='in', units='lb', desc='Total weight (pounds)')
	airDens = Float(2.329E-3, iotype='in', units='slug/ft**3', desc='density of air')
	mu_k = Float(0.035, iotype='in', desc='wheel friction coefficient')		# wheel friction coefficient
	S_wing = Float(14.07, iotype='in', units='ft**2', desc='Wing area')
	h_wing = Float(10.5, iotype='in', units='inch', decs='height of wing')
	x_wLE = Float(1, iotype='in', units='ft', desc='x-coordinate of wing leading edge')
	b_w = Float(106.05, iotype='in', units='inch', desc='wingspan (inches)')
	c_w = Float(1, iotype='in', units='ft', desc='wing chord (ft)')
	Cm_w = Float(-0.23, iotype='in', desc='Wing moment coefficient')
	x_tLE = Float(4, iotype='in', units='ft', desc='x-coordinate of tail leading edge')
	c_ht = Float(0.5, iotype='in', units='ft', desc='horizontal tail chord (ft)')
	AR_w = Float(5.0, iotype='in', desc='wing aspect ratio')


	# Outputs
	
	Lift_takeoff = Float(iotype='out', units='lb')
	V_takeoff = Float(iotype='out', units='ft/s')
	dist = Float(iotype='out', unit='ft')
	K = Float(iotype='out')
	CL = Float(iotype='out')

	def execute(self):
		airDens = self.airDens 
		
		S_ref = self.S_wing
		Cd_p = self.Cd_p
		
		mu_k = self.mu_k
		h_wing = self.h_wing
		b_w = self.b_w
		c_w = self.c_w
		
		Cm_w = self.Cm_w
		x_wLE = self.x_wLE
		x_tLE = self.x_tLE
		c_ht = self.c_ht
		
		
		

		
		
		x_cg = self.x_cg

		W_0 = self.W_0 



		self.M=M = W_0 / 32.1740  # total mass (slug)

		CLCDi = CLCDiSolver()
		CLCDi.AR = self.AR_w
		CLCDi.a_inf = 3.5
		CLCDi.run()
		CL = CLCDi.CL
		K = CLCDi.K
		K_eff = (33*(h_wing/b_w)**1.5)/(1+33*(h_wing/b_w)**1.5) * K
		

		Lift_w = 0.00
		Lift_t = 0.00


		# f = dE/dx
		f = lambda E: (-0.00082*(2*E/M)+0.00073*sqrt(2*E/M)+7.2) - 0.5*airDens*(2*E/M)*S_ref*(Cd_p+K_eff*CL**2) - mu_k*(W_0-(Lift_w+Lift_t))

		dE = RK4(f)    # put dE/dx as the argument of RK4

		x, E, dx = 0.0, 0.0, 0.1	#step-size of x = 0.1 ft

		
		while x <=  180.0 and W_0*1.05 > (Lift_w+Lift_t):
			x , E = x+dx , E + dE(E,dx)
			V = sqrt(2*E/M)
			Moment_w = 0.5*airDens*V**2*c_w*S_ref*Cm_w
			Lift_w = 0.5*airDens*V**2*S_ref*CL
			Lift_t = (Moment_w  -  Lift_w*(x_wLE+0.25*c_w - x_cg))/(x_tLE+0.25*c_ht - x_cg)
			

		CLCDi.a_inf = 9.0
		CLCDi.run()
		self.CL = CL = CLCDi.CL
		self.K = K = CLCDi.K
		K_eff = (33*(h_wing/b_w)**1.5)/(1+33*(h_wing/b_w)**1.5) * K	


		while  x <=190.0 and W_0*1.05 > (Lift_w+Lift_t):
			x , E = x+dx , E + dE(E,dx)
			V = sqrt(2*E/M)
			Moment_w = 0.5*airDens*V**2*c_w*S_ref*Cm_w
			Lift_w = 0.5*airDens*V**2*S_ref*CL
			Lift_t = (Moment_w  -  Lift_w*(x_wLE+0.25*c_w - x_cg))/(x_tLE+0.25*c_ht - x_cg)


		self.E_takeoff =  E
		self.dist = x
		self.V_takeoff = V
		self.Lift_takeoff_w = Lift_w
		self.Moment_w = Moment_w 
		self.Lift_takeoff_t = Lift_t 

		self.Lift_takeoff = self.Lift_takeoff_w + self.Lift_takeoff_t
		

	

	
		print 'net Lift', self.Lift_takeoff
		print 'V_takeoff', self.V_takeoff
		print 'Lift_takeoff_w', self.Lift_takeoff_w
		print 'Lift_takeoff_t', self.Lift_takeoff_t
		print 'Distance', x
		print 'WingMoment', Moment_w
	
