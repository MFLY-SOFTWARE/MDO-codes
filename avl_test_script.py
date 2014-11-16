from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float
import math

from avl_surfaces_list import AVLSurfList
from avl_geometry_gen import AVLGeo

surf = AVLSurfList()
surf.execute()

print "Success!"

gen = AVLGeo()
gen.surfaces = surf.surfaces
gen.execute()