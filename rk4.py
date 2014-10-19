from openmdao.main.api import Component, convert_units
from openmdao.lib.datatypes.api import Float, Int, Enum
import math
from math import pi, sin
import numpy



def RK4(f):
    return lambda E, dx: (
           		lambda dE1: (
           			lambda dE2: (
           				lambda dE3: (
           					lambda dE4: (dE1 + 2*dE2 + 2*dE3 + dE4)/6
        								)( dx * f( E + dE3   ) )
	    								)( dx * f(  E + dE2 /2 ) )
	    								)( dx * f(  E + dE1 /2 ) )
	    								)( dx * f(  E  ) )




