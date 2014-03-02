import direct.directbase.DirectStart
from pandac.PandaModules import *

from CameraControl_11 import Camera
from InputManagerClass_05 import InputManager
from RoomClass import Room
from MenuClass_05 import Menu
from WebCamClass import WebCamMonitor
from PawesomiumClass_07 import HtmlView
from pawesomium import *
from PreloaderClass import Preloader


class World:
    def __init__(self):
        base.disableMouse()
        base.setBackgroundColor(0, 0, 0)
        render.setLightOff()
        self.inputManager = InputManager()
        self.cam = Camera(self.inputManager)

        self.menuGraphics = loader.loadModel(
			"Gui/MenuGraphics.egg")

        self.menuButton = loader.loadModel(
			"Gui/button.egg")

	self.fonts = {
			"silver" : loader.loadFont("Fonts/LuconSilver.egg"),
			"blue" : loader.loadFont("Fonts/LuconBlue.egg"),
                        "times" : loader.loadFont("Fonts/times.egg")}

        preloader = Preloader(self.fonts)
        self.room = Room()

        self.webCore = WebCore(LogLevel.LOG_VERBOSE, True, PixelFormat.PF_BGRA)
        self.htmlview1 = HtmlView(self.webCore, "web1", "", -26.445, 5.30, 68.046, 43.50, 2.74, 0)
        self.htmlview2 = HtmlView(self.webCore, "web2", "", -2.11, 24.95, 68.02, 35.13, 2.74, 0)
        self.htmlview3 = HtmlView(self.webCore, "web3", "", 24.837, 41.1, 68.021, 26.89, 2.74 , 0)
        self.htmlview4 = HtmlView(self.webCore, "web4", "", -25.123, 4.18, 48.081, 43.56 ,346.49 , 0)
        self.htmlview5 = HtmlView(self.webCore, "web5", "", -1.171, 23.632, 48.056, 35.06, 346.49, 0)

        self.startOptions = {}
        try:
            f = open('options.txt', 'r')
            self.startOptions = eval(f.read())
        except:
            self.options = open('options.txt', 'w')

        self.createStartMenu()

    def createStartMenu(self):
         self.menu = Menu(self.menuGraphics, self.fonts, self.menuButton, self)
         self.menu.initMenu([0, None,
                       ["Screen 1", "Screen 2", "Screen 3", "Screen 4", "Screen 5", "WebCam", "Start", "Help"],
                       [[None],
                       [None],
                       [None],
                       [None],
                       [None],
                       [self.startWebcam],
                       [self.startSession],
                       [None]],
                       [[None], [None], [None], [None], [None], [None], [None], [None]]])

    def startSession(self):
            self.menu.hide()
            taskMgr.add(self.cam.cameraControl, "Camera Control")
            self.optionsFile = open('options.txt', 'w')
            self.optionsFile.write(str(self.menu.options))
            self.optionsFile.close()

    def startWebcam(self):
            self.webcam = WebCamMonitor(25.58, 39.7, 48.06, 26.56, 346.49,0)


w = World()
run()