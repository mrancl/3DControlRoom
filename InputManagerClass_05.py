from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import sys

class InputManager(DirectObject):
    def __init__(self):

        self.goForward=0
        self.goBackwards=0
        self.goRight=0
        self.goLeft=0

        self.keyMap = {
                       "select":0,
                       "reload":0}

        self.accept("escape", sys.exit)
        self.accept("f2", self.setKey, ["select",1])
        self.accept("f1", self.setKey, ["reload",1])
        self.accept("f2-up", self.setKey, ["select",0])
        self.accept("f1-up", self.setKey, ["reload",0])
        self.accept ("arrow_left", self.setGoLeft, [1])
        self.accept ("arrow_left-up", self.setGoLeft, [0])

        self.accept ("arrow_right", self.setGoRight, [1])
        self.accept ("arrow_right-up", self.setGoRight, [0])

        self.accept ("arrow_up", self.setGoForward, [1])
        self.accept ("arrow_up-up", self.setGoForward, [0])

        self.accept ("arrow_down", self.setGoBackwards, [1])
        self.accept ("arrow_down-up", self.setGoBackwards, [0])

        self.browser = None

        self.setupMouseAim()

    def setKey(self, key, value):
        self.keyMap[key] = value

    def setGoLeft (self,value):
        self.goLeft = value

    def setGoRight (self,value):
        self.goRight = value

    def setGoForward (self,value):
        self.goForward = value

    def setGoBackwards (self,value):
        self.goBackwards = value

    def setupMouseAim(self):
		self.CN = CollisionNode("RayCN")
		self.cRay = CollisionRay()
		self.CN.addSolid(self.cRay)
		self.CN.setFromCollideMask(BitMask32.bit(8))
		self.CN.setIntoCollideMask(BitMask32.allOff())
		self.CN = base.camera.attachNewNode(self.CN)

		self.cTrav = CollisionTraverser()
		# Creates a traverser to do collision testing

		self.cHanQ = CollisionHandlerQueue()
		# Creates a queue type handler to receive the collision event info.

		self.cTrav.addCollider(self.CN, self.cHanQ)
		# register the ray as a collider with the traverser,
		# and register the handler queue as the handler to be used for the collisions.

    def getMouseAim(self):
		#This function takes a self node and checks that node and it's children for collision with the mouse ray. It also makes
		#sure that the ray is positioned correctly and aimed at the mouse pointer.

		if base.mouseWatcherNode.hasMouse():
			#We must check to make sure the window has the mouse to prevent a crash error caused by accessing the mouse
			#when it's not in the window.

			mpos = base.mouseWatcherNode.getMouse()
			#get the mouse position in the window

			self.cRay.setFromLens(
				base.camNode, mpos.getX(), mpos.getY())
			#sets the ray's origin at the camera and directs it to shoot through the mouse cursor

			self.cTrav.traverse(render)
			#performs the collision checking pass

			self.cHanQ.sortEntries()
			# Sort the handler entries from nearest to farthest

			if(self.cHanQ.getNumEntries() > 0):
				entry = self.cHanQ.getEntry(0)
				colPoint = entry.getSurfacePoint(render)
				webView = entry.getIntoNodePath().getPythonTag("browser")
                                webView.setMouseCoords(colPoint.getX(), colPoint.getY(), colPoint.getZ())
                                if self.browser !=None and self.browser != webView:
                                    self.browser.quad.setLight(self.browser.ambientNP)
                                self.browser = webView
                                self.browser.active = True
                                if self.browser.quad.hasLight(self.browser.ambientNP):
                                    self.browser.quad.clearLight(self.browser.ambientNP)

                        else:
                                if self.browser != None:
                                    self.browser.active = False
                                if (self.browser != None and not self.browser.quad.hasLight(self.browser.ambientNP)):
                                    self.browser.quad.setLight(self.browser.ambientNP)
                                    self.browser = None



