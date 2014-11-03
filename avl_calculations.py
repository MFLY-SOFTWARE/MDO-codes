from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float
import math

class AVL_Calculations (Component):
	# consider the origin at the nose of the fuselage (0,0,0)
	# x points towards tail, y points out of right wing, z points straight up
	# wing/tail geometry inputs, consider all geometries start at wing/tail root for now
	xle_root_wing = Float(1.0, iotype='in', desc='x distance to wing root from plane tip')
	span_wing = Float(1.0, iotype='in', desc='wing tip to wing tip distance')
	chord_root_wing = Float(1.0, iotype='in', desc='chord length at wing root')
	sweeping_angle_wing = Float(1.0, iotype='in', desc='sweeping angle at wing root')
	taper_ratio_wing = Float(1.0, iotype='in', desc='wing taper ratio')
	dihedral_wing = Float(1.0, iotype='in', desc='dihedral angle at wing root')
	
	xle_root_tail = Float(1.0, iotype='in', desc='x distance to tail root from plane tip')
	span_tail = Float(1.0, iotype='in', desc='wing tip to tail tip distance')
	chord_root_tail = Float(1.0, iotype='in', desc='chord length at tail root')
	sweeping_angle_tail = Float(1.0, iotype='in', desc='sweeping angle at tail root')
	taper_ratio_tail = Float(1.0, iotype='in', desc='tail taper ratio')
	dihedral_tail = Float(1.0, iotype='in', desc='dihedral angle at tail root')

	# outputs
	xle_tip_wing = Float(1.0, iotype='out', desc='leading edge of wing tip x')
	yle_tip_wing = Float(1.0, iotype='out', desc='leading edge of wing tip y')
	zle_tip_wing = Float(1.0, iotype='out', desc='leading edge of wing tip z')
	chord_tip_wing = Float(1.0, iotype='out', desc='cord length at wing tip')
	
	xle_tip_tail = Float(1.0, iotype='out', desc='leading edge of tail tip x')
	yle_tip_tail = Float(1.0, iotype='out', desc='leading edge of tail tip y')
	zle_tip_tail = Float(1.0, iotype='out', desc='leading edge of tail tip z')
	chord_tip_tail = Float(1.0, iotype='out', desc='cord length at tail tip')

	def execute(self):
		# calculate x based on root wing/tail x value, sweeping angle, wingspan
		self.xle_tip_wing = self.xle_root_wing + math.tan(self.sweeping_angle_wing)*self.span_wing/2.0
		self.xle_tip_tail = self.xle_root_tail + math.tan(self.sweeping_angle_tail)*self.span_tail/2.0

		# calculate y based on dihedral, sweeping angle, wingspan
		self.yle_tip_wing = self.span_wing/2.0
		self.yle_tip_tail = self.span_tail/2.0

		# calculate z based on dihedral and wingspan
		self.zle_tip_wing = math.tan(self.dihedral_wing)*self.span_wing/2.0
		self.zle_tip_tail = math.tan(self.dihedral_tail)*self.span_tail/2.0

		# calculate tip chord length based on root chord length, taper ratio
		self.chord_tip_wing = self.chord_root_wing*self.taper_ratio_wing
		self.chord_tip_tail = self.chord_root_tail*self.taper_ratio_tail
		