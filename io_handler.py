from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from OpenGL.GL import shaders

class IOHandler(object):
    def __init__(self, game):
        self.game = game

    def drawScene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.game.renderer.draw()

        glutSwapBuffers()

    def timerUpdate(self, value):
        self.setupTimer()

    def keyboardPress(self, *args):
        if args[0] == '\033':
            self.game.windowManager.destroyWindow()
            sys.exit()
            self.game.player.intendRot += 1
        if args[0] == 'a':
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if args[0] == 's':
            self.game.renderer.drawBackground()
        if args[0] == 'd':
            self.game.renderer.drawAxes()
        if args[0] == 'f':
            glutSwapBuffers()

    def keyboardUpPress(self, *args):
        if args[0] == '\033':
            pass

    def mouseMotion(self, x, y):
        if x <= self.game.windowManager.width/2:
            self.game.renderer.mouseIn('before',
                (x-self.game.windowManager.width/4.)/(self.game.windowManager.width/4.),
                (self.game.windowManager.height/2.-y)/(self.game.windowManager.height/2.))

    def bindIOCalls(self):
        glutDisplayFunc(self.drawScene)

        glutIdleFunc(self.drawScene)

        glutKeyboardFunc(self.keyboardPress)
        glutKeyboardUpFunc(self.keyboardUpPress)
        glutIgnoreKeyRepeat(True)

        glutPassiveMotionFunc(self.mouseMotion)

        self.setupTimer()

    def setupTimer(self):
        glutTimerFunc(1000/60, self.timerUpdate, 0)