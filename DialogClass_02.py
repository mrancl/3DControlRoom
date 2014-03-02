from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText

class Dialog:
	def __init__(self, menuGraphics, fonts, menu, menuButton):

		self.menuGraphics = menuGraphics
                self.menuButton = menuButton
		self.fonts = fonts
		self.self = self
                self.menu = menu
                self.links = {}
                links = open('links.txt', 'r')
                for line in links:
                    (key, val) = line.split()
                    self.links[key] = val
                self.keys = self.links.keys()
                self.pressed = False

	def initMenu(self, args):
		type = args[0]
		if(args[1] != None):
			self.title = args[1]
		else:
			self.title = None
		self.items = args[2]
		self.buttons = []

		if(type == 3):
			self.frame = DirectFrame(
				geom = self.menuGraphics.find("**/menu3"),
				relief = None, scale = (1.5,1,1.5),
				frameColor = (1,1,1,.75), parent = base.aspect2d)
			framePadding = .1

			height = self.frame.getHeight()/2 - framePadding

			self.title = DirectLabel(text = self.title,
				text_font = self.fonts["times"], text_fg = (1,1,1,.75),
				relief = None, text_align = TextNode.ACenter,
				text_scale = .05, parent = self.frame,
				pos = (-.025,0,height+0.05))
                        if self.title["text"].startswith('Screen'):
                            if self.menu.world.startOptions.has_key(self.title["text"]):
                                self.active = [self.menu.world.startOptions[self.title["text"]]]
                            else:
                                self.active = [0]
                            for N in range(len(self.items)):
                                    xPos = -.3
                                    zPos = -(height / (2)) * N + 0.1
                                    if len(self.buttons)>=5:
                                        xPos = 0.15
                                        zPos = self.buttons[N-5]["pos"][2]
                                    self.buttons.append(DirectRadioButton(
                                            variable = self.active, value = [N], scale = 0.045,
                                            text = self.keys[N], text_font = self.fonts["times"],
                                            boxPlacement = 'left',
                                            text_fg = (1,1,1,.75),
                                            text_pos=(0,0),
                                            text_align = TextNode.ALeft,
                                            relief = None,
                                            clickSound = None,
                                            #rolloverSound = None,
                                            parent = self.frame,
                                            pos = (xPos, 0, zPos)))

                            for button in self.buttons:
                                    button.setOthers(self.buttons)

                            b = DirectButton(
                                            command = self.loadWebView,
                                            text = "OK",
                                            text_font = self.fonts["blue"],
                                            text_fg = (1,1,1,1),
                                            text_scale=(0.04,0.04),
                                            text_pos=(0,-0.01),
                                            text_align = TextNode.ACenter,
                                            geom = (self.menuButton.find("**/normal"),
                                                            self.menuButton.find("**/clicked"),
                                                            self.menuButton.find("**/hoover")),
                                            geom_scale = (1,1,1.5),
                                            relief = None, clickSound = None,
                                            rolloverSound = None, parent = self.frame,
                                            pos = (0, 0, -.16))
                        else:
                            self.help = OnscreenText(text = 'f1 - URL reload\
                                                        \nf2 - Zoom in on display\
                                                        \nf3 - Toggle menu\
                                                        \narrow keys - Navigation',
                                                font = self.fonts["times"],
                                                fg = (1,1,1,.75),
                                                pos = (-0.37, 0.09),
                                                scale = 0.045,
                                                align = TextNode.ALeft,
                                                parent = self.frame)
                                                
                            self.close = DirectButton(
                                            command = self.destroyHelp,
                                            text = "Close",
                                            text_font = self.fonts["blue"],
                                            text_fg = (1,1,1,1),
                                            text_scale=(0.04,0.04),
                                            text_pos=(0,-0.01),
                                            text_align = TextNode.ACenter,
                                            geom = (self.menuButton.find("**/normal"),
                                                            self.menuButton.find("**/clicked"),
                                                            self.menuButton.find("**/hoover")),
                                            geom_scale = (1,1,1.5),
                                            relief = None, clickSound = None,
                                            rolloverSound = None, parent = self.frame,
                                            pos = (0, 0, -.16))

		return

        def loadWebView(self):
                if self.title["text"] == "Screen 1":
                    key = self.buttons[self.active[0]]["text"]
                    self.menu.world.htmlview1.webView.loadURL(self.links[key], '', '', '')
                    self.menu.world.htmlview1.htmlFile = self.links[key]
                elif self.title["text"] == "Screen 2":
                    key = self.buttons[self.active[0]]["text"]
                    self.menu.world.htmlview2.webView.loadURL(self.links[key], '', '', '')
                    self.menu.world.htmlview2.htmlFile = self.links[key]
                elif self.title["text"] == "Screen 3":
                    key = self.buttons[self.active[0]]["text"]
                    self.menu.world.htmlview3.webView.loadURL(self.links[key], '', '', '')
                    self.menu.world.htmlview3.htmlFile = self.links[key]
                elif self.title["text"] == "Screen 4":
                    key = self.buttons[self.active[0]]["text"]
                    self.menu.world.htmlview4.webView.loadURL(self.links[key], '', '', '')
                    self.menu.world.htmlview4.htmlFile = self.links[key]
                elif self.title["text"] == "Screen 5":
                    key = self.buttons[self.active[0]]["text"]
                    self.menu.world.htmlview5.webView.loadURL(self.links[key], '', '', '')
                    self.menu.world.htmlview5.htmlFile = self.links[key]
                self.menu.options[self.title["text"]] = self.active[0]
                self.destroyScreen()

	def destroyScreen(self):
		for N in range(len(self.items)):
			self.buttons[0].destroy()
		if(self.title != None):
			self.title.destroy()
		self.frame.destroy()
		self.self = None
		return

        def destroyHelp(self):
                self.close.destroy()
                self.help.destroy()
                self.title.destroy()
                self.frame.destroy()