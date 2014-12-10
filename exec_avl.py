# avl execution module

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Str
from openmdao.lib.datatypes.api import Float
from openmdao.lib.datatypes.api import File
from defs import surface
from math import tan
import avl,sys,time
import numpy

class exec2(Component):
    cdi = Float(0.0,iotype ='out', desc = 'Induced drag')
    infile = File(iotype = 'in')
   
    def execute(self):
        # create geometry file
        avl.avl()
        avl.load_geo(self.infile.path)
        avl.load_case('vanilla.run')
        avl.oper()
        print(avl.case_r.cdtot)
        self.cdi = avl.case_r.cdtot.item(0)

   # cdip = Float(avl.case_r.cdtot.item(0),iotype = 'out',desc = 'total induced drag')    
