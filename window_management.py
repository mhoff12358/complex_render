from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class WindowManager(object):
    def __init__(self, game, width=600, height=400, windowText="_"):
        self.game = game
        self.width = width
        self.height = height
        self.windowText = windowText
        self.window = None

    def initializeWindow(self):
        glutInit('')

        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA)

        glutInitWindowSize(self.width, self.height)

        glutInitWindowPosition(0, 0)

        self.window = glutCreateWindow(self.windowText)

        glutReshapeFunc(self.resizeWindow)

        glDisable(GL_DEPTH_TEST)

    def resizeWindow(self, width=None, height=None):
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height

        glViewport(0, 0, self.width, self.height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # glFrustum(-1, 1, -1, 1, .25, 1.75)
        # gluPerspective(45.0, float(self.width)/float(self.height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def destroyWindow(self):
        glutDestroyWindow(self.window)