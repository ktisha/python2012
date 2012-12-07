import math
import random
import Point
import matplotlib.pyplot as plt
     
class PointSet:
  def __init__(self):
    self.__pointSet = []
    
  def addPoint(self, x, y):
    self.__pointSet.append(Point.Point(x, y))
    
  def minDisk(self):
    self.__permute(len(self.__pointSet))
    a = self.__pointSet[0]
    b = self.__pointSet[1]
    c = PointSet.__thirdPoint(a,b)
    for i in xrange(2, len(self.__pointSet)):
      if PointSet.__det3_1(a, b, c) * PointSet.__det4(a, b, c, self.__pointSet[i]) > 0:
        (a,b,c) = self.__minDisk1(i)
    r = PointSet.__radius(a,b,c)
    cent = PointSet.__centre(a,b,c)   
    return (r,cent)
  
  def __minDisk1(self, i):
    a = self.__pointSet[i]
    self.__permute(i)
    b = self.__pointSet[0]
    c = PointSet.__thirdPoint(a,b)
    for j in xrange(1, i):
      if PointSet.__det3_1(a, b, c) * PointSet.__det4(a, b, c, self.__pointSet[j]) > 0:
        (a, b, c) = self.__minDisk2(i, j)
    return (a, b, c)
  
  def __minDisk2(self, i, j):
    a = self.__pointSet[i]
    b = self.__pointSet[j]
    self.__permute(j)
    c = PointSet.__thirdPoint(a,b)
    for k in xrange(0, j):
      if self.__pointSet[k] != b and PointSet.__det3_1(a, b, c) * PointSet.__det4(a, b, c, self.__pointSet[k]) > 0:
        c = self.__pointSet[k]
    return (a, b, c)
 
  def drawMinDisk(self, cent, r):
    margin = 10
    plt.axis([cent.x - r - margin, cent.x + r + margin, cent.y - r - margin, cent.y + r + margin])
    ax = plt.gca()
    ax.set_title("MinDisk")
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for p in self.__pointSet:
      plt.plot(p.x, p.y, 'ro')
    circ = plt.Circle((cent.x, cent.y), r)
    ax.add_patch(circ)
    plt.show()
  
  def __permute(self, n):
    random.seed()
    for k in xrange(n):
      r = random.randint(0, n - 1)
      tmp = self.__pointSet[k]
      self.__pointSet[k] = self.__pointSet[r]
      self.__pointSet[r] = tmp
  
  @staticmethod  
  def __radius(a, b, c):
    z = ( a.length(b) + b.length(c) + c.length(a)) * \
        (-a.length(b) + b.length(c) + c.length(a)) * \
        ( a.length(b) - b.length(c) + c.length(a)) * \
        ( a.length(b) + b.length(c) - c.length(a))
    return a.length(b) * b.length(c) * c.length(a) / math.sqrt(z)
    
  @staticmethod
  def __centre(a, b, c):
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
  
  @staticmethod
  def __det2(a, b):
    return a.x * b.y - a.y * b.x

  @staticmethod
  def __det3_d(a, b, c):
    return a.d2() * PointSet.__det2(b, c) - b.d2() * PointSet.__det2(a, c) + c.d2() * PointSet.__det2(a, b)
  
  @staticmethod  
  def __det3_1(a, b, c):
    return PointSet.__det2(a, b) - PointSet.__det2(a, c) + PointSet.__det2(b, c)
   
  @staticmethod   
  def __det4(a, b, c, d):
    return PointSet.__det3_d(b, c, d) - PointSet.__det3_d(a, c, d) + PointSet.__det3_d(a, b, d) - PointSet.__det3_d(a, b, c)
    
  @staticmethod
  def __thirdPoint(a, b):
    if a.x == b.x:
      y = float(a.y + b.y) / 2
      return Point.Point(a.x + abs(a.y - y), y)
    if a.y == b.y:
      x = float(a.x + b.x) / 2
      return Point.Point(x, a.y + abs(a.x - x))
    return Point.Point(a.x, b.y)