from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float
from openmdao.lib.datatypes.api import List
from openmdao.lib.datatypes.api import Slot
from avl_geometry_surface import *

# link input vars for calculations to AVLCalc, output will link to AVLSurfList
# other design variables link directly to AVLSurfList
# link all over plane specification variables to AVLGeo
# link AVLSurfList output to AVLGeo, and then execute AVLGeo to write file

class AVLSurfList (Component):

	# wing geometry
	wing_nchord = Float(10.0, iotype='in')
	wing_cspace = Float(1.0, iotype='in')
	wing_nspan = Float(30.0, iotype='in')
	wing_sspace = Float(-2.0, iotype='in')
	# wing root
	xle_root_wing = Float(0.0, iotype='in')
	yle_root_wing = Float(0.0, iotype='in')
	zle_root_wing = Float(0.0, iotype='in')
	chord_root_wing = Float(1.64, iotype='in')
	ainc_root_wing = Float(2.0, iotype='in')
	# wing taper start
	xle_tap_start = Float(0.0, iotype='in')
	yle_tap_start = Float(1.5, iotype='in')
	zle_tap_start = Float(0.0, iotype='in')
	chord_tap_start = Float(1.64, iotype='in')
	ainc_tap_start = Float(2.0, iotype='in')
	# wing aileron start
	xle_ail_start = Float(0.025, iotype='in')
	yle_ail_start = Float(2.42, iotype='in')
	zle_ail_start = Float(0.0, iotype='in')
	chord_ail_start = Float(1.5088, iotype='in')
	ainc_ail_start = Float(0.0, iotype='in')
	# wing aileron end
	xle_ail_end = Float(0.07, iotype='in')
	yle_ail_end = Float(4.205, iotype='in')
	zle_ail_end = Float(0.0, iotype='in')
	chord_ail_end = Float(1.28, iotype='in')
	ainc_ail_end = Float(0.0, iotype='in')
	# wing tip
	xle_tip_wing = Float(0.103, iotype='in')
	yle_tip_wing = Float(4.375, iotype='in')
	zle_tip_wing = Float(0.0, iotype='in')
	chord_tip_wing = Float(1.23, iotype='in')
	ainc_tip_wing = Float(2.0, iotype='in')
	# winglet top
	xle_tip_winglet = Float(1.623, iotype='in')
	yle_tip_winglet = Float(4.375, iotype='in')
	zle_tip_winglet = Float(0.563, iotype='in')
	chord_tip_winglet = Float(0.3, iotype='in')
	ainc_tip_winglet = Float(2.0, iotype='in')
	# aileron specifications
	#ail_gain = Float(-1.0, iotype='in')
	#ail_xhinge = Float(.75, iotype='in')
	#ail_hvec_x = Float(0.0, iotype='in')
	#ail_hvec_y = Float(1.0, iotype='in')
	#ail_hvec_z = Float(0.0, iotype='in')
	#ail_sgndup = Float(-2.0, iotype='in')

	# horizontal tail geometry
	htail_nchord = Float(10.0, iotype='in')
	htail_cspace = Float(1.0, iotype='in')
	htail_nspan = Float(20.0, iotype='in')
	htail_sspace = Float(2.0, iotype='in')
	# horizontal tail root
	xle_root_htail = Float(3.01, iotype='in')
	yle_root_htail = Float(0.0, iotype='in')
	zle_root_htail = Float(0.0, iotype='in')
	chord_root_htail = Float(0.75, iotype='in')
	ainc_root_htail = Float(-1.0, iotype='in')
	# horizontal tail tip
	xle_tip_htail = Float(3.01, iotype='in')
	yle_tip_htail = Float(1.52, iotype='in')
	zle_tip_htail = Float(0.0, iotype='in')
	chord_tip_htail = Float(0.75, iotype='in')
	ainc_tip_htail = Float(-1.0, iotype='in')
	# elevator specifications
	elev_gain = Float(-1.00, iotype='in')
	elev_xhinge = Float(.5, iotype='in')
	elev_hvec_x = Float(0.0, iotype='in')
	elev_hvec_y = Float(1.0, iotype='in')
	elev_hvec_z = Float(0.0, iotype='in')
	elev_sgndup = Float(1.0, iotype='in')

	# vertical tail geometry
	vtail_nchord = Float(10.0, iotype='in')
	vtail_cspace = Float(1.0, iotype='in')
	vtail_nspan = Float(15.0, iotype='in')
	vtail_sspace = Float(1.0, iotype='in')
	# vertical tail root
	xle_root_vtail = Float(3.01, iotype='in')
	yle_root_vtail = Float(1.52, iotype='in')
	zle_root_vtail = Float(-.324, iotype='in')
	chord_root_vtail = Float(0.75, iotype='in')
	ainc_root_vtail = Float(0.0, iotype='in')
	# vertical tail tip
	xle_tip_vtail = Float(3.01, iotype='in')
	yle_tip_vtail = Float(1.52, iotype='in')
	zle_tip_vtail = Float(0.563, iotype='in')
	chord_tip_vtail = Float(0.75, iotype='in')
	ainc_tip_vtail = Float(0.0, iotype='in')
	# rudder specifications
	rud_gain = Float(1.00, iotype='in')
	rud_xhinge = Float(0.5, iotype='in')
	rud_hvec_x = Float(0.0, iotype='in')
	rud_hvec_y = Float(0.0, iotype='in')
	rud_hvec_z = Float(1.0, iotype='in')
	rud_sgndup = Float(-1.0, iotype='in')

	surfaces = List(Slot(AVLSurface), iotype = 'out')

	def execute(self):
		wing_def = "AFILE\ns1223.dat"
		winglet_def = "AFILE\ne201.dat"
		tail_def = "NACA\n0012\nCLAF\n1.1078"

		# MAIN WING SURFACE
		wing_root = AVLSection(self.xle_root_wing, self.yle_root_wing, self.zle_root_wing,
			self.chord_root_wing, self.ainc_root_wing, wing_def)

		wing_tap = AVLSection(self.xle_tap_start, self.yle_tap_start, self.zle_tap_start,
			self.chord_tap_start, self.ainc_tap_start, wing_def)

		#aileron = AVLControlSurface("Aileron", self.ail_gain, self.ail_xhinge, self.ail_hvec_x,
			#self.ail_hvec_y, self.ail_hvec_z, self.ail_sgndup)

		wing_ail_start = AVLSection(self.xle_ail_start, self.yle_ail_start, self.zle_ail_start,
			self.chord_ail_start, self.ainc_ail_start, wing_def)

		wing_ail_end = AVLSection(self.xle_ail_end, self.yle_ail_end, self.zle_ail_end,
			self.chord_ail_end, self.ainc_ail_end, wing_def)

		wing_tip = AVLSection(self.xle_tip_wing, self.yle_tip_wing, self.zle_tip_wing,
			self.chord_tip_wing, self.ainc_tip_wing, wing_def)

		winglet_tip = AVLSection(self.xle_tip_winglet, self.yle_tip_winglet, self.zle_tip_winglet,
			self.chord_tip_winglet, self.ainc_tip_winglet, winglet_def)

		main_wing = AVLSurface("Main Wing", self.wing_nchord, self.wing_cspace, self.wing_nspan,
			self.wing_sspace, 1.0, 1.0, 1.0, [wing_root, wing_tap, wing_ail_start, wing_ail_end,
			wing_tip, winglet_tip], True)

		# HORIZONTAL TAIL SURFACE
		elevator = AVLControlSurface("Elevator", self.elev_gain, self.elev_xhinge, self.elev_hvec_x,
			self.elev_hvec_y, self.elev_hvec_z, self.elev_sgndup)

		htail_root = AVLSection(self.xle_root_htail, self.yle_root_htail, self.zle_root_htail,
			self.chord_root_htail, self.ainc_root_htail, tail_def, elevator)

		htail_tip = AVLSection(self.xle_tip_htail, self.yle_tip_htail, self.zle_tip_htail,
			self.chord_tip_htail, self.ainc_tip_htail, tail_def, elevator)

		horizontal_tail = AVLSurface("Horizontal Tail", self.htail_nchord, self.htail_cspace, self.htail_nspan,
			self.htail_sspace, 1.0, 1.0, 1.0, [htail_root, htail_tip], True)

		# VERTICAL TAIL SURFACE
		rudder = AVLControlSurface("Rudder", self.rud_gain, self.rud_xhinge, self.rud_hvec_x,
			self.rud_hvec_y, self.rud_hvec_z, self.rud_sgndup)

		vtail_root = AVLSection(self.xle_root_vtail, self.yle_root_vtail, self.zle_root_vtail,
			self.chord_root_vtail, self.ainc_root_vtail, tail_def, rudder)

		vtail_tip = AVLSection(self.xle_tip_vtail, self.yle_tip_vtail, self.zle_tip_vtail,
			self.chord_tip_vtail, self.ainc_tip_vtail, tail_def, rudder)

		vertical_tail = AVLSurface("Vertical Tail", self.vtail_nchord, self.vtail_cspace, self.vtail_nspan,
			self.vtail_sspace, 1.0, 1.0, 1.0, [vtail_root, vtail_tip], True)

		self.surfaces = [main_wing, horizontal_tail, vertical_tail]
		