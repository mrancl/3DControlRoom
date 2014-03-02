from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.stdpy.file import *
from direct.gui.OnscreenImage import OnscreenImage

class Preloader:
	def __init__(self, fonts):
		self.createGraphics(fonts)

		file = open("models.txt", "r")
		self.models = file.readlines()
		file.close()
		for N in range(len(self.models)):
			self.models[N] = self.models[N].replace("\n", "")

		self.totalItems = len(self.models)

		self.loaderBar.setTexOffset(self.modTS, .015, 0)
		base.graphicsEngine.renderFrame()
		#base.graphicsEngine.renderFrame()

		self.itemCount = 0

		for M in self.models:
			item = loader.loadModel(M)
			self.itemCount += 1
			progress = self.itemCount / float(self.totalItems)
			self.loaderBar.setTexOffset(self.modTS,
				-progress  + .005, 0)
			base.graphicsEngine.renderFrame()
			#base.graphicsEngine.renderFrame()

		self.destroy()

	def createGraphics(self, fonts):
		self.modTS = TextureStage("Modulate")
		self.modTS.setMode(TextureStage.MModulate)

		self.frame = DirectFrame(frameSize = (-.3, .3, -.2, .2),
			frameColor = (1,1,1,0),
			parent = base.aspect2d)
                        
		loaderEgg = loader.loadModel("Models/EnergyBar.egg")
		self.loaderBG = loaderEgg.find("**/EnergyBG")
		self.loaderBar = loaderEgg.find("**/EnergyBar")
		self.loaderFrame = loaderEgg.find("**/EnergyFrame")
		self.loaderBG.reparentTo(self.frame)
		self.loaderBar.reparentTo(self.loaderBG)
		self.loaderFrame.reparentTo(self.loaderBG)
		self.loaderBG.setPos(0, 0, -.2)
	
		alpha = loader.loadTexture("Models/LoaderAlpha.png")
		alpha.setFormat(Texture.FAlpha)
		alpha.setWrapU(Texture.WMClamp)

		self.loaderBar.setTexture(self.modTS, alpha)

                self.image = OnscreenImage(image = 'Models2/3dcrlogo.png', pos = (0, 0, -.05), scale = (0.799,0,0.152))
                self.image.setTransparency(TransparencyAttrib.MAlpha)
		return

	def destroy(self):
		self.loaderBG.removeNode()
		self.image.destroy()
		self.frame.destroy()