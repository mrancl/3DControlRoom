from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *

class Camera(DirectObject):
    def __init__(self, inputManager):
        self.floorMask = BitMask32.bit(0)
        self.inputManager = inputManager
        self.setupOperator()
        self.setupCollisions()
        self.selectLerp = None

        self.prevtime = 0
 

    def setupOperator(self):
        self.operator = render.attachNewNode("Operator")
        self.operator.reparentTo(render)
        base.camera.reparentTo(self.operator)
        base.camera.setPos(83.092, -150.189, 70.776)
        base.camera.setHpr(24.875, -6.25, 0)
        base.camera.getChild(0).node().getLens().setNear(1.0)
        base.camera.getChild(0).node().getLens().setFar(100000.0)
        base.camera.getChild(0).node().getLens().setFov(VBase2(39.32012, 30.00000))
        base.camera.getChild(0).node().getLens().setFilmSize(1.000, 0.750)
        base.camera.getChild(0).node().getLens().setFocalLength(1.39951908588)

    def setupCollisions(self):
        base.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        cs = CollisionSphere(0, 0, 1, 1)
        cnode = base.camera.attachNewNode(CollisionNode('cnode'))
        cnode.setPos(0,0,0)
        cnode.node().addSolid(cs)

        base.cTrav.addCollider(cnode, self.pusher)
        self.pusher.addCollider(cnode, base.camera)

    def cameraControl(self, task):
        elapsed = task.time - self.prevtime

        oldPos = base.camera.getPos()

        leftVec = VBase3(-1, 0, 0)
        yformedVec = render.getRelativeVector(base.camera, leftVec)

        if self.inputManager.goLeft:
            newPos = oldPos + yformedVec * elapsed * 50
            base.camera.setPos(newPos)
        if self.inputManager.goRight:
            newPos = oldPos - yformedVec * elapsed * 50
            base.camera.setPos(newPos)
  
        forwardVec = VBase3(0, -1, 0)
        xformedVec = render.getRelativeVector(base.camera, forwardVec)
        
        if self.inputManager.goForward:
            newPos = oldPos - xformedVec * elapsed * 100
            base.camera.setPos(newPos)

        if self.inputManager.goBackwards and base.camera.getY()>-175:
            newPos = oldPos + xformedVec * elapsed * 100
            base.camera.setPos(newPos)
        if(self.inputManager.keyMap["select"] == True):
            self.selectScreen()
        if(self.inputManager.keyMap["reload"] == True):
            self.reload()
        if(base.mouseWatcherNode.hasMouse() == True):
           mpos = base.mouseWatcherNode.getMouse()
           base.camera.setP(mpos.getY() * 15)
           base.camera.setH(mpos.getX() * -25)
        self.inputManager.getMouseAim()
        base.cTrav.traverse(render)
        self.prevtime = task.time
        return task.cont

    def selectScreen(self):
        if self.inputManager.browser != None:
            pos = self.inputManager.browser.quad.getPos()
            pos.setY(self.inputManager.browser.quad.getY()- 40)
            pos.setX(self.inputManager.browser.quad.getX()+ 15)
            self.selectLerp = LerpPosInterval(base.camera, 1, pos)
            self.selectLerp.start()

    def reload(self):
        if self.inputManager.browser != None:
            self.inputManager.browser.webView.loadURL(self.inputManager.browser.htmlFile, '', '', '')

    def collisionEvent(self, entry):
        return

       