import sys
import random
import Point

def wrongUsage():
  print "Program needs two or three input parameters: number of points, file name, <maximum coordinates (2^16 by default)>"
  print "Example: " + sys.argv[0] + " 100 1.txt <2 ** 16>"
  exit(1)

lst = sys.argv
if len(lst) != 3 and len(lst) != 4:
  wrongUsage()
try:
  n = int(lst[1])
except:
  wrongUsage()

if len(lst) == 3:
  max_coord = 2 ** 16
else:
  try:
    max_coord = int(lst[3])
  except:
    wrongUsage()

pointSet = set()
random.seed()
while len(pointSet) < min(n, (max_coord + 1) ** 2):
  pointSet.add(Point.Point(random.randint(0, max_coord), random.randint(0, max_coord)))
  
outfile = open(lst[2], 'w')
for p in pointSet:
  outfile.write(str(p) + "\n")
outfile.close()
	  