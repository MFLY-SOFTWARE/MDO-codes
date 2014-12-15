# surface and section class definitions

class surface:
    def __init__(self,name,nchord,cspace,nspace,sspace,yduplicate,angle):
        self.name = name
        self.nchord = nchord
        self.cspace = cspace
        self.nspace = nspace
        self.sspace = sspace
        self.yduplicate = yduplicate
        self.angle = angle

    class section:
        def __init__(self,name,xle,yle,zle,chord,ainc,nspace,sspace,afile):
            self.name = name
            self.xle = xle
            self.yle = yle
            self.zle = zle
            self.chord = chord
            self.ainc = ainc
            self.nspace = nspace
            self.sspace = sspace
            self.afile = afile


        
