from openmdao.main.api import Component, convert_units
from openmdao.lib.datatypes.api import Float, Int, Enum

class Configuration_rect(Component):
        """Generating Geometric variables (rectangular wing & conventional tail)"""
        """x-position of fuselage start = 0"""



        # Inputs
        
        b_w = Float(8.0, iotype='in', units='ft', desc='wingspan (ft)')

        c_vt = Float(0.5, iotype='in', units='ft', desc='vertical tail chord  (ft)')
         
        c_ht = Float(0.5, iotype='in', units='ft', desc='horizontal tail chord (ft)')
		 
        AR_w = Float(5.0, iotype='in', desc='wing aspect ratio')

        x_wLE = Float(0.2, iotype='in', units='ft', desc='x-coordinate of wing leading edge')
		 
        x_tLE = Float(2.2, iotype='in', units='ft', desc='x-coordinate of tail leading edge')

        
		 
		 

        # Outputs

        S_wing = Float(iotype='out', units='ft**2', desc='Wing area')
         
        S_ht = Float(iotype='out', units='ft**2', desc='horizontal tail area')

        S_vt = Float(iotype='out', units='ft**2', desc='vertical tail area')
		 
        c_w = Float(iotype='out', units='ft', desc='Wing chord')

        b_ht = Float(iotype='out', units='ft', desc='horizontal tail span (ft)')
		 
        b_vt = Float(iotype='out', units='ft', desc='vertical tail span (ft)')
		 
		 
        AR_ht = Float(iotype='out', desc='horizontal tail aspect ratio')

		 

        def execute(self):

           b_w = self.b_w
           AR = self.AR_w
           self.c_w = c_w = b_w/AR
           self.S_wing = b_w*c_w  # for rectangular wing

            # Volume coefficient method
           cVT = float(0.03)  # vertical tail volume coefficient
           cHT = float(0.30)   # horizontal tail volume coefficient
                         
           self.S_vt = cVT*b_w*self.S_wing/((self.x_tLE+self.c_vt*0.25)-(self.x_wLE+self.c_w*0.25))
           self.S_ht = cHT*c_w*self.S_wing/((self.x_tLE+self.c_ht*0.25)-(self.x_wLE+self.c_w*0.25))
                         
           self.b_vt  = self.S_vt/self.c_vt  # for rectangular vertical tail
           self.b_ht  = self.S_ht/self.c_ht  # for rectangular horizontal tail              
           
           self.AR_ht = self.b_ht**2 /self.S_ht

           
           print 'x_wLE ', self.x_wLE
           print 'x_tLE ', self.x_tLE
           print 'AR_w ', self.AR_w
           print 'b_w ', self.b_w
           print 'c_w', self.c_w
           print 'c_vt', self.c_vt
           print 'c_ht', self.c_ht
           print 'b_vt ', self.b_vt
           print 'b_ht ', self.b_ht
           print 'S_wing ', self.S_wing
           print 'S_vt ', self.S_vt
           print 'S_ht ', self.S_ht
           









        """def list_deriv_vars(self):

            return ('b_w','c_ht','c_vt','AR_w','x_wLE','x_tLE'),('S_wing','c_w')



        def provideJ(self):

            # S_wing
            dSwing_dbw = 2*self.b_w/self.AR_w
            dSwing_dcht = 0.0
            dSwing_dcvt = 0.0
            dSwing_dARw = -(self.b_w)**2/(self.AR_w)**2
            dSwing_dxwLE = 0.0
            dSwing_dxtLE = 0.0

            # c_w
            dcw_dbw = 1/self.AR_w
            dcw_dcht = 0.0
            dcw_dcvt = 0.0
            dcw_dARw = -self.b_w/(self.AR_w)**2
            dcw_dxwLE = 0.0
            dcw_dxtLE = 0.0

            J = array([[dSwing_dbw, dSwing_dcht, dSwing_dcvt, dSwing_dARw, dSwing_dxwLE, dSwing_dxtLE],
                       [dcw_dbw, dcw_dcht, dcw_dcvt, dcw_dARw, dcw_dxwLE, dcw_dxtLE]])

            return J"""










