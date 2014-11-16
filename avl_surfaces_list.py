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
	# wing root
	xle_root_wing = Float(0.0, iotype='in')
	yle_root_wing = Float(0.0, iotype='in')
	zle_root_wing = Float(0.0, iotype='in')
	chord_root_wing = Float(1.136, iotype='in')
	ainc_root_wing = Float(0.0, iotype='in')
	# wing dihedral start
	xle_dih_wing = Float(0.0, iotpye='in')
	yle_dih_wing = Float(0.774, iotype='in')
	zle_dih_wing = Float(0.0, iotype='in')
	chord_dih_wing = Float(1.136, iotype='in')
	ainc_dih_wing = Float(0.0, iotype='in')
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
	# horizontal tail root
	# horizontal tail tip
	xle_tip_htail = Float(1.0, iotype='in')
	yle_tip_htail = Float(1.0, iotype='in')
	zle_tip_htail = Float(1.0, iotype='in')
	chord_tip_htail = Float(1.0, iotype='in')

	# vertical tail geometry
	# vertical tail root
	# vertical tail tip

	surfaces = List(Slot(AVLSurface), iotype = 'out')

	def execute(self):
		# MAIN WING SURFACE

		wing_root = AVLSection(self.xle_root_wing, self.yle_root_wing, self.zle_root_wing,
			self.chord_root_wing, self.ainc_root_wing, 4412)

		wing_dih_start = AVLSection(self.xle_dih_wing, self.yle_dih_wing, self.zle_dih_wing,
			self.chord_dih_wing, self.ainc_dih_wing, 4412)

		aileron = AVLControlSurface("Aileron", self.ail_gain, self.ail_xhinge, self.ail_hvec_x,
			self.ail_hvec_y, self.ail_hvec_z, self.ail_sgndup)

		wing_ail_start = AVLSection(self.xle_ail_start, self.yle_ail_start, self.zle_ail_start,
			self.chord_ail_start, self.ainc_ail_start, 4412, aileron)

		wing_ail_end = AVLSection(self.xle_ail_end, self.yle_ail_end, self.zle_ail_end,
			self.chord_ail_end, self.ainc_ail_end, 4412, aileron)

		wing_tip = AVLSection(self.xle_tip_wing, self.yle_tip_wing, self.zle_tip_wing,
			self.chord_tip_wing, self.ainc_tip_wing, 4412)

		main_wing = AVLSurface("Main Wing", 10, 1.0, 40, -2.0, 1.0, 1.0, 1.0, 
			[wing_root, wing_dih_start, wing_ail_start, wing_ail_end, wing_tip])

		# HORIZONTAL TAIL SURFACE
		#h_tail = AVLSurface()
		#h_tail.name = "Horizontal Tail"

		#h_tail_root = AVLSection()
		#h_tail_tip = AVLSection()

		#h_tail.sections = [h_tail_root, h_tail_tip]

		# VERTICAL TAIL SURFACE
		#v_tail = AVLSurface()
		#v_tail.name = "Vertical Tail"

		#v_tail_root = AVLSection()
		#v_tail_tip = AVLSection()

		#v_tail.sections = [v_tail_root, v_tail_tip]

		# CONTINUE FROM HERE MA NIGGA

		self.surfaces = [main_wing]

		for section in main_wing.sections[:]:
			print section.yle
			print section.ControlSurface.surface
		