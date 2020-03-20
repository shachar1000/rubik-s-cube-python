import pygame
import sys
from pygame.locals import *
from itertools import starmap, product
import random
from collections import deque
import time
from threedcube import point
import numpy as np
import concurrent.futures
from threading import Timer, Thread, Event

stop = False    
counter = 0   

colors = {
"w":"white",
"g":"green",
"r":"red",
"b":"blue",
"o":"orange",
"y":"yellow"
}

def main():
    
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
        
    pygame.init()
    DISPLAY = pygame.display.set_mode((1400, 1000))
    clock = pygame.time.Clock()

    selection = {"front": True, "top": False, "bottom": False}

    matrix1 = [
    [0, 1, 0, 0],
    [1, 1, 1, 1],
    [0, 1, 0, 0]
    ]

    def randomCube():
        for y in range(len(matrix1)):
            for x in range(len(matrix1[y])):
                if matrix1[y][x] is not 0:
                    matrix1[y][x] = [[random.choice(list(colors.keys())) for j in range(3)] for i in range(3)]

    def startCubeSolved():
        counter = 0
        for y in range(len(matrix1)):
            for x in range(len(matrix1[y])):
                if matrix1[y][x] is not 0:
                    matrix1[y][x] = [[list(colors.keys())[counter] for j in range(3)] for i in range(3)]
                    counter = counter + 1

    startCubeSolved()

    mat1 = [
    ["r", "g", "b"],
    ["w", "g", "o"],
    ["b", "w", "y"]
    ]



    offsetX = 50
    offsetY = 50
    height = 100
    width = 100

    def scramble(matrix):
        if (random.random() < 0.5):
            matrix = switch(matrix, counter=random.random() > 0.5)
            print("ok")
        else:
            matrix = rotateTopBottom(matrix, top=random.random() > 0.5, counter=random.random() > 0.5)
            print("ok")
        drawCube(matrix)
        return matrix
        
    # i want the delay here to not stop the entire code

    def rotateTopBottom(matrix, top=True, counter=True):
        prevRowList = []
        matrix[0 if top else 2][1] = rotate90deg(matrix[0 if top else 2][1], not counter)
        for i in range(4):
            try:
                prevRowList.append(matrix[1][i-1 if counter else i+1][0 if top else 2]) # order according to counter/cw
            except IndexError:  # if we are clockwise (not counter) then i+1 will return index error RIP
                prevRowList.append(matrix[1][0][0 if top else 2])
        for i in range(4):
            matrix[1][i][0 if top else 2] =  prevRowList[i]
        return matrix

    def drawMatrix(matrix, yy, xx):
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                pygame.draw.rect(DISPLAY, pygame.Color(colors[matrix[y][x]]), (offsetX+x*width+xx*width*3, offsetY+y*height+yy*height*3, height, width), 0)
                pygame.draw.rect(DISPLAY, pygame.Color("black"), (offsetX+x*width+xx*width*3, offsetY+y*height+yy*height*3, height, width), 2)

    buttonRotateAnti = pygame.draw.rect(DISPLAY, pygame.Color("red") ,(0, 0, 50, 50))
    buttonRotate = pygame.draw.rect(DISPLAY, pygame.Color("orange") ,(50, 0, 50, 50))
    buttonFrontRight = pygame.draw.rect(DISPLAY, pygame.Color("blue") ,(0, 50, 50, 50))
    buttonFrontLeft = pygame.draw.rect(DISPLAY, pygame.Color("green") ,(50, 50, 50, 50))

    buttonScramble = pygame.draw.rect(DISPLAY, pygame.Color("purple") ,(0, 150, 50, 50))

    selection_buttons = { # this will store the args to pass to draw buttons
        "front": (0, 100, 50, 50),
        "top": (50, 100, 50, 50),
        "bottom": (100, 100, 50, 50),
    }

    selection_text = {
        "front": (5, 88),
        "top": (55, 88),
        "bottom": (105, 88),
    }

    f = pygame.font.Font("nigga.ttf",64) # 64
    DISPLAY.blit(f.render("↺", True, (255, 255, 255)) , (5, -12))
    DISPLAY.blit(f.render("↻", True, (255, 255, 255)) , (55, -12))
    DISPLAY.blit(f.render("→", True, (255, 255, 255)) , (5, 38))
    DISPLAY.blit(f.render("←", True, (255, 255, 255)) , (55, 38))

    #counterclockwise = right, clockwise = left

    def drawCube(matrix):
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                if matrix[y][x] is not 0:
                    drawMatrix(matrix[y][x], y, x)

    def transposeMatrix(matrix):
        return [[matrix[y][x] for y in range(len(matrix))] for x in range(len(matrix[0]))]

    def rotate90deg(matrix, clockwise):
        return [array[::-1] for array in transposeMatrix(matrix)] if clockwise else transposeMatrix(matrix)[::-1]

    def getNeighbors(matrix, x, y, getIndexes=False):
        indexes = starmap((lambda a, b: [x+a, y+b]), product((-1, 0, 1), (-1, 0, 1))) # this will return list of x, y coors for 2d mat
        indexes = filter(lambda index:  (0 <= index[0] < len(matrix) and (0 <= index[1] < len(matrix[index[0]])) ), list(indexes)) # filter the shit by checking if index smaller then len
        return [matrix[index[0]][index[1]] for index in indexes] if not getIndexes else indexes

    def switch(matrix, counter=True): # currently counter clockwise
        matrix[1][1] = rotate90deg(matrix[1][1], clockwise=False)
        def transIndex():
            matrix[neighIndexes[i][0]][neighIndexes[i][1]] = transposeMatrix(matrix[neighIndexes[i][0]][neighIndexes[i][1]])
        order = list(product(("reg", "trans"), (0, 2))) #reg/trans, 0/2
        order.sort(key=lambda x: x[1], reverse=True) # sort reg trans in order (counterclockwise from top)
        sides = list(filter(lambda side: side is not 0 and side is not matrix[1][1], getNeighbors(matrix, 1, 1)))
        neighIndexes = list(getNeighbors(matrix, 1, 1, getIndexes=True))
        neighIndexes = list(filter(lambda ix: matrix[ix[0]][ix[1]] is not 0 and matrix[ix[0]][ix[1]] is not matrix[1][1], getNeighbors(matrix, 1, 1, getIndexes=True)))
        sides[-1], sides[-2] = sides[-2], sides[-1] # sides in counterclockwise order from top
        neighIndexes[-1], neighIndexes[-2] = neighIndexes[-2], neighIndexes[-1]

        if counter==False:
            order[1], order[-1] = order[-1], order[1]
            sides[1], sides[-1] = sides[-1], sides[1]
            neighIndexes[1], neighIndexes[-1] = neighIndexes[-1], neighIndexes[1]
        prevRowList = []
        for i in range(len(neighIndexes)):
            prevRow = None
            if order[i-1][0] is "trans":
                row = transposeMatrix(matrix[neighIndexes[i-1][0]][neighIndexes[i-1][1]])[order[i-1][1]]
                if counter is True:
                    prevRowList.append(row)
                else:
                    prevRowList.append(row[::-1])
            else: #elif order[i-1][0] is "reg"
                prevRow = matrix[neighIndexes[i-1][0]][neighIndexes[i-1][1]][order[i-1][1]]
                if counter is True:
                    prevRow = prevRow[::-1] #if currently trans we need to inverse nigga (hoes mad warning)
                prevRowList.append(prevRow)
        for i in range(len(prevRowList)):
            if order[i-1][0] is "trans":
                matrix[neighIndexes[i][0]][neighIndexes[i][1]][order[i][1]] = prevRowList[i]
            else:
                transIndex()
                matrix[neighIndexes[i][0]][neighIndexes[i][1]][order[i][1]] = prevRowList[i]
                transIndex() # return to usual
        return matrix

    def switchFront(matrix, right=True):
        matrix[0][1] = rotate90deg(matrix[0][1], clockwise=not right) # if we move right we want anticlockwise in the top
        matrix[2][1] = rotate90deg(matrix[2][1], clockwise=right) # and the opposite in the bottom
        bar = deque(matrix[1])
        bar.rotate(1 if right else -1) # displace first & last elements
        matrix[1] = list(bar) # re-insert the nigga to the ghetto
        return matrix

    def yellowOnTop():
        pass

    drawCube(matrix1)

    def buttonsFunc():
        global buttons
        buttons = [pygame.draw.rect(DISPLAY, pygame.Color("white") if selection[key] is False else pygame.Color("red") , value) for key, value in selection_buttons.items()]
        for key, value in selection_text.items():
            DISPLAY.blit(f.render(key[0], True, (0, 0, 0)) , value)
    buttonsFunc()
    
    
            
    colorsCube = list(product([0, 255], repeat=3))[1:]
    colorsCube.remove((255, 255, 255))

    faces  = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]
    
    angle = 0
    
    side = [
    ["r", "g", "b"],
    ["w", "g", "o"],
    ["b", "w", "y"]
    ]
    
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

    while True:
        angle = angle + 1
        # vertices = [point(coor) for coor in list(product([1, -1], repeat=3))]

        squaresPoint = [[point(pointX) for pointX in square] for square in final_squares]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(50)
        DISPLAY.fill((0,0,0), (1000, 700, 500, 500))

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
            # we want to add x and y to point list to move the entire cube
            for i in range(len(pointlist)):
                pointlist[i][0] = pointlist[i][0] + 500 
                pointlist[i][1] = pointlist[i][1] + 350
                
            indexNow = dicti["index"]
            sideNumber = indexNow//9 # now we have a number, but we want x, y in matrix1 to know which we are talking about
            
            array = [[0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [2, 1]]
            
            y_index = array[sideNumber][0]
            x_index = array[sideNumber][1]
            
            side = matrix1[y_index][x_index]
            
            
                
            pygame.draw.polygon(DISPLAY, pygame.Color(colors[side[dicti["index"]%9%3][dicti["index"]%9//3]]), pointlist)            
            
        pygame.display.flip()        
            
            
         
            
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for count, button in enumerate(buttons):
                    if button.collidepoint(mouse_pos):
                        which = list(selection_buttons.keys())[count]
                        print(which)
                        for key, value in selection.items():
                            selection[key] = True
                            if not key is which:
                                selection[key] = False
                        buttonsFunc()
            
                if buttonScramble.collidepoint(mouse_pos):
                    global counter
                    counter = 0
                    # t = threading.Thread(target=scramble)
                    # t.start()
                    # with concurrent.futures.ThreadPoolExecutor() as executor:
                    #     future = executor.submit(scramble, matrix1)
                    #     return_value = future.result()
                    #     matrix1 = return_value
                    
                    class perpetualTimer():
                        def __init__(self,t,hFunction, arg, counter):
                          self.counter = counter
                          self.arg = arg   
                          self.t=t
                          self.hFunction = hFunction
                          self.thread = Timer(self.t,self.handle_function)

                        def handle_function(self):
                            if counter is not 10:
                              self.hFunction(self.arg)
                              self.thread = Timer(self.t,self.handle_function)
                              self.thread.start()

                        def start(self):
                          self.thread.start()

                        def cancel(self):
                          self.thread.cancel()
                    
                    def inner(matrix):
                        global stop
                        global counter
                        counter = counter + 1
                        matrix = scramble(matrix)
                        pygame.display.update()
                        print(counter)
                    
                            
                    #global counter    
                    t = perpetualTimer(0.4, inner, matrix1, counter)
                    t.start()
                    
                        
                    
            
                if buttonRotateAnti.collidepoint(mouse_pos):
                    if selection["front"] is True:
                        matrix1 = switch(matrix1, counter=True)
                    else:
                        matrix1 = rotateTopBottom(matrix1, top=selection["top"], counter=True)
                    drawCube(matrix1)
            
                if buttonRotate.collidepoint(mouse_pos):
                    if selection["front"] is True:
                        matrix1 = switch(matrix1, counter=False)
                    else:
                        matrix1 = rotateTopBottom(matrix1, top=selection["top"], counter=False)
                    drawCube(matrix1)
            
                if buttonFrontRight.collidepoint(mouse_pos):
                    matrix1 = switchFront(matrix1)
                    drawCube(matrix1)
                if buttonFrontLeft.collidepoint(mouse_pos):
                    matrix1 = switchFront(matrix1, right=False)
                    drawCube(matrix1)
            
        
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


main()
