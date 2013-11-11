#!/usr/bin/env python

#Imports!
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from OpenGL.GL import shaders

from window_management import WindowManager
from io_handler import IOHandler
from renderer import Renderer

class Game(object):
    def __init__(self):
        self.windowManager = WindowManager(self, width=1200, height=600)
        self.ioHandler = IOHandler(self)
        self.renderer = Renderer(self)

        self.windowManager.initializeWindow()
        self.ioHandler.bindIOCalls()

        self.bootstrapGL()        

        glutMainLoop() 

    def bootstrapGL(self):
        glClearColor(0.392, 0.584, 0.929, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_NEVER)
        # glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

if __name__ == "__main__":
    g = Game()