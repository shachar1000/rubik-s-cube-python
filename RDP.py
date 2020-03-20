import numpy as np
from math import sqrt
import math
from matplotlib import pyplot as plt
def distance(p1, p2):
    return sqrt((p0[0]-p1[0])**2+(p0[1]-p1[1])**2)

def pointLineDistance(p1, p2, point):
    # orthogonal projection = dot product, divided by you know... math be gay
     a = p2[1]-p1[1]
     b = -(p2[0]-p1[0])
     distOfPerp = sqrt(a**2+b**2)
     vectorOfPointFromStart = [
        p1[0] - point[0],
        p1[1] - point[1]
     ]
     dotProduct = abs(np.dot(vectorOfPointFromStart, [a, b]))
     return dotProduct/distOfPerp

print(pointLineDistance([2, 2], [3, 4], [10, 8]))

def rdp_algo(points, epsilon):
    maxDist = 0
    index = 0
    for i in range(1, len(points)-1):
        distance = pointLineDistance(points[0], points[-1], points[i])
        if distance > maxDist:
            maxDist = distance
            index = i
    if (maxDist > epsilon):
        return rdp_algo(points[0:index+1], epsilon)[:-1] + rdp_algo(points[index:], epsilon)
    else: #no point is further than epsilon
        return [points[0], points[-1]] # first and last since no point between is good (lame AF)

x_points = np.arange(0, 5, 0.01)
def myFunction(x):
    return math.exp(-x)*math.cos(2*math.pi*x)
y_points = [myFunction(x) for x in x_points]
points = [[x_points[i], y_points[i]] for i in range(len(y_points))]

myEpsilon = 0
for i in range(100):
    myEpsilon=myEpsilon+0.001
    new_points = rdp_algo(points, myEpsilon)

    plt.plot([p[0] for p in new_points], [p[1] for p in new_points])
    #plt.plot(x_points, y_points)
    plt.draw()
    plt.pause(0.1)
    plt.clf()
