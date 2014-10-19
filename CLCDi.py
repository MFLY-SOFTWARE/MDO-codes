from openmdao.main.api import Component, convert_units
from openmdao.lib.datatypes.api import Float, Int, Enum
import math
from math import pi, sin
import numpy

class CLCDiSolver(Component):
        """Generating CL & CDi & K (induced drag coefficient) at different AOA (rectangular wing only)"""
        
        # Inputs
        a_inf = Float(9.5, iotype='in', units='deg', desc='freestream angle of attack')
        a_zeroLift = Float(-9.0, iotype='in', units='deg', desc='angle of attack at zero sectional lift')
        N = Int(70, iotype='in', desc='number of collocation points along the wingspan')
        AR = Float(5.55, iotype='in', desc='aspect ratio')
            
        # Outputs
        CL = Float(iotype='out', desc='lift coefficient')
        CDi = Float(iotype='out', desc='induced drag coefficient')
        K = Float(iotype='out')
        
        def execute(self):
            """applying lifting line theory"""
        
            AR = self.AR
            N = self.N
            a0 = 2*pi  # Sectional lift curve slope
            theta = numpy.linspace(pi/2, pi-pi/2/N, N)  # locations of collocation points
            a_inf , a_zeroLift = convert_units(self.a_inf, 'deg', 'rad') , convert_units(self.a_zeroLift, 'deg', 'rad')

            M = numpy.zeros([N,N]) # coefficient matrix
            F = numpy.zeros([N,1]) # right hand side array
    
    
            for ii in range(N):   # loop over span-wise location
                                for jj in range(N): # loop over A_n unknowns
                   					M[ii,jj] = 4*AR/a0*sin((2*jj+1)*theta[ii]) + (2*jj+1)*sin((2*jj+1)*theta[ii])/sin(theta[ii]);   # filling the coefficient matrix
                        ####rectangular wing only#### otherwise AR = b**2/S = b/c
            
        
            
            
            F[:] = (a_inf - a_zeroLift)   # assuming no twist   
            
    
            A = numpy.linalg.solve(M,F) # solving the sys
    
            self.A = A
            ## OUTPUT
    
            #CL
            self.CL = pi*self.AR*A[0][0]
        
            #CDi & K

            sum = 0;
            for i in range(N):
                sum = sum + (2*i+1)*A[i][0]**2;
            

            Del = sum/A[0][0]**2 - 1
            e = 1/(1+Del)

            self.K = 1/(pi*AR*e)
            self.CDi = pi*self.AR*sum;


            print'CL', self.CL
            print'CDi', self.CDi



