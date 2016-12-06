import os
def averageXYZ(points):
	result = [0]*3
	for point in points:
		result[0] += point[0]
		result[1] += point[1]
		result[2] += point[2]
	result[0]/=len(points)
	result[1]/=len(points)
	result[2]/=len(points)
	return result
def cleanString(string):
	for i in xrange(0,10):
		string = string.replace("  "," ")
	return string
def discardDimension(points):
	xDifference = 0
	yDifference = 0
	zDifference = 0
	memory = points[0]
	averages = [0,0,0]
	averages[0]+=memory[0]
	averages[1]+=memory[1]
	averages[2]+=memory[2]
	for point in points[1:]:
		xDifference+=abs(point[0]-memory[0])
		yDifference+=abs(point[1]-memory[1])
		zDifference+=abs(point[2]-memory[2])
		averages[0]+=point[0]
		averages[1]+=point[1]
		averages[2]+=point[2]
	averages[0]/=len(points)*1.0
	averages[1]/=len(points)*1.0
	averages[2]/=len(points)*1.0
	minimum = min(xDifference,yDifference,zDifference)
	keep1 = 0
	keep2 = 1
	average = 0
	if minimum==xDifference:
		average = 0
		keep1 = 1
		keep2 = 2
	elif minimum==yDifference:
		keep1 = 0
		average = 1
		keep2 = 2
	else:
		keep1 = 0
		keep2 = 1
		average = 2
	result = []
	for i in xrange(0,len(points)):
		result.append([0,0])
	counter = 0
	for point in points:
		result[counter][0] = point[keep1]
		result[counter][1] = point[keep2]
		counter+=1
	return (averages,result,[keep1,keep2,average])
def polygonCentroid(points):
	averages,pointsNew,dimensions = discardDimension(points)
	return averages
	centroid = [0,0,0]
	centroid[dimensions[2]] = averages[dimensions[2]]
	signedArea = 0.0
	x0 = 0.0
	y0 = 0.0
	x1 = 0.0
	y1 = 0.0
	pSA = 0.0 #partial signed area
	for i in xrange(0,len(pointsNew)):
		x0 = pointsNew[i][0]
		y0 = pointsNew[i][1]
		x1 = pointsNew[(i+1)%len(pointsNew)][0]
		y1 = pointsNew[(i+1)%len(pointsNew)][1]
		a = x0*y1 - x1*y0
		print a
		signedArea += a
		centroid[dimensions[0]] += (x0 + x1)*a
		centroid[dimensions[1]] += (y0 + y1)*a
	signedArea *= 0.5
	centroid[dimensions[0]] /= (6.0*signedArea)
	centroid[dimensions[1]] /= (6.0*signedArea)
	return centroid
csvFile = open("GAT-1.pdb")
atoms = dict()
contador = 0
points = ["60","74","317","457"]
for linea in csvFile:
	if "ATOM" in linea:
		strings = cleanString(linea.strip()).split(" ")
		#print strings
		if strings[4] in points:
			if not strings[4] in atoms:
				atoms[strings[4]] = []
			atoms[strings[4]].append([float(strings[5]),float(strings[6]),float(strings[7])])
csvFile.close()
result = []
for key in points:
	result.append(averageXYZ(atoms[key]))
centroid = polygonCentroid(result)
print centroid