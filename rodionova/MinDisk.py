import sys
import PointSet

def printError(i, l):
  print "Wrong file format."
  print "Error in line " + str(i) + " : " + l.strip()
  print "There should be two integers separated by a space in the line"

list = sys.argv
if len(list) != 2:
  print "Program need one input parameter: file name"
  print "Example: 1.py input.txt"
  exit(0)
filename = list[1]
file = open(filename)
pointSet = PointSet.PointSet()
i = 0;
for l in file.xreadlines():
  i = i+1
  try:
    p = l.split(' ');
  except:
    printError(i, l)
    exit()
  if len(p) != 2:
    printError(i, l)
    exit()
  try:
    pointSet.addPoint(int(p[0]), int(p[1]))
  except:
    printError(i, l)
    exit()

(radius, centre) = pointSet.minDisk()  
  
print "centre = (" + str(centre) + ")"
print "radius = " + str(radius)
      
      