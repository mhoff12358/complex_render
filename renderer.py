from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from OpenGL.GL import shaders

from complex import PolarComplexField, PolarComplexMappedField, cnumxy
import math

# pcf = PolarComplexField(numRad = 20, numTheta = 100)
# pcmf = PolarComplexMappedField(numRad = 20, numTheta = 100, maxTheta = 4*math.pi)

class Renderer(object):
	def __init__(self, game):
		self.game = game
		self.startingPCF = PolarComplexField(numRad = 20, numTheta = 100)
		self.mappedPCF = PolarComplexMappedField(numRad = 20, numTheta = 100, maxTheta = 4*math.pi)

	def draw(self):
		self.drawAxes()

		glPushMatrix()
		glTranslate(-.5, 0, 0)
		glScale(.5, 1, 1)
		self.startingPCF.draw()
		glPopMatrix()
		glPushMatrix()
		glTranslate(.5, 0, 0)
		glScale(.5, 1, 1)
		self.mappedPCF.draw()
		glPopMatrix()

		self.drawBackground()

	def drawBackground(self):
		glColor(0, 0, 0)
		glBegin(GL_QUADS)
		glVertex(-1, -1, -1)
		glVertex(1, -1, -1)
		glVertex(1, 1, -1)
		glVertex(-1, 1, -1)
		glEnd()

	def drawAxes(self):
		glColor(1,1,1)
		glBegin(GL_LINES)
		glVertex(-1, 0, -1)
		glVertex(1, 0, -1)
		glVertex(0, -1, -1)
		glVertex(0, 1, -1)
		glEnd()

	def mouseIn(self, section, x, y):
		self.startingPCF.renderPoints([cnumxy(x, y).toPolar()])
		self.mappedPCF.renderPoints(cnumxy(x, y).toPolarList(4*math.pi))