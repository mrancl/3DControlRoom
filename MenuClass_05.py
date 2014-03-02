from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from DialogClass_02 import Dialog

class Menu(DirectObject):
	def __init__(self, menuGraphics, fonts, menuButton, world):

		self.menuGraphics = menuGraphics
                self.menuButton = menuButton
		self.fonts = fonts
                self.world = world
		self.self = self
                self.mVisible = True
                self.accept("f3", self.toggle)
                self.options = {}

                base.camera.setPos(83.092, -150.189, 70.776)
                base.camera.setHpr(24.875, -6.25, 0)

	def initMenu(self, args):
		type = args[0]
		if(args[1] != None):
			self.title = args[1]
		else:
			self.title = None
		self.items = args[2]
                self.funcs = args[3]
                self.funcArgs = args[4]
		self.buttons = []

		if(type == 0):

			self.frame = DirectFrame(
				geom = self.menuGraphics.find("**/menu0"),
                                relief = None,
				scale = (1.5,1,1.5), frameColor = (1,1,1,.75),
				pos = (.2625,0,.45125), parent = base.a2dBottomLeft)

			framePadding = .1

			height = self.frame.getHeight() - framePadding

			for N in range(len(self.items)):

				xPos = 0
				zPos = height/2 - (height / (len(self.items))) * N -0.05

				self.buttons.append(DirectButton(
					command = self.activateDialog, extraArgs = [N],
					geom = (self.menuButton.find("**/normal"),
							self.menuButton.find("**/clicked"),
							self.menuButton.find("**/hoover")),
                                        geom_scale = (1,1,1.5),
					relief = None, clickSound = None,
					rolloverSound = None, parent = self.frame,
					pos = (xPos, 0, zPos)))

				self.items[N] = DirectLabel(text = self.items[N],
				text_font = self.fonts["times"],
				text_fg = (0,0,0,1), relief = None, text_pos = (0,.005),
				text_align = TextNode.ACenter, text_scale = .035,
				parent = self.buttons[N])

				self.items[N].setPos(0,0,-self.items[N].getHeight()/2)

		return

	def activateDialog(self, item):
                if self.items[item]["text"].startswith('Screen'):
                    dialog = Dialog(self.menuGraphics, self.fonts, self, self.menuButton)
                    dialog.initMenu([3, self.items[item]["text"],
                            [None, None, None, None, None, None, None, None, None]])
                elif self.items[item]["text"] == 'Help':
                    dialog = Dialog(self.menuGraphics, self.fonts, self, self.menuButton)
                    dialog.initMenu([3, self.items[item]["text"],[None]])
                else:
                    if(type(self.funcs[item]) == list):

			for N in range(len(self.funcs[item])):
				if(self.funcArgs[item][N] != None):
					self.funcs[item][N](self.funcArgs[item][N])
				else:
					self.funcs[item][N]()

                    else:
                        if(self.funcArgs[item] != None):
				self.funcs[item](self.funcArgs[item])
			else:
				self.funcs[item]()

		#self.destroy()
		return
		

	def destroy(self):
		for N in range(len(self.items)):
			#self.items[0].destroy()
			self.buttons[0].destroy()
		if(self.title != None):
			self.title.destroy()
		self.frame.destroy()

		self.self = None

		return

        def getVisible(self):
            return self.mVisible

        def hide(self):
            self.mVisible=False
            for N in range(len(self.items)):
		#self.items[0].hide()
		self.buttons[0].hide()
            if(self.title != None):
		self.title.hide()
            self.frame.hide()

        def show(self):
            self.mVisible=True
            for N in range(len(self.items)):
		self.buttons[0].show()
            if(self.title != None):
		self.title.show()
            self.frame.show()
            taskMgr.remove("Camera Control")

        def toggle(self):
            self.getVisible()
            if self.mVisible:
                self.hide()
            else:
                self.show()
       