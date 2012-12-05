import math

class Point: 
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
  def __str__(self):
    return str(self.x) + " " + str(self.y)
    
  def d2(self):
    return self.x * self.x + self.y * self.y

  def length(self, a):
    return math.sqrt((self.x - a.x) * (self.x - a.x) + (self.y - a.y) * (self.y - a.y))
	
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __ne__(self, other):
    return not self.__eq__(other)
  
  def __hash__(self):
    return hash(hash(self.x) + hash(self.y))