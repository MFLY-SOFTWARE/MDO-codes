from openmdao.main.api import Component, convert_units
from openmdao.lib.datatypes.api import Float, Int, Enum, Str
import math
from math import pi, sin, sqrt

import matplotlib as mpl
from mpl_toolkits.mplot3d import axis3d, Axes3D
import numpy as np
import matplotlib.pyplot as plt



class GenPlot(Component):

 	Len_fuse = Float(24.9, iotype='in', units='inch', desc='Fuselage length (inches)')

	Wid_fuse = Float(4.5, iotype='in', units='inch', desc='Fuselage width (inches)')

	Hgt_fuse = Float(9, iotype='in', units='inch', desc='Fuselage height (inches)')

	b_w = Float(8.8375, iotype='in', units='ft', desc='wingspan (ft)')

	b_ht = Float(1.0, iotype='in', units='ft', desc='horizontal tail span (ft)')
		 
	b_vt = Float(1.0, iotype='in', units='ft', desc='vertical tail span (ft)')

	c_vt = Float(0.75, iotype='in', units='ft', desc='vertical tail chord  (ft)')
         
	c_ht = Float(0.75, iotype='in', units='ft', desc='horizontal tail chord (ft)')

	c_w = Float(1.2, iotype='in', units='ft', desc='Wing chord (ft)')

	x_wLE = Float(0.4917, iotype='in', units='ft', desc='x-coordinate of wing leading edge')
		 
	x_tLE = Float(3.35583, iotype='in', units='ft', desc='x-coordinate of tail leading edge')

	x_cg = Float(2, iotype='in', units='ft', desc='x-coordinate of cg')

	W_payload = Float(23.0, iotype='in', units='lb', desc='payload weight (pounds)')

	

	def execute(self):
		Len_fuse = convert_units(self.Len_fuse,'inch','ft')
		Wid_fuse = convert_units(self.Wid_fuse,'inch','ft')
		Hgt_fuse = convert_units(self.Hgt_fuse,'inch','ft')
		c_w = self.c_w
		c_ht = self.c_ht
		c_vt = self.c_vt
		x_wLE = self.x_wLE
		x_tLE = self.x_tLE
		x_cg = self.x_cg
		b_w = self.b_w
		b_ht = self.b_ht
		b_vt = self.b_vt
		#itername = self.itername
		count = self.exec_count



		fig1 = plt.figure(1)
		fig2 = plt.figure(2)

		ax1 = fig1.add_subplot(111,projection='3d')
		ax2 = fig2.add_subplot(111)
		ax1.cla()
		ax2.cla()

		# Fuselage
		x = [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , Len_fuse , Len_fuse , Len_fuse , Len_fuse , Len_fuse]
		y = [-Wid_fuse/2 , -Wid_fuse/2 , Wid_fuse/2 , Wid_fuse/2 , -Wid_fuse/2 , -Wid_fuse/2 , -Wid_fuse/2 , Wid_fuse/2 , Wid_fuse/2 , -Wid_fuse/2]
		z = [-Hgt_fuse/2 , Hgt_fuse/2 , Hgt_fuse/2 , -Hgt_fuse/2 , -Hgt_fuse/2 , -Hgt_fuse/2 , Hgt_fuse/2 , Hgt_fuse/2 , -Hgt_fuse/2 , -Hgt_fuse/2]
		ax1.plot(x, y, z, 'k-')
		ax2.plot(x, y, 'k-')
		x = [0.0 , Len_fuse]
		y = [-Wid_fuse/2 , -Wid_fuse/2]
		z = [Hgt_fuse/2 , Hgt_fuse/2]
		ax1.plot(x, y, z, 'k-')
		ax2.plot(x, y, 'k-')
		x = [0.0 , Len_fuse]
		y = [Wid_fuse/2 , Wid_fuse/2]
		z = [-Hgt_fuse/2 , -Hgt_fuse/2]
		ax1.plot(x, y, z, 'k-')
		ax2.plot(x, y, 'k-')
		x = [0.0 , Len_fuse]
		y = [Wid_fuse/2 , Wid_fuse/2]
		z = [Hgt_fuse/2 , Hgt_fuse/2]
		ax1.plot(x, y, z, 'k-')
		ax2.plot(x, y, 'k-')



		# Wing
		x = [x_wLE , x_wLE , x_wLE+c_w , x_wLE+c_w]
		y = [Wid_fuse/2, b_w/2 , b_w/2 , Wid_fuse/2]
		z = [0.0 , 0.0 , 0.0 , 0.0]
		ax1.plot(x, y, z, 'b-')
		ax2.plot(x, y, 'b-')
		x = [x_wLE , x_wLE , x_wLE+c_w , x_wLE+c_w]
		y = [-Wid_fuse/2, -b_w/2 , -b_w/2 , -Wid_fuse/2]
		ax1.plot(x, y, z, 'b-')
		ax2.plot(x, y, 'b-')

		# Tailboom
		x = [x_wLE+c_w*0.25 , x_tLE]
		y = [0.0 , 0.0]
		z = [0.0 , 0.0]
		ax1.plot(x, y, z, 'r-')
		ax2.plot(x, y, 'r-')

		# HT
		x = [x_tLE , x_tLE , x_tLE+c_ht , x_tLE+c_ht , x_tLE]
		y = [b_ht/2 , -b_ht/2 , -b_ht/2 , b_ht/2 , b_ht/2]
		z = [0.0 , 0.0 , 0.0 , 0.0 , 0.0]
		ax1.plot(x, y, z, 'g-')
		ax2.plot(x, y, 'g-')

		# VT
		x = [x_tLE , x_tLE , x_tLE+c_vt , x_tLE+c_vt , x_tLE]
		y = [0.0 , 0.0 , 0.0 , 0.0 , 0.0]
		z = [0.0 , b_vt , b_vt , 0.0 , 0.0]
		ax1.plot(x, y, z, 'g-')
		ax2.plot(x, y, 'g-')


		# c.g.
		x = x_cg
		y = 0.0
		ax2.plot(x,y,'kx')

		# Wing ac location
		x = x_wLE+0.25*c_w
		y = 0.0
		ax2.plot(x,y,'b+')

		# H-tail ac location
		x = x_tLE+0.25*c_ht
		y = 0.0
		ax2.plot(x,y,'g+')


		#plt.xlim([-10,10])
		#plt.ylim([-10,10])


		ax1.auto_scale_xyz([-5,9],[-7,7],[-7,7])
		ax2.axis([-5,9,-7,7])
		
		ax1.view_init(35.27,225)
		
		ax1.set_xlabel('x')
		ax1.set_ylabel('y')
		ax1.set_zlabel('z')
		ax2.set_xlabel('x')
		ax2.set_ylabel('y')


		#fname1 = 'movie/3D/%10s_image3D.png' %itername
		#fname2 = 'movie/2D/%10s_image2D.png' %itername
		fname1 = 'movie/3D/%03d_image3D.png' %count
		fname2 = 'movie/2D/%03d_image2D.png' %count
		p = 'Payload: %.2f lbs' %self.W_payload
		ax1.text(2, -2, -7, p, color='red')
		#fig1.savefig('movie/image1.png')
		#fig2.savefig('movie/image2.png')
		fig1.savefig(fname1)
		fig2.savefig(fname2)
		
		






