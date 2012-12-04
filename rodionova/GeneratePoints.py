import sys
import random
import Point

list = sys.argv
if len(list) != 3 and len(list) != 4:
  print "Program need two or three input parameters: number of points, file name, <maximum coordinates (2^16 by default)>"
  print "Example: GeneratePoints.py 100 1.txt <2 ** 16>"
  exit(0)
try:
  n = int(list[1])
except:
  print "First parameter should be an integer"
  print "Example: GeneratePoints.py 100 1.txt"
  exit()
filename = list[2]

if len(list) == 3:
  max_coord = 2 ** 16
else:
  try:
    max_coord = int(list[3])
  except:
    print "Third parameter should be an integer (2^16 by default)"
    print "Example: GeneratePoints.py 100 1.txt <2 ** 16>"
    exit()

pointSet = set()
random.seed()
while len(pointSet) < min(n, (max_coord + 1) ** 2):
  pointSet.add(Point.Point(random.randint(0, max_coord), random.randint(0, max_coord)))
  
file = open(filename, 'w')
for p in pointSet:
  file.write(str(p.x) + " " + str(p.y) + "\n")
file.close()
	  