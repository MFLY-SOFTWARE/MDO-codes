from openmdao.main.api import Component, Assembly, convert_units
from openmdao.lib.datatypes.api import Float, Int, Enum , Str
from openmdao.lib.drivers.api import SLSQPdriver, FixedPointIterator, CONMINdriver, COBYLAdriver, NEWSUMTdriver
import math
from math import pi, sin, sqrt
import numpy
from configuration_rect import Configuration_rect
from weight_buildup_rect import Weight_buildup_rect
from static_margin import Static_margin
#from CLCDi import CLCDiSolver
from parasitic_drag import Parasitic_drag
from runway_sim import Runway_sim
#from shortperiodapprox import ShortPeriodApprox
from genplot import GenPlot
from openmdao.lib.casehandlers.api import JSONCaseRecorder, CSVCaseRecorder
from exec_avl import exec2
from avl_geometry_gen import AVLGeo
from avl_geometry_surface import AVLSection, AVLControlSurface, AVLSurface
from avl_surfaces_list import AVLSurfList


class MflyOpt(Assembly):

	"""
	b_w = Float(8.8375, iotype='in', units='ft', desc='Wingspan (ft)')
	c_vt = Float(0.75, iotype='in', units='ft', desc='vertical tail chord  (ft)')
	c_ht = Float(0.75, iotype='in', units='ft', desc='horizontal tail chord (ft)')	 
	AR_w = Float(5.55, iotype='in', desc='wing aspect ratio')
	x_wLE = Float(0.4917, iotype='in', units='ft', desc='x-coordinate of wing leading edge')
	x_tLE = Float(3.35583, iotype='in', units='ft', desc='x-coordinate of tail leading edge')

	Len_fuse = Float(24.9, iotype='in', units='inch', desc='Fuselage length (inches)')
	Wid_fuse = Float(4.5, iotype='in', units='inch', desc='Fuselage width (inches)')
	Hgt_fuse = Float(9.0, iotype='in', units='inch', desc='Fuselage height (inches)')
	
	W_payload = Float(23.0, iotype='in', units='lb', desc='payload weight (pounds)')
	x_cg_payload = Float(0.733, iotype='in', units='ft')
	"""



	b_w = Float(8.4, iotype='in', units='ft', desc='Wingspan (ft)')
	c_vt = Float(0.5, iotype='in', units='ft', desc='vertical tail chord  (ft)')
	c_ht = Float(0.5, iotype='in', units='ft', desc='horizontal tail chord (ft)')	 
	AR_w = Float(6.1, iotype='in', desc='wing aspect ratio')
	x_wLE = Float(0.3917, iotype='in', units='ft', desc='x-coordinate of wing leading edge')
	x_tLE = Float(3.0, iotype='in', units='ft', desc='x-coordinate of tail leading edge')

	Len_fuse = Float(23.9, iotype='in', units='inch', desc='Fuselage length (inches)')
	Wid_fuse = Float(4.5, iotype='in', units='inch', desc='Fuselage width (inches)')
	Hgt_fuse = Float(8.0, iotype='in', units='inch', desc='Fuselage height (inches)')
	
	W_payload = Float(23.5, iotype='in', units='lb', desc='payload weight (pounds)')
	x_cg_payload = Float(0.7, iotype='in', units='ft')

	


	
	




	def configure(self):

		# Driver settings
		self.add('driver', SLSQPdriver())
		self.driver.accuracy = 1.0e-6
		self.driver.maxiter = 500
		


		# Creating instances for components
		self.add('config',Configuration_rect())
		self.add('Weight_buildup',Weight_buildup_rect())
		self.add('Static_margin',Static_margin())
		#self.add('CLCDiSolver',CLCDiSolver())
		self.add('CDp',Parasitic_drag())
		self.add('simRun',Runway_sim())
		self.add('GenPlot',GenPlot())
		self.add('exec2',exec2())
		self.add('avlgeogen',AVLGeo())
		self.add('avlsurflist',AVLSurfList())
		

	


		# Connect & passthrough manually
		self.connect('b_w',['config.b_w','Weight_buildup.b_w','simRun.b_w','GenPlot.b_w','avlgeogen.bref'])
		self.connect('AR_w',['config.AR_w','Static_margin.AR_w','simRun.AR_w'])
		self.connect('c_vt',['config.c_vt','Weight_buildup.c_vt','CDp.c_vt','GenPlot.c_vt','avlsurflist.chord_root_vtail','avlsurflist.chord_tip_vtail'])
		self.connect('c_ht',['config.c_ht','Weight_buildup.c_ht','Static_margin.c_ht','CDp.c_ht','simRun.c_ht','GenPlot.c_ht','avlsurflist.chord_root_htail','avlsurflist.chord_tip_htail'])
		self.connect('x_wLE',['config.x_wLE','Weight_buildup.x_wLE','Static_margin.x_wLE','simRun.x_wLE', 'GenPlot.x_wLE', 'avlsurflist.xle_root_wing', 'avlsurflist.xle_tip_wing', 'avlsurflist.xle_ail_start', 'avlsurflist.xle_ail_end'])
		self.connect('x_tLE',['config.x_tLE','Weight_buildup.x_tLE','Static_margin.x_tLE','simRun.x_tLE', 'GenPlot.x_tLE', 'avlsurflist.xle_root_htail', 'avlsurflist.xle_tip_htail', 'avlsurflist.xle_root_vtail', 'avlsurflist.xle_tip_vtail'])
		self.connect('Len_fuse',['Weight_buildup.Len_fuse','Static_margin.Len_fuse','CDp.Len_fuse','GenPlot.Len_fuse'])
		self.connect('Wid_fuse',['Weight_buildup.Wid_fuse','Static_margin.Wid_fuse','CDp.Wid_fuse','GenPlot.Wid_fuse'])
		self.connect('Hgt_fuse',['Weight_buildup.Hgt_fuse','CDp.Hgt_fuse','GenPlot.Hgt_fuse'])
		self.connect('W_payload',['Weight_buildup.W_payload','GenPlot.W_payload'])
		self.connect('x_cg_payload',['Weight_buildup.x_cg_payload'])
		

		# Adding components into driver's workflow
		#self.driver.workflow.add(['config','Weight_buildup','Static_margin','CLCDiSolver','CDp','simRun','GenPlot'])
		#self.driver.workflow.add(['config','Weight_buildup','Static_margin','CDp','simRun','GenPlot'])
  		self.driver.workflow.add(['config','Weight_buildup','Static_margin','CDp','avlsurflist','avlgeogen','exec2','simRun','GenPlot'])
  

		# Hooking up the components

		# config's outputs
		#self.connect('config.S_wing',['Weight_buildup.S_wing','Static_margin.S_wing','CDp.S_wing','simRun.S_wing'])
		self.connect('config.S_wing',['Weight_buildup.S_wing','Static_margin.S_wing','CDp.S_wing','simRun.S_wing','avlgeogen.sref'])
		self.connect('config.S_ht',['Weight_buildup.S_ht','Static_margin.S_ht','CDp.S_ht'])
		self.connect('config.S_vt',['Weight_buildup.S_vt','CDp.S_vt'])
		self.connect('config.c_w',['Weight_buildup.c_w','Static_margin.c_w','CDp.c_wr','GenPlot.c_w', 'avlsurflist.chord_root_wing', 'avlsurflist.chord_tip_wing'])
		self.connect('config.b_ht',['Weight_buildup.b_ht','GenPlot.b_ht'])
		self.connect('config.b_vt',['Weight_buildup.b_vt','GenPlot.b_vt'])
		self.connect('config.AR_ht',['Static_margin.AR_ht'])

		# Weight_buildup's outputs
		
		self.connect('Weight_buildup.W_0',['simRun.W_0'])
		self.connect('Weight_buildup.x_cg',['simRun.x_cg','Static_margin.x_cg','GenPlot.x_cg','avlgeogen.xcg'])
	


		# CDp's outputs

		self.connect('CDp.Cd_p',['simRun.Cd_p'])

		# AVL
		self.connect('avlsurflist.surfaces',['avlgeogen.surfaces'])
		self.connect('avlgeogen.savefile',['exec2.infile'])



		# Design Variables
		self.driver.add_parameter('b_w', name='wingspan', low=5.0, high=17.0)
		self.driver.add_parameter('c_vt', name='vertical tail chord', low=0.2, high=2.0)
		self.driver.add_parameter('c_ht', name='horizontal tail chord', low=0.15, high=2.0)
		self.driver.add_parameter('AR_w', name='Wing aspect ratio', low=5.0, high=17.0)
		self.driver.add_parameter('x_wLE', name='wing leading edge position', low=0.150, high=1.2)
		self.driver.add_parameter('x_tLE', name='tail leading edge position', low=1.50, high=4.0)
		self.driver.add_parameter('Len_fuse', name='fuselage length', low=20.0, high=50.0)	
		self.driver.add_parameter('Wid_fuse', name='fuselage width', low=4.0, high=6.0)		
		self.driver.add_parameter('Hgt_fuse', name='fuselage height', low=6.0, high=11.0)
		self.driver.add_parameter('W_payload', name='payload weight', low = 21.0, high = 42.0)
		self.driver.add_parameter('x_cg_payload', name='payload location', low = 0.625, high = 0.85)
		

		# Constraints

		# Dimension constraint
		self.driver.add_constraint('(x_tLE+max(c_vt,c_ht)+0.373) + b_w + max(1.20,config.b_vt+Hgt_fuse/12) - 14.583<= 0.0')   #assume height = 1.20ft
		
		
		# Total weight constraint
		self.driver.add_constraint('Weight_buildup.W_0  <= 65.0')

		# Static Margin constraint
		self.driver.add_constraint('Static_margin.SM - 0.13 >= 0.0')
		
	



		# Other constraints
		self.driver.add_constraint('Len_fuse/12 >= x_wLE+config.c_w')

		self.driver.add_constraint('x_wLE+config.c_w <= x_tLE')

		self.driver.add_constraint('config.b_ht <= b_w')

		self.driver.add_constraint('c_ht >= 0.0')
		self.driver.add_constraint('c_vt >= 0.0')
		


		self.driver.add_constraint('simRun.Lift_takeoff  - simRun.W_0 * 1.05 >= 0.0')

		self.driver.add_constraint('simRun.dist >= 130.0')





		# Objective
		self.driver.add_objective('-W_payload')

		





		self.driver.iprint = 0

		self.recorders = [JSONCaseRecorder('results.json')]




