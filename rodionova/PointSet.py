import math
import random
import Point

def det2(a, b):
  return a.x * b.y - a.y * b.x

def det3_d(a, b, c):
  return a.d2() * det2(b, c) - b.d2() * det2(a, c) + c.d2() * det2(a, b)
  
def det3_1(a, b, c):
  return det2(a, b) - det2(a, c) + det2(b, c)
  
def det4(a, b, c, d):
  return det3_d(b, c, d) - det3_d(a, c, d) + det3_d(a, b, d) - det3_d(a, b, c)
  
def radius(a, b, c):
  z = (a.length(b)+b.length(c)+c.length(a))*(-a.length(b)+b.length(c)+c.length(a))*(a.length(b)-b.length(c)+c.length(a))*(a.length(b)+b.length(c)-c.length(a))
  return a.length(b) * b.length(c) * c.length(a) / math.sqrt(z)
  
def centre(a, b, c):
  A = b.x - a.x
  B = b.y - a.y
  C = c.x - a.x
  D = c.y - a.y
  E = A * (a.x + b.x) + B * (a.y + b.y)
  F = C * (a.x + c.x) + D * (a.y + c.y)
  G = 2 * (A * (c.y - b.y) - B * (c.x - b.x))
  Cx = float(D * E - B * F) / G
  Cy = float(A * F - C * E) / G
  return Point.Point(Cx, Cy)
  
def thirdPoint(a, b):
  if a.x == b.x:
    y = float(a.y+b.y)/2
    return Point.Point(a.x + abs(a.y-y), y)
  if a.y == b.y:
    x = float(a.x+b.x)/2
    return Point.Point(x, a.y + abs(a.x-x))
  return Point.Point(a.x, b.y)
     
class PointSet:
  __pointSet = []
  
  def __init__(self):
   i = 0
  
  def addPoint(self, p):
    self.__pointSet += p
    
  def addPoint(self, x, y):
    self.__pointSet.append(Point.Point(x, y))
    
  def __str__(self):
    s = ""
    for p in self.__pointSet:
      s += str(p) + "\n"
    return s.strip()
    
  def minDisk(self):
    self.perturb(len(self.__pointSet))
    a = self.__pointSet[0]
    b = self.__pointSet[1]
    c = thirdPoint(a,b)
    for i in xrange(2, len(self.__pointSet)):
      #print "MinDisk"
      #print str(a) + "; " + str(b) + "; " + str(c)
      #print self.__pointSet[i]
      if det3_1(a,b,c)*det4(a,b,c,self.__pointSet[i]) > 0:
        (a,b,c) = self.__minDisk1(i)
    r = radius(a,b,c)
    cent = centre(a,b,c)
    return (r,cent)
  
  def __minDisk1(self, i):
    a = self.__pointSet[i]
    self.perturb(i)
    b = self.__pointSet[0]
    c = thirdPoint(a,b)
    for j in xrange(1, i):
      #print "MinDisk1"
      #print str(a) + "; " + str(b) + "; " + str(c)
      #print self.__pointSet[j]
      if det3_1(a,b,c)*det4(a,b,c,self.__pointSet[j]) > 0:
        (a, b, c) = self.__minDisk2(i, j)
    return (a, b, c)
  
  def __minDisk2(self, i, j):
    a = self.__pointSet[i]
    b = self.__pointSet[j]
    self.perturb(j)
    c = thirdPoint(a,b)
    for k in xrange(0, j):
      #print "MinDisk2"
      #print str(a) + "; " + str(b) + "; " + str(c)
      #print self.__pointSet[k]
      if self.__pointSet[k] != b and det3_1(a,b,c)*det4(a,b,c,self.__pointSet[k]) > 0:
        c = self.__pointSet[k]
    return (a, b, c)
 
  def perturb(self, n):
    random.seed()
    for k in xrange(n):
      r = random.randint(0, n-1)
      tmp = self.__pointSet[k]
      self.__pointSet[k] = self.__pointSet[r]
      self.__pointSet[r] = tmp