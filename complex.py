from OpenGL.GL import *

import math
from itertools import *

# def calcbrightness(fraction):
	# return 1./(25*fraction+1)-1./25
def calcbrightness(fraction):
	return 1-fraction

def offsetcos(theta, shift):
	return (math.cos(theta+shift)+1)/2.
	# return math.cos(theta+shift)

def getColor(theta, brightness):
	return getTwoHue(theta, brightness)
	# return getRainbowColor(theta, brightness)

def getRainbowColor(theta, brightness):
	colortriple = (offsetcos(theta,0)*brightness,
		           offsetcos(theta,math.pi*(2./3))*brightness,
		           offsetcos(theta,math.pi*(4./3))*brightness)
	return colortriple

def getTwoHue(theta, brightness):
	theta = theta % (2*math.pi)
	colortriple = (offsetcos(theta/2., 0)*brightness,
				   0,
				   offsetcos(theta/2., math.pi)*brightness)
	return colortriple

class cnum(object):
	def callGl(self, endrad):
		self.callGlColor(endrad)
		self.callGlVertex()

	def callGlVertex(self):
		glVertex(*self.getGlVertex())

	def callGlColor(self, endrad):
		glColor(*self.getGlColor(endrad))

class cnumxy(cnum):
	def __init__(self, real, imag):
		self.real = real
		self.imag = imag

	def __add__(self, other):
		if isinstance(other, cnumxy):
			return cnumxy(self.real+other.real, self.imag+other.imag)
		elif isinstance(other, int) or isinstance(other, float):
			return cnumxy(self.real+other, self.imag)

	def toPolar(self):
		theta = math.atan2(self.imag, self.real)
		theta = (theta+2*math.pi)%(2*math.pi)
		return cnumpolar(math.pow(math.pow(self.real,2)+math.pow(self.imag,2),.5),
			             theta)

	def toPolarList(self, maxTheta):
		plist = []

		theta = math.atan2(self.imag, self.real)
		theta = (theta+2*math.pi)%(2*math.pi)
		while theta <= maxTheta:
			plist.append(cnumpolar(math.pow(math.pow(self.real,2)+math.pow(self.imag,2),.5),
			             theta))
			theta += 2*math.pi
		return plist

	def toxy(self):
		return self

	def getGlVertex(self):
		return (self.real, self.imag, -1)

	def getGlColor(self, endrad):
		return self.toPolar().getGlColor()

class cnumpolar(cnum):
	def __init__(self, radius, theta):
		self.radius = radius
		self.theta = theta

	def toPolar(self):
		return self

	def toxy(self):
		return cnumxy(self.radius*math.cos(self.theta), self.radius*math.sin(self.theta))

	def getGlVertex(self):
		return self.toxy().getGlVertex()

	def getGlColor(self, endrad):
		return getColor(self.theta, calcbrightness(float(self.radius)/endrad))


class MappedComplex(cnum):
	def __init__(self, cin, mapstack):
		self.cin = cin
		self.mapstack = mapstack
		self.cout = self.cin
		for m in self.mapstack:
			self.cout = m(self.cout)

	def getGlColor(self, endrad):
		return self.cin.getGlColor(endrad)

	def getGlVertex(self):
		return self.cout.getGlVertex()


class PolarComplexField(object):
	def __init__(self, maxRad=1, numRad=1,
		               maxTheta=2*math.pi, numTheta=4):
		self.maxRad = maxRad
		self.numRad = numRad
		self.maxTheta = maxTheta
		self.numTheta = numTheta

		self.cycles = []
		for i in range(self.numRad+1):
			newcycle = []
			newrad = float(self.maxRad*i)/self.numRad
			for j in range(self.numTheta+1):
				newcycle.append(self.newPoint(cnumpolar(newrad, float(self.maxTheta*j)/self.numTheta)))
			self.cycles.append(newcycle)

		self.points = []

	def newPoint(self, cnp):
		return cnp

	def renderPoints(self, cnps):
		self.points = map(lambda x:self.newPoint(x), cnps)

	def draw(self):
		self.drawPoints()
		self.drawField()

	def drawField(self):
		for cyclestrip in range(len(self.cycles)-1):
			glBegin(GL_QUAD_STRIP)
			for i in range(len(self.cycles[cyclestrip])):
				self.cycles[cyclestrip][i].callGl(1)
				self.cycles[cyclestrip+1][i].callGl(1)
			self.cycles[cyclestrip][0].callGl(1)
			self.cycles[cyclestrip+1][0].callGl(1)
			glEnd()

	def drawPoints(self):
		for point in self.points:
			(x, y, z) = point.getGlVertex()
			glColor(1, 1, 1)
			glBegin(GL_QUADS)
			glVertex(x-.01, y-.01, z)
			glVertex(x+.01, y-.01, z)
			glVertex(x+.01, y+.01, z)
			glVertex(x-.01, y+.01, z)
			glEnd()
		


class PolarComplexMappedField(PolarComplexField):
	def newPoint(self, cnp):
		m = [lambda x: cnumpolar(math.pow(x.radius, .5), x.theta/2.)]
		return MappedComplex(cnp, m)
