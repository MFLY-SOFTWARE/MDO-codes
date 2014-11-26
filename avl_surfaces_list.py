from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float
from openmdao.lib.datatypes.api import List
from openmdao.lib.datatypes.api import Slot
from avl_geometry_surface import *
import math

# have not considered NACA
# have not done ainc, need to ask about that
# does aileron control variables change at root AND tip? (can you use it twice, basically)
# because that's what I'm doing right now
#
#
# way it works:
# link input vars for calculations to AVLCalc, output will link to AVLSurfList
# other design variables link directly to AVLSurfList
# link all over plane specification variables to AVLGeo
# link AVLSurfList output to AVLGeo, and then execute AVLGeo to write file

class AVLSurfList (Component):

	# wing geometry
	wing_nchord = Float(10.0, iotype='in')
	wing_cspace = Float(1.0, iotype='in')
	wing_nspan = Float(40.0, iotype='in')
	wing_sspace = Float(-2.0, iotype='in')
	# wing root
	xle_root_wing = Float(0.0, iotype='in')
	yle_root_wing = Float(0.0, iotype='in')
	zle_root_wing = Float(0.0, iotype='in')
	chord_root_wing = Float(1.136, iotype='in')
	ainc_root_wing = Float(0.0, iotype='in')
	# wing aileron start
	xle_ail_start = Float(0.0, iotype='in')
	yle_ail_start = Float(3.059, iotype='in')
	zle_ail_start = Float(.289, iotype='in')
	chord_ail_start = Float(1.136, iotype='in')
	ainc_ail_start = Float(0.0, iotype='in')
	# wing aileron end
	xle_ail_end = Float(0.0, iotype='in')
	yle_ail_end = Float(4.67, iotype='in')
	zle_ail_end = Float(.487, iotype='in')
	chord_ail_end = Float(1.136, iotype='in')
	ainc_ail_end = Float(0.0, iotype='in')
	# wing tip
	xle_tip_wing = Float(0.0, iotype='in')
	yle_tip_wing = Float(5.02, iotype='in')
	zle_tip_wing = Float(.5291, iotype='in')
	chord_tip_wing = Float(1.136, iotype='in')
	ainc_tip_wing = Float(0.0, iotype='in')
	# aileron specifications
	ail_gain = Float(-1.0, iotype='in')
	ail_xhinge = Float(.725, iotype='in')
	ail_hvec_x = Float(0.0, iotype='in')
	ail_hvec_y = Float(1.62, iotype='in')
	ail_hvec_z = Float(.199, iotype='in')
	ail_sgndup = Float(-2.0, iotype='in')

	# horizontal tail geometry
	htail_nchord = Float(10.0, iotype='in')
	htail_cspace = Float(1.0, iotype='in')
	htail_nspan = Float(25.0, iotype='in')
	htail_sspace = Float(1.0, iotype='in')
	# horizontal tail root
	xle_root_htail = Float(3.42, iotype='in')
	yle_root_htail = Float(0.0, iotype='in')
	zle_root_htail = Float(.51, iotype='in')
	chord_root_htail = Float(1.06, iotype='in')
	ainc_root_htail = Float(0.0, iotype='in')
	# horizontal tail tip
	xle_tip_htail = Float(3.42, iotype='in')
	yle_tip_htail = Float(1.60, iotype='in')
	zle_tip_htail = Float(.51, iotype='in')
	chord_tip_htail = Float(1.06, iotype='in')
	ainc_tip_htail = Float(0.0, iotype='in')
	# elevator specifications
	elev_gain = Float(1.00, iotype='in')
	elev_xhinge = Float(.5, iotype='in')
	elev_hvec_x = Float(0.0, iotype='in')
	elev_hvec_y = Float(1.0, iotype='in')
	elev_hvec_z = Float(0.0, iotype='in')
	elev_sgndup = Float(1.0, iotype='in')

	# vertical tail geometry
	vtail_nchord = Float(10.0, iotype='in')
	vtail_cspace = Float(1.0, iotype='in')
	vtail_nspan = Float(10.0, iotype='in')
	vtail_sspace = Float(0.0, iotype='in')
	# vertical tail root
	xle_root_vtail = Float(3.42, iotype='in')
	yle_root_vtail = Float(1.60, iotype='in')
	zle_root_vtail = Float(.51, iotype='in')
	chord_root_vtail = Float(1.06, iotype='in')
	ainc_root_vtail = Float(0.0, iotype='in')
	# vertical tail tip
	xle_tip_vtail = Float(3.42, iotype='in')
	yle_tip_vtail = Float(1.60, iotype='in')
	zle_tip_vtail = Float(1.41, iotype='in')
	chord_tip_vtail = Float(1.06, iotype='in')
	ainc_tip_vtail = Float(0.0, iotype='in')
	# rudder specifications
	rud_gain = Float(1.00, iotype='in')
	rud_xhinge = Float(.5, iotype='in')
	rud_hvec_x = Float(0.0, iotype='in')
	rud_hvec_y = Float(0.0, iotype='in')
	rud_hvec_z = Float(1.0, iotype='in')
	rud_sgndup = Float(1.0, iotype='in')

	# multiple tails will come later

	surfaces = List(Slot(AVLSurface), iotype = 'out')

	def execute(self):
		# MAIN WING SURFACE
		wing_root = AVLSection(self.xle_root_wing, self.yle_root_wing, self.zle_root_wing,
			self.chord_root_wing, self.ainc_root_wing, 4412)

		aileron = AVLControlSurface("Aileron", self.ail_gain, self.ail_xhinge, self.ail_hvec_x,
			self.ail_hvec_y, self.ail_hvec_z, self.ail_sgndup)

		wing_ail_start = AVLSection(self.xle_ail_start, self.yle_ail_start, self.zle_ail_start,
			self.chord_ail_start, self.ainc_ail_start, 4412, aileron)

		wing_ail_end = AVLSection(self.xle_ail_end, self.yle_ail_end, self.zle_ail_end,
			self.chord_ail_end, self.ainc_ail_end, 4412, aileron)

		wing_tip = AVLSection(self.xle_tip_wing, self.yle_tip_wing, self.zle_tip_wing,
			self.chord_tip_wing, self.ainc_tip_wing, 4412)

		main_wing = AVLSurface("Main Wing", self.wing_nchord, self.wing_cspace, self.wing_nspan,
			self.wing_sspace, 1.0, 1.0, 1.0, [wing_root, wing_ail_start, wing_ail_end, wing_tip], True)

		# HORIZONTAL TAIL SURFACE
		elevator = AVLControlSurface("Elevator", self.elev_gain, self.elev_xhinge, self.elev_hvec_x,
			self.elev_hvec_y, self.elev_hvec_z, self.elev_sgndup)

		htail_root = AVLSection(self.xle_root_htail, self.yle_root_htail, self.zle_root_htail,
			self.chord_root_htail, self.ainc_root_htail, 4412, elevator)

		htail_tip = AVLSection(self.xle_tip_htail, self.yle_tip_htail, self.zle_tip_htail,
			self.chord_tip_htail, self.ainc_tip_htail, 4412, elevator)

		horizontal_tail = AVLSurface("Horizontal Tail", self.htail_nchord, self.htail_cspace, self.htail_nspan,
			self.htail_sspace, 1.0, 1.0, 1.0, [htail_root, htail_tip], True)

		# VERTICAL TAIL SURFACE
		rudder = AVLControlSurface("Rudder", self.rud_gain, self.rud_xhinge, self.rud_hvec_x,
			self.rud_hvec_y, self.rud_hvec_z, self.rud_sgndup)

		vtail_root = AVLSection(self.xle_root_vtail, self.yle_root_vtail, self.zle_root_vtail,
			self.chord_root_vtail, self.ainc_root_vtail, 4412, rudder)

		vtail_tip = AVLSection(self.xle_tip_vtail, self.yle_tip_vtail, self.zle_tip_vtail,
			self.chord_tip_vtail, self.ainc_tip_vtail, 4412, rudder)

		vertical_tail = AVLSurface("Vertical Tail", self.vtail_nchord, self.vtail_cspace, self.vtail_nspan,
			self.vtail_sspace, 1.0, 1.0, 1.0, [vtail_root, vtail_tip], True)

		self.surfaces = [main_wing, horizontal_tail, vertical_tail]
		