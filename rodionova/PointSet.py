import math

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
  return Point(Cx, Cy)
  
def thirdPoint(a, b):
  if a.x == b.x:
    y = (a.y+b.y)/2
    return Point(a.x+math.abz(a.y-y), y)
  if a.y == b.y:
    x = (a.x+b.x)/2
    return Point(x, a.y+math.abz(a.x-x))
  return Point(a.x, b.y)
  
class Point:
  x = 0
  y = 0
  
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
  def __str__(self):
    return str(self.x) + " " + str(self.y)  
    
  def d2(self):
    return self.x * self.x + self.y * self.y

  def length(self, a):
    return math.sqrt((self.x - a.x) * (self.x - a.x) + (self.y - a.y) * (self.y - a.y))
    
class PointSet:
  __pointSet = []
  
  def __init__(self):
   i = 0
  
  def addPoint(self, p):
    self.__pointSet += p
    
  def addPoint(self, x, y):
    self.__pointSet.append(Point(x, y))
    
  def __str__(self):
    s = ""
    for p in self.__pointSet:
      s += str(p.x) + " " + str(p.y) + "\n"
    return s.strip()
    
  def minDisk(self):
    a = self.__pointSet[0]
    b = self.__pointSet[1]
    c = thirdPoint(a,b)
    for i in xrange(2, len(self.__pointSet)):
      if det3_1(a,b,c)*det4(a,b,c,self.__pointSet[i]) > 0:
        (a,b,c) = self.__minDisk1(i)
    r = radius(a,b,c)
    cent = centre(a,b,c)
    return (r,cent)
  
  def __minDisk1(self, i):
    a = self.__pointSet[i]
    b = self.__pointSet[0]
    c = thirdPoint(a,b)
    for j in xrange(1, i):
      if det3_1(a,b,c)*det4(a,b,c,self.__pointSet[j]) > 0:
        (a, b, c) = self.__minDisk2(i, j)
    return (a, b, c)
  
  def __minDisk2(self, i, j):
    a = self.__pointSet[i]
    b = self.__pointSet[j]
    c = thirdPoint(a,b)
    for k in xrange(0, j):
      if k != j and det3_1(a,b,c)*det4(a,b,c,self.__pointSet[k]) > 0:
        c = self.__pointSet[k]
    return (a, b, c)
    