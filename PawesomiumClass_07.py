import array, sys, string

import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

from pawesomium import *

WIDTH = 835 #835,512
HEIGHT = 512
SCALE = 10.6

class HtmlView(DirectObject, WebViewListener):
    def __init__(self, webCore, name, htmlFile, x=0.0, y=0.0, z=0.0, h=0, p=0, r=0):

        WebViewListener.__init__(self)
        self.webCore = webCore
        self.name = name
        self.quad = None
        self.active = False
        # set position
        self.x = x
        self.y = y
        self.z = z

        # my light
        self.ambientNP = None

        # set rotation
        self.h = h
        self.p = p
        self.r = r

        # Mouse coordinates
        self.mouseX = 0.0
        self.mouseY = 0.0
        self.mouseZ = 0.0
        # black background suits better in our case
        base.win.setClearColor(Vec4(0.0, 0.0, 0.0, 1.0))

        self.htmlFile = htmlFile
        self.transparency = False
        dt = globalClock.getDt()

        self.webView = self.webCore.createWebView(WIDTH, HEIGHT, self.transparency, False, 70)
        self.webView.setListener(self)
        self.webView.setCallback("requestFPS");
        self.history = []

        self.imgBuffer = array.array('B')
        for i in xrange(WIDTH*HEIGHT):
            self.imgBuffer.append(0)
            self.imgBuffer.append(0)
            self.imgBuffer.append(0)
            self.imgBuffer.append(255)

        textClipboard = ""
        self.setupEventsHandling()
        self.setupTexture()

        #self.accept("escape", sys.exit, [0])
        #self.accept("w", self.writeTex)

    def setupEventsHandling(self):

        self.webView.setCallback("setTextClipboard")

        self.accept("mouse1", self.mouseDown, [MouseButton.LEFT_MOUSE_BTN])
        self.accept("mouse3", self.mouseDown, [MouseButton.RIGHT_MOUSE_BTN])
        self.accept("mouse1-up", self.mouseUp, [MouseButton.LEFT_MOUSE_BTN])
        self.accept("mouse3-up", self.mouseUp, [MouseButton.RIGHT_MOUSE_BTN])

        base.buttonThrowers[0].node().setButtonDownEvent('buttonDown')
        base.buttonThrowers[0].node().setButtonRepeatEvent('keyrepeat')
        base.buttonThrowers[0].node().setKeystrokeEvent('keystroke')

        self.accept('buttonDown', self.buttonHandler)
        self.accept('keyrepeat', self.buttonHandler)
        self.accept('keystroke', self.keystrokeHandler)

        taskMgr.add(self.update, 'UpdateTask')


    def setupTexture(self):
        cm = CardMaker('quadMaker')
        cm.setColor(1.0, 1.0, 1.0, 1.0)

        aspect = base.camLens.getAspectRatio()
        htmlWidth = 2.0 * aspect * WIDTH / base.win.getXSize()
        htmlHeight = 2.0 * HEIGHT / base.win.getYSize()
        # the html area will be center aligned and vertically top aligned
        cm.setFrame(-htmlWidth/2.0, htmlWidth/2.0, -htmlHeight/2, htmlHeight/2)
        card = cm.generate()
        self.quad = NodePath(card)
        #self.quad.reparentTo(aspect2d)
        self.quad.reparentTo(render)

        self.guiTex = Texture("guiTex")
        self.guiTex.setupTexture(Texture.TT2dTexture, WIDTH, HEIGHT, 1, Texture.TUnsignedByte, Texture.FRgba)
        self.guiTex.setKeepRamImage(True)
        self.guiTex.makeRamImage()
        self.guiTex.setWrapU(Texture.WMRepeat)
        self.guiTex.setWrapV(Texture.WMRepeat)

        ts = TextureStage('webTS')
        self.quad.setTexture(ts, self.guiTex)
        self.quad.setTexScale(ts, 1.0, -1.0)

        self.quad.setTransparency(0)
        self.quad.setTwoSided(True)
        self.quad.setColor(1.0, 1.0, 1.0, 1.0)

        # My settings
        self.quad.setScale(SCALE)
        self.quad.setPos(self.x,self.y,self.z)

        mask = BitMask32.bit(8)
        self.quad.setCollideMask(mask)

        self.quad.setPythonTag("browser", self)

        self.quad.setHpr(self.h, self.p, self.r)

        ambient = AmbientLight('ambient')
        ambient.setColor(Vec4(0.6, 0.6, 0.6, 1))
        self.ambientNP = self.quad.attachNewNode(ambient)
        self.quad.setLightOff()
        self.quad.setLight(self.ambientNP)

        # Pivot Node
        self.pivot = render.attachNewNode("Pivot")

    def mouseDown(self, button):
        if self.active != False:
            self.webView.injectMouseDown(button)

    def mouseUp(self, button):
        self.webView.injectMouseUp(button)

    def goBack(self):
        if (len(self.history) > 1):
            #print self.history
            del self.history[len(self.history) - 1]
            #print self.history
            backURL = self.history.pop()
            #print backURL
            if (backURL.find('http')!= -1):
                self.webView.loadURL(backURL, '', '', '')
            elif (backURL.find('file')!= -1):
                self.webView.loadFile(self.htmlFile, '')
        elif (len(self.history) == 1):
            backURL = self.history.pop()
            if (backURL.find('http')!= -1):
                self.webView.loadURL(backURL, '', '', '')
            elif (backURL.find('file')!= -1):
                self.webView.loadFile(self.htmlFile, '')

    def toggleTransparency(self):
        self.transparency = not self.transparency
        self.webView.setTransparent(self.transparency)

    def update(self, task):
        if base.mouseWatcherNode.hasMouse():
            x, y = self._translateRelativeCoordinates()
            self.webView.injectMouseMove(x, y)

        if self.webView.isDirty():
            self.webView.render(self.imgBuffer.buffer_info()[0], WIDTH*4, 4, 0)
            textureBuffer = self.guiTex.modifyRamImage()
            textureBuffer.setData(self.imgBuffer.tostring())


        self.webCore.update()
        return Task.cont


    def _translateRelativeCoordinates(self):
        '''
        Surface coordinates are passed to Pivot Node to be
        converted in CardMaker own system coordinates.
        Simple transformation is made to get pixels.
        '''
        aspect = base.camLens.getAspectRatio()
        w = 2.0 * aspect * WIDTH / base.win.getXSize()
        h = 2.0 * HEIGHT / base.win.getYSize()
        self.pivot.setPos(self.mouseX, self.mouseY, self.mouseZ)
        pct = self.pivot.getPos(self.quad)
        webX = int(WIDTH * (pct.getX() + w/2) / w)
        webY = int(HEIGHT * (h/2 - pct.getZ()) / h)
        return webX, webY

    def setMouseCoords(self, mx, my, mz):
        self.mouseX = mx
        self.mouseY = my
        self.mouseZ = mz
    # --------------------[ WebViewListener implementation ]--------------------------
    def onCallback(self, name, args):
        if name == "requestFPS":
            self.webView.setProperty( "fps", JSValue("%.1f" % (1.0 / globalClock.getDt())) )
            self.webView.executeJavascript("updateFPS()", "")

    def onBeginNavigation(self, url,  frameName):
        pass

    def onBeginLoading(self, url, frameName, statusCode, mimeType):
        self.history.append(url)
        #pass

    def onFinishLoading(self):
        pass

    def onReceiveTitle(self, title, frameName):
        pass

    def onChangeTooltip(self, tooltip):
        pass

    def onChangeCursor(self, cursor):
        pass

    def onChangeKeyboardFocus(self, isFocused):
        pass

    def onChangeTargetURL(self, url):
        pass

    def buttonHandler(self, event):
        if self.active != False:
            if event == "backspace":
                self.webView.setProperty("depressedKey", JSValue("backspace"))
                JScmd = "inputField = document.activeElement; " +\
                "if (inputField.nodeName == 'TEXTAREA'){ " +\
                "initialCursorPosition = inputField.selectionStart; "  +\
                "textEnd = inputField.innerHTML.substring(inputField.selectionEnd); " +\
                "characterToInsert = Client.depressedKey; " +\
                "if(Client.depressedKey == 'backspace'){ " +\
                "characterToInsert = ''; " +\
                "if(inputField.selectionEnd - inputField.selectionStart > 0){ " +\
                "textStart = inputField.innerHTML.substring(0, inputField.selectionStart); " +\
                "newCursorPosition = initialCursorPosition; " +\
                "} " +\
                "else { " +\
                "textStart = inputField.innerHTML.substring(0, inputField.selectionStart-1); " +\
                "newCursorPosition = initialCursorPosition - 1; " +\
                "} " +\
                "} " +\
                "inputField.innerHTML = textStart + characterToInsert + textEnd; " +\
                "inputField.selectionStart = inputField.selectionEnd = newCursorPosition; " +\
                "document.activeElement.style.backgroundColor = 'moccasin'; " +\
                "} " +\
                "else if (inputField.nodeName == 'INPUT' && (inputField.getAttribute('type').toLowerCase() == 'text' || inputField.getAttribute('type').toLowerCase() == 'password' || inputField.getAttribute('type').toLowerCase() == 'search')){  " +\
                "initialCursorPosition = inputField.selectionStart; "  +\
                "textEnd = inputField.value.substring(inputField.selectionEnd); " +\
                "characterToInsert = Client.depressedKey; " +\
                "if(Client.depressedKey == 'backspace'){ " +\
                "characterToInsert = ''; " +\
                "if(inputField.selectionEnd - inputField.selectionStart > 0){ " +\
                "textStart = inputField.value.substring(0, inputField.selectionStart); " +\
                "newCursorPosition = initialCursorPosition; " +\
                "} " +\
                "else { " +\
                "textStart = inputField.value.substring(0, inputField.selectionStart-1); " +\
                "newCursorPosition = initialCursorPosition - 1; " +\
                "} " +\
                "} " +\
                "inputField.value = textStart + characterToInsert + textEnd; " +\
                "inputField.selectionStart = inputField.selectionEnd = newCursorPosition; " +\
                "document.activeElement.style.backgroundColor = 'moccasin'; " +\
                "} "
                self.webView.executeJavascript(JScmd, "")

            elif event.startswith("arrow_"):
                if event == "arrow_right":
                    self.webView.setProperty("cursorShift", JSValue(1))
                    self.webView.executeJavascript("moveCursor()", "")

                elif event == "arrow_left":
                    self.webView.setProperty("cursorShift", JSValue(-1))
                    self.webView.executeJavascript("moveCursor()", "")

                elif event == "arrow_up":
                    self.webView.setProperty("cursorShift", JSValue(-1))
                    self.webView.executeJavascript("moveCursorOneLine()", "")

                elif event == "arrow_down":
                    self.webView.setProperty("cursorShift", JSValue(1))
                    self.webView.executeJavascript("moveCursorOneLine()", "")

            elif event.startswith("shift-arrow_"):
                if event == "shift-arrow_right":
                    self.webView.setProperty("selectionEndShift", JSValue(1))
                    self.webView.executeJavascript("moveSelectionEnd()", "")

                elif event == "shift-arrow_left":
                    self.webView.setProperty("selectionEndShift", JSValue(-1))
                    self.webView.executeJavascript("moveSelectionEnd()", "")

                elif event == "shift-arrow_up":
                    self.webView.setProperty("selectionEndShift", JSValue(-1))
                    self.webView.executeJavascript("moveSelectionEndOneLine()", "")

                elif event == "shift-arrow_down":
                    self.webView.setProperty("selectionEndShift", JSValue(1))
                    self.webView.executeJavascript("moveSelectionEndOneLine()", "")


    legalCharacters = string.letters + string.digits + string.punctuation + string.whitespace
    def keystrokeHandler(self, event):
        if self.active != False:
            if event in self.legalCharacters:
                self.webView.setProperty("depressedKey", JSValue(str(event)))
                JScmd = "inputField = document.activeElement; " + \
                "if (inputField.nodeName == 'TEXTAREA'){ " + \
                "initialCursorPosition = inputField.selectionStart; " + \
                "textEnd = inputField.innerHTML.substring(inputField.selectionEnd); " + \
                "characterToInsert = Client.depressedKey; " + \
                "if(Client.depressedKey != 'backspace'){ " + \
                "textStart = inputField.innerHTML.substring(0, inputField.selectionStart); " + \
                "newCursorPosition = initialCursorPosition + 1; " + \
                "} " +\
                "inputField.innerHTML = textStart + characterToInsert + textEnd; " + \
                "inputField.selectionStart = inputField.selectionEnd = newCursorPosition; " + \
                "document.activeElement.style.backgroundColor = 'moccasin'; " + \
                "} " +\
                "else if (inputField.nodeName == 'INPUT' && (inputField.getAttribute('type').toLowerCase() == 'text' || inputField.getAttribute('type').toLowerCase() == 'password' || inputField.getAttribute('type').toLowerCase() == 'search')){  " +\
                "initialCursorPosition = inputField.selectionStart; " + \
                "textEnd = inputField.value.substring(inputField.selectionEnd); " + \
                "characterToInsert = Client.depressedKey; " + \
                "if(Client.depressedKey != 'backspace'){ " + \
                "textStart = inputField.value.substring(0, inputField.selectionStart); " + \
                "newCursorPosition = initialCursorPosition + 1; " + \
                "} " +\
                "inputField.value = textStart + characterToInsert + textEnd; " + \
                "inputField.selectionStart = inputField.selectionEnd = newCursorPosition; " + \
                "document.activeElement.style.backgroundColor = 'moccasin'; " + \
                "} "
                self.webView.executeJavascript(JScmd, "")
