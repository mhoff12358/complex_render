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

	def __add__(self, other):
		if isinstance(other, cnum):
			this = self.toxy()
			other = other.toxy()
			return cnumxy(this.real+other.real, this.imag+other.imag)
		elif isinstance(other, int) or isinstance(other, float):
			return cnumxy(this.real+other, this.imag)

	def __div__(self, other):
		this = self.toPolar()
		if isinstance(other, cnum):
			other = other.toPolar()
			if other.radius == 0:
				return cnumpolar(5000, this.theta-other.theta)
			return cnumpolar(this.radius/other.radius, this.theta-other.theta)
		elif isinstance(other, int) or isinstance(other, float):
			if other == 0:
				return cnumpolar(5000, this.theta)
			return cnumpolar(this.radius/other, this.theta)

class cnumxy(cnum):
	def __init__(self, real, imag):
		self.real = real
		self.imag = imag

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

	def toxy(self):
		return self.cout.toxy()

	def toPolar(self):
		return self.cout.toPolar()

	def getGlColor(self, endrad):
		return self.cin.getGlColor(endrad)

	def getGlVertex(self):
		return self.cout.getGlVertex()


class PolarComplexField(object):
	def __init__(self, minRad = 0, maxRad=1, numRad=1,
		               maxTheta=2*math.pi, numTheta=4):
		self.minRad = minRad
		self.maxRad = maxRad
		self.numRad = numRad
		self.maxTheta = maxTheta
		self.numTheta = numTheta

		self.cycles = []
		for i in range(self.numRad+1):
			newcycle = []
			newrad = float((self.maxRad-self.minRad)*i)/self.numRad+self.minRad
			for j in range(self.numTheta+1):
				newcycle.append(self.newPoint(cnumpolar(newrad, float(self.maxTheta*j)/self.numTheta)))
			self.cycles.append(newcycle)

		self.points = []

	def newPoint(self, cnp):
		return cnp

	def renderPoints(self, cnps):
		self.points = map(lambda x:self.newPoint(x), cnps)

	def draw(self, ptScale=1):
		self.drawField()
		self.drawPoints(ptScale)

	def drawField(self):
		for cyclestrip in range(len(self.cycles)-1):
			glBegin(GL_QUAD_STRIP)
			for i in range(len(self.cycles[cyclestrip])):
				self.cycles[cyclestrip][i].callGl(self.maxRad)
				self.cycles[cyclestrip+1][i].callGl(self.maxRad)
			self.cycles[cyclestrip][0].callGl(self.maxRad)
			self.cycles[cyclestrip+1][0].callGl(self.maxRad)
			glEnd()

	def drawPoints(self, ptScale=1):
		for point in self.points:
			(x, y, z) = point.getGlVertex()
			glColor(1, 1, 1)
			glBegin(GL_QUADS)
			glVertex(x-.01*ptScale, y-.01*ptScale, z)
			glVertex(x+.01*ptScale, y-.01*ptScale, z)
			glVertex(x+.01*ptScale, y+.01*ptScale, z)
			glVertex(x-.01*ptScale, y+.01*ptScale, z)
			glEnd()
		


class PolarComplexMappedField(PolarComplexField):
	def __init__(self, mapFns=[lambda x: cnumpolar(math.pow(x.radius, .5), x.theta/2.)], *args, **kwargs):
		self.mapFns = mapFns
		super(PolarComplexMappedField, self).__init__(*args, **kwargs)

	def newPoint(self, cnp):
		return MappedComplex(cnp, self.mapFns)

class Shape(object):
	def __init__(self, start_t = 0.0, end_t = 1.0, num_t = 10, color = (0, 1, 0),
		pointGenerator = lambda x: cnumxy(x, 0)):
		self.num_t = num_t
		self.start_t = start_t
		self.end_t = end_t
		self.color = color
		self.pointGenerator = pointGenerator

	def drawPoints(self, mappings=[]):
		glColor(*self.color)
		glLineWidth(3)
		glBegin(GL_LINE_STRIP)
		t = min(self.start_t, self.end_t)
		while t <= max(self.start_t, self.end_t):
			MappedComplex(self.pointGenerator(t), mappings).callGlVertex()
			t += float(abs(self.start_t-self.end_t))/self.num_t
		glEnd()
		glLineWidth(1)