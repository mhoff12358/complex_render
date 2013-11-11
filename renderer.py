from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from OpenGL.GL import shaders

from complex import *
import math, functools

# pcf = PolarComplexField(numRad = 20, numTheta = 100)
# pcmf = PolarComplexMappedField(numRad = 20, numTheta = 100, maxTheta = 4*math.pi)

def oneoverz(z):
	z = z.toPolar()
	if z.radius == 0:
		return cnumpolar(5000, -1*z.theta)
	else:
		return cnumpolar(1.0/z.radius, -1*z.theta)

def zsquared(z):
	z = z.toPolar()
	return cnumpolar(math.pow(z.radius, 2), 2*z.theta)

def joukowsky(z):
	return z + cnumpolar(1, 0)/z

def addjoukowskyfoil(shapes, radius, theta):
	shapes.append(Shape(start_t = 0, end_t = 2*math.pi, num_t = 100, pointGenerator=functools.partial(lambda x, r, t: cnumpolar(r, x)+cnumxy(1-r*math.cos(t), math.sin(t)), r=radius, t=theta)))

class Renderer(object):
	def __init__(self, game):
		self.game = game

		self.toDraw = {"axes":1, "shapes":1, "graph":1}

		self.mapOptions = [
		{"name":"unitcircle", "maps":[], "shapes":[], "windowScalePre":1, "windowScalePost":1,
		 "pcfKwargs":{"numRad":20, "minRad":0, "maxRad":1, "numTheta":100},
		 "mapKwargs":{"numRad":20, "minRad":0, "maxRad":1, "numTheta":100, "maxTheta":2*math.pi}},
		{"name":"oneoverz", "maps":[oneoverz], "shapes":[], "windowScalePre":2, "windowScalePost":2,
		 "pcfKwargs":{"numRad":20, "minRad":0, "maxRad":2, "numTheta":100},
		 "mapKwargs":{"numRad":20, "minRad":0, "maxRad":2, "numTheta":100, "maxTheta":2*math.pi}},
		{"name":"zsquared", "maps":[zsquared], "shapes":[], "windowScalePre":3, "windowScalePost":9,
		 "pcfKwargs":{"numRad":20, "minRad":0, "maxRad":3, "numTheta":100},
		 "mapKwargs":{"numRad":20, "minRad":0, "maxRad":9, "numTheta":100, "maxTheta":math.pi}},
		{"name":"joukowskyinner", "maps":[joukowsky], "shapes":[], "windowScalePre":1, "windowScalePost":10,
		 "pcfKwargs":{"numRad":20, "minRad":0, "maxRad":1, "numTheta":100},
		 "mapKwargs":{"numRad":20, "minRad":0, "maxRad":1, "numTheta":100, "maxTheta":2*math.pi}},
		{"name":"joukowskyouter", "maps":[joukowsky], "shapes":[], "windowScalePre":5, "windowScalePost":5,
		 "pcfKwargs":{"numRad":20, "minRad":1, "maxRad":5, "numTheta":100},
		 "mapKwargs":{"numRad":20, "minRad":1, "maxRad":5, "numTheta":100, "maxTheta":2*math.pi}},
		]

		self.assignMap(0)

	def assignMap(self, newIndex):
		self.mapIndex = newIndex % len(self.mapOptions)
		self.map = self.mapOptions[self.mapIndex]
		self.startingPCF = PolarComplexField(**self.map["pcfKwargs"])
		self.mappedPCF = PolarComplexMappedField(mapFns = self.map["maps"], **self.map["mapKwargs"])
		# self.shapes = [Shape(start_t=0, end_t=9, num_t=100, pointGenerator=lambda x: cnumxy(x+1, 0)),
		# Shape(start_t=0, end_t=9, num_t=100, pointGenerator=lambda x: cnumxy(1, x), color=(1,1,1))]
		self.shapes = []
		addjoukowskyfoil(self.shapes, 1.25, .2)

	def incrementMap(self):
		self.assignMap(self.mapIndex+1)

	def decrementMap(self):
		self.assignMap(self.mapIndex-1)
	
	def draw(self):
		self.drawBackground()

		glPushMatrix()
		glTranslate(.5, 0, 0)
		self.drawBackground()
		glScale(.5/self.map["windowScalePost"], 1.0/self.map["windowScalePost"], 1)
		self.drawGraph(True)
		self.drawAxes(self.map["windowScalePost"])
		self.drawShapes(True)
		glPopMatrix()
		glPushMatrix()
		glTranslate(-.5, 0, 0)
		self.drawBackground()
		glScale(.5/self.map["windowScalePre"], 1.0/self.map["windowScalePre"], 1)
		self.drawGraph(False)
		self.drawAxes(self.map["windowScalePre"])
		self.drawShapes(False)
		glPopMatrix()


	def drawBackground(self):
		glPushMatrix()
		glScale(.5, 1, 1)
		glBegin(GL_QUADS)
		glColor(0, 0, 0)
		glVertex(-1, -1, .5)
		glVertex(1, -1, .5)
		glVertex(1, 1, .5)
		glVertex(-1, 1, .5)
		glEnd()
		glPopMatrix()

	def drawGraph(self, mapped=False):
		if self.toDraw["graph"]:
			if mapped:
				self.mappedPCF.draw(self.map["windowScalePost"])
			else:
				self.startingPCF.draw(self.map["windowScalePre"])

	def drawShapes(self, mapped=False):
		if self.toDraw["shapes"]:
			if mapped:
				for s in self.shapes:
					s.drawPoints(self.map["maps"])
			else:
				for s in self.shapes:
					s.drawPoints()
			
	def drawAxes(self, scale):
		if self.toDraw["axes"]:
			glColor(1,1,1)
			glBegin(GL_LINES)
			glVertex(-scale, 0, -1)
			glVertex(scale, 0, -1)
			glVertex(0, -scale, -1)
			glVertex(0, scale, -1)
			for i in range(scale):
				glVertex(-.1, i, -1)
				glVertex(.1, i, -1)
				glVertex(-.1, -i, -1)
				glVertex(.1, -i, -1)
				glVertex(i, -.1, -1)
				glVertex(i, .1, -1)
				glVertex(-i, -.1, -1)
				glVertex(-i, .1, -1)
			glEnd()

	def mouseIn(self, section, x, y):
		self.startingPCF.renderPoints([cnumxy(x*self.map["windowScalePre"], y*self.map["windowScalePre"]).toPolar()])
		self.mappedPCF.renderPoints(cnumxy(x*self.map["windowScalePre"], y*self.map["windowScalePre"]).toPolarList(4*math.pi))