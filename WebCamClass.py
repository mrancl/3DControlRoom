
import direct.directbase.DirectStart
from pandac.PandaModules import *

WIDTH = 835
HEIGHT = 512
SCALE = 10.6

class WebCamMonitor:
    def __init__(self, x=0.0, y=0.0, z=0.0, h=0, p=0, r=0):
        self.x = x
        self.y = y
        self.z = z

        self.h = h
        self.p = p
        self.r = r
        
        if WebcamVideo.getNumOptions() > 0:
            opt = WebcamVideo.getOption(4)
            self.cursor = opt.open()
            self.tex = Texture()
            self.cursor.setupTexture(self.tex)

        aspect = base.camLens.getAspectRatio()
        htmlWidth = 2.0 * aspect * WIDTH / base.win.getXSize()
        htmlHeight = 2.0 * HEIGHT / base.win.getYSize()
        cm = CardMaker("plane")
        cm.setFrame(-htmlWidth/2.0, htmlWidth/2.0, -htmlHeight/2, htmlHeight/2)
        
        self.plane = render.attachNewNode(cm.generate())
        self.plane.setScale(SCALE)
        self.plane.setPos(self.x,self.y,self.z)
        self.plane.setHpr(self.h, self.p, self.r)
        self.plane.setTexture(self.tex)

        scaleX = float(self.cursor.sizeX()) / float(self.tex.getXSize())
        scaleY = float(self.cursor.sizeY()) / float(self.tex.getYSize())
        self.plane.setTexScale(TextureStage.getDefault(), Vec2(scaleX, scaleY))
        
        taskMgr.add(self.update, "update video")

    def update(self, task):
        if self.cursor.ready():
            self.cursor.fetchIntoTexture(0, self.tex, 0)
        return task.cont


