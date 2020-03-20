


import math
import pygame
import numpy as np
from itertools import product
import sys

vertices = [
    [-1,1,-1],
    [1,1,-1],
    [1,-1,-1],
    [-1,-1,-1],
    [-1,1,1],
    [1,1,1],
    [1,-1,1],
    [-1,-1,1]
]
faces  = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]

final_squares = []

# my goal: for every face (4 vertices) create a matrix of 9 squares, the colors will be assigned to them

# in all sides, there will always be one coordinate that stays the same, I want to identify it (and what it equals to)
# for example in the front face z is the same but x and y change

        
# now we know which coor stays the same
# the rest will go from -1 to 1 (for the 2 other coors) in increments of 2/3 each time (2 = 1-(-1) the delta)

for face in faces:
    faceNewPoints = []
    coorNoChange = None
    coorNoChangeValue = None
    points = [vertices[index] for index in face]
    #print(all(point[coor]==points[0][coor] for point in points for coor in [0, 1, 2]))
    for coor in [0, 1, 2]:
        if all(point[coor]==points[0][coor] for point in points):
            coorNoChange = coor
            coorNoChangeValue = points[0][coor]
    # we want to skip the iteration if the coor is the one that doesn't change
    # but that would be difficult so we'll remove duplicates later on
    for z in range(3):
        for y in range(3):
            for x in range(3):
                point = [None, None, None]
                for coor in [0, 1, 2]:
                    if coor is coorNoChange:
                        point[coor] = coorNoChangeValue
                    else:
                        point[coor] = -1 + (2/3)*y if coor is 1 else -1 + (2/3)*x if coor is 0 else -1 + (2/3)*z # if coor is 2
                        # I typed 1 instead of 0 which fucked up the code (3 new points after filter in the last 2 sides instead of 4)
                        
                faceNewPoints.append(point)
    #faceNewPoints = list(set(faceNewPoints)) # this doesn't work with matrix :(
    newFaceNewPoints = []
    for elem in faceNewPoints:
        if elem not in newFaceNewPoints:
            newFaceNewPoints.append(elem)
    faceNewPoints = newFaceNewPoints
    #print(faceNewPoints)
    
    
    # now we want the 3 other points (the form the squares for the polygon draw function)
    #print(len(faceNewPoints))
    for point in faceNewPoints:
        square = [point, None, None, None]
        optionalCoors = [0, 1, 2]
        optionalCoors.remove(coorNoChange)
        #print(optionalCoors)
        for i in range(len(optionalCoors)):
            #print(point)
            new = square[0][:]
            new[optionalCoors[i]] = new[optionalCoors[i]] + 2/3
            square[i+1] = new
        square[3] = square[0][:]
        for optionalCoor in optionalCoors:
            square[3][optionalCoor] = square[3][optionalCoor] + 2/3
        
        # VERY IMPORTANT: it turns out that assigning square[0] to new creates an unwanted reference which causes problems in iteration
        final_squares.append(square)
        #print(square)
        print(" ")
    




 
def mainCube():
    
    
    
    class point:
        def __init__(self, coor):
            self.coor = np.array(coor)
            
        def convert(self, field, dist):
            coefficient = field / (dist + self.coor[2]) # z
            self.coor[0] = self.coor[0] * coefficient + 1400 / 2 # x , 400 is width
            self.coor[1] = -self.coor[1] * coefficient + 1000 / 2 # y, 400 is height
            return self
            
        def rotate(self, axis, angle): # angle in nigga deg not rad arg
            theta = np.radians(angle)
            rotationMat = {
            "x" : np.array(( (1, 0, 0),
                            (0, np.cos(theta), -np.sin(theta)),
                           (0, np.sin(theta),  np.cos(theta)) )),
        
            "y" : np.array(( (np.cos(theta), 0, np.sin(theta)),
                            (0, 1, 0),
                           (-np.sin(theta),  0, np.cos(theta)) )),
        
            "z"  : np.array(( (np.cos(theta), -np.sin(theta), 0),
                           (np.sin(theta),  np.cos(theta), 0), 
                           (0, 0, 1) ))
            }
            self.coor = self.coor.dot(rotationMat[axis])
            return self
    
    
    colors = list(product([0, 255], repeat=3))[1:]
    colors.remove((255, 255, 255))
    pygame.init()
    DISPLAY = pygame.display.set_mode((1400, 1000))

    faces  = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]
    clock = pygame.time.Clock()
    
    
    side = [
    ["r", "g", "b"],
    ["w", "g", "o"],
    ["b", "w", "y"]
    ]
    
    
    
    colors = {
    "w":"white",
    "g":"green",
    "r":"red",
    "b":"blue",
    "o":"orange",
    "y":"yellow"
    }
    
    

    
    
    angle = 0
    while True:
        # vertices = [point(coor) for coor in list(product([1, -1], repeat=3))]

        
        
        squaresPoint = [[point(pointX) for pointX in square] for square in final_squares]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(50)
        DISPLAY.fill((0,10,0))

        transformed = []
        
        for count, square in enumerate(squaresPoint):
            transformed.append([])
            for pointClass in square:
                transformed[count].append(pointClass.rotate("x", angle).rotate("y", angle).rotate("z", angle).convert(250, 4))
                
        
        # now we need to get average z of all the squares and sort them in draw order
        # but instead of doing this invidually for each little square we can do it on the large ones
        # or not :) fuck computational intensity suck my dick
        average_z_list = []
        index = 0
        for square in transformed:
            z = [square[i].coor[2] for i in range(len(square))]
            average_z = sum(z) / 4
            average_z_list.append({"index": index, "avg": average_z})
            index = index + 1
        
        average_z_list.sort(key = lambda dicti: dicti["avg"], reverse=True)
        
            
        for dicti in average_z_list:
            square = transformed[dicti["index"]]
            pointlist = [pointClass.coor[:-1] for pointClass in square]
            pointlist[3], pointlist[2] = pointlist[2], pointlist[3] 
            pygame.draw.polygon(DISPLAY, pygame.Color(colors[side[dicti["index"]%9%3][dicti["index"]%9//3]]), pointlist)
        pygame.display.flip()    
        
        
            
        # for square in transformed:
        #     pointlist = [pointClass.coor[:-1] for pointClass in square]
        #     pointlist[3], pointlist[2] = pointlist[2], pointlist[3] 
        #     pygame.draw.polygon(DISPLAY, tuple(np.random.randint(256, size=3)), pointlist)
        # pygame.display.flip()
        
        # 
        # #calculate average z to know what to draw
        # average_z_list = []
        # index = 0
        # for face in faces:
        #     z = [transformed[face[i]].coor[2] for i in range(len(face))]    
        #     average_z = sum(z) / 4 # /4
        # 
        #     average_z_list.append({"index" : index, "avg" : average_z})
        #     index = index + 1
        # average_z_list.sort(key=lambda dicti: dicti['avg'], reverse=True)
        # 
        # for dicti in average_z_list:
        #     face = faces[dicti["index"]]
        #     # pointlist = [(transformed[face[0]].coor[0], transformed[face[0]].coor[1]), (transformed[face[1]].coor[0], transformed[face[1]].coor[1]),
        #     #              (transformed[face[1]].coor[0], transformed[face[1]].coor[1]), (transformed[face[2]].coor[0], transformed[face[2]].coor[1]),
        #     #              (transformed[face[2]].coor[0], transformed[face[2]].coor[1]), (transformed[face[3]].coor[0], transformed[face[3]].coor[1]),
        #     #              (transformed[face[3]].coor[0], transformed[face[3]].coor[1]), (transformed[face[0]].coor[0], transformed[face[0]].coor[1])]
        #     # 
        #     pointlist = [[[transformed[face[i]].coor[0], transformed[face[i]].coor[1]], [transformed[face[i+1]].coor[0], transformed[face[i+1]].coor[1]]] for i in range(3)]
        #     pointlist.append( [[transformed[face[3]].coor[0], transformed[face[3]].coor[1]], [transformed[face[0]].coor[0], transformed[face[0]].coor[1]]] )
        #     #we need to flatten matrix
        #     # from [[],[]], [[],[]] to [], [], [], []
        #     pointlist = [point for duo in pointlist for point in duo ]
        #     pygame.draw.polygon(DISPLAY, colors[dicti["index"]], pointlist)
        # pygame.display.flip()
            
        angle = angle + 1
if __name__ == "__main__":
    mainCube()
