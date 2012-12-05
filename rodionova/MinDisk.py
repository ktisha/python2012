import sys
import PointSet

def printError(i, l):
  print "Wrong file format."
  print "Error on line " + str(i) + " : " + l.strip()
  print "There should be two integers separated by a space in the line"
  exit(1)

if len(sys.argv) != 2:
  print "Program needs one input parameter: file name"
  print "Example: " + sys.argv[0] + " input.txt"
  exit(1)
  
pointSet = PointSet.PointSet()
for i, l in enumerate(open(sys.argv[1])):
  p = l.split()
  if len(p) != 2:
    printError(i, l)
  try:
    pointSet.addPoint(int(p[0]), int(p[1]))
  except:
    printError(i, l)

(radius, centre) = pointSet.minDisk()
  
print "centre = (" + str(centre) + ")"
print "radius = " + str(radius)

pointSet.drawMinDisk(centre, radius)