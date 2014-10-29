class AVLControlSurface:
	surface = "Aileron"
	gain = -1.00
	xhinge = 0.725
	xhvec = 0.0
	yhvec = 1.6179
	zhvec = 0.1986
	sgndup = -2.0
	def __init__(self, surf, gain, xhinge, xhvec, yhvec, zhvec, sgndup):
		self.surface = surf
		self.gain = gain
		self.xhinge = xhinge
		self.xhvec = xhvec
		self.yhvec = yhvec
		self.zhvec = zhvec
		self.sgndup = sgndup

class AVLSection:
	xle = 0.0
	yle = 0.0
	zle = 0.0
	chord = 1.13627
	ainc = 0.0
	NACA = 4412
	hascontrol = True
	ControlSurface = AVLControlSurface(
									"Aileron",
									-1.00,
									0.725,
									0.0,
									1.6179,
									0.1986,
									-2.0)
	def __init__(self, 
				xle, 
				yle, 
				zle, 
				chord, 
				ainc, 
				naca, 
				ctlsurf=AVLControlSurface("NONE",0,0,0,0,0,0)):
		self.xle = xle
		self.yle = yle
		self.zle = zle
		self.chord = chord
		self.ainc = ainc
		self.NACA = naca
		self.ControlSurface = ctlsurf
		if self.ControlSurface.surface == "NONE":
			self.hascontrol = False
		else:
			self.hascontrol = True
	
class AVLSurface:
	name = "wing"
	nchordwise = 10
	cspace = 1.0
	nspanwise = 40
	sspace = -2.0
	xscale = 1.0
	yscale = 1.0
	zscale = 1.0
	isyduplicate = True
	yduplicate = 0.0
	sections = [AVLSection(0.0, 0.0, 0.0, 1.13627, 0.0, 4412), \
				AVLSection(0.0, 0.774, 0.0, 1.13627, 0.0, 4412), \
				AVLSection(0.0, 3.0586, 0.0, 1.13627, 0.0, 4412)]
	def __init__(self,
				name, 
				nchordwise,
				cspace,
				nspanwise,
				sspace,
				xscale,
				yscale,
				zscale,
				sections,
				isyduplicate=False,
				yduplicate=0.0):
		self.name = name
		self.nchordwise = nchordwise
		self.cspace = cspace
				
	
	
