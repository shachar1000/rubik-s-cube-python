import math
import pygame
import numpy as np
from itertools import product
import sys

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
 
def mainCube():
    colors = list(product([0, 255], repeat=3))[1:]
    colors.remove((255, 255, 255))
    pygame.init()
    DISPLAY = pygame.display.set_mode((1400, 1000))

    faces  = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]
    clock = pygame.time.Clock()
    
    angle = 0
    while True:
        # vertices = [point(coor) for coor in list(product([1, -1], repeat=3))]

        vertices = [
            point([-1,1,-1]),
            point([1,1,-1]),
            point([1,-1,-1]),
            point([-1,-1,-1]),
            point([-1,1,1]),
            point([1,1,1]),
            point([1,-1,1]),
            point([-1,-1,1])
        ]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(50)
        DISPLAY.fill((0,10,0))

        transformed = []
        
        for vertex in vertices:
            transformed.append((  vertex.rotate("x", angle).rotate("y", angle).rotate("z", angle).convert(250, 4) ))
        
            #calculate average z to know what to draw
        average_z_list = []
        index = 0
        for face in faces:
            z = [transformed[face[i]].coor[2] for i in range(len(face))]    
            average_z = sum(z) / 4 # /4

            average_z_list.append({"index" : index, "avg" : average_z})
            index = index + 1
        average_z_list.sort(key=lambda dicti: dicti['avg'], reverse=True)
            
        for dicti in average_z_list:
            face = faces[dicti["index"]]
            
            pointlist = [(transformed[face[0]].coor[0], transformed[face[0]].coor[1]), (transformed[face[2]].coor[0], transformed[face[2]].coor[1]), (transformed[face[1]].coor[0], transformed[face[1]].coor[1]), (transformed[face[3]].coor[0], transformed[face[3]].coor[1])]
            
            
            # pointlist = [(transformed[face[0]].coor[0], transformed[face[0]].coor[1]), (transformed[face[1]].coor[0], transformed[face[1]].coor[1]),
            #              (transformed[face[1]].coor[0], transformed[face[1]].coor[1]), (transformed[face[2]].coor[0], transformed[face[2]].coor[1]),
            #              (transformed[face[2]].coor[0], transformed[face[2]].coor[1]), (transformed[face[3]].coor[0], transformed[face[3]].coor[1]),
            #              (transformed[face[3]].coor[0], transformed[face[3]].coor[1]), (transformed[face[0]].coor[0], transformed[face[0]].coor[1])]
            # 
            # pointlist = [[[transformed[face[i]].coor[0], transformed[face[i]].coor[1]], [transformed[face[i+1]].coor[0], transformed[face[i+1]].coor[1]]] for i in range(3)]
            # pointlist.append( [[transformed[face[3]].coor[0], transformed[face[3]].coor[1]], [transformed[face[0]].coor[0], transformed[face[0]].coor[1]]] )
            #we need to flatten matrix
            # from [[],[]], [[],[]] to [], [], [], []
            #pointlist = [point for duo in pointlist for point in duo ]
            pygame.draw.polygon(DISPLAY, colors[dicti["index"]], pointlist)
        pygame.display.flip()
            
        angle = angle + 1
if __name__ == "__main__":
    mainCube()
