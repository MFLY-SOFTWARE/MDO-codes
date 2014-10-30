from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float
import math

class AVL_Calculations (Component):
	# get values in terms of front of plane, wont avl need in terms of wing root?
	# degrees or radians?

	# reference point (instead of hard coding)
	x_origin = Float(1.0, iotype='in', desc='origin x towards tail (plane tip)')
	y_origin = Float(1.0, iotype='in', desc='origin y towards right wing (plane tip)')
	z_origin = Float(1.0, iotype='in', desc='origin z straight up (plane tip)')

	# wing geometry inputs, consider all geometries start at wing root for now
	xle_root = Float(1.0, iotype='in', desc='x distance to wing root from plane tip')
	wingspan = Float(1.0, iotype='in', desc='wing tip to wing tip distance')
	chord_root = Float(1.0, iotype='in', desc='chord length at wing root')
	sweeping_angle = Float(1.0, iotype='in', desc='sweeping angle at wing root')
	taper_ratio = Float(1.0, iotype='in', desc='wing taper ratio')
	dihedral = Float(1.0, iotype='in', desc='dihedral angle at wing root')

	# outputs
	xle_tip = Float(1.0, iotype='out', desc='leading edge of wing tip x')
	yle_tip = Float(1.0, iotype='out', desc='leading edge of wing tip y')
	zle_tip = Float(1.0, iotype='out', desc='leading edge of wing tip z')
	chord_tip = Float(1.0, iotype='out', desc='cord length at wing tip')

	def execute(self):
		# calculate x based on root wing x value, dihedral, sweeping angle, wingspan
		self.xle_tip = self.xle_root + math.tan(self.sweeping_angle)*self.wingspan/2.0

		# calculate y based on dihedral, sweeping angle, wingspan
		self.yle_tip = self.wingspan/2.0

		# calculate z based on dihedral and wingspan
		self.zle_tip = math.tan(self.dihedral)*self.wingspan/2.0

		# calculate tip chord length based on root chord length, taper ratio
		self.chord_tip = self.chord_root*self.taper_ratio
		