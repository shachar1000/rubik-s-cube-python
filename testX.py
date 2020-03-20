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



# my goal: for every face (4 vertices) create a matrix of 9 squares, the colors will be assigned to them

# in all sides, there will always be one coordinate that stays the same, I want to identify it (and what it equals to)
# for example in the front face z is the same but x and y change

squaresLOL = []

for face in faces:
    faceNewPoints = []
    coorNoChange = None
    coorNoChangeValue = None
    points = [vertices[index] for index in face]
    print(all(point[coor]==points[0][coor] for point in points for coor in [0, 1, 2]))
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
                        
                faceNewPoints.append(point)
    #faceNewPoints = list(set(faceNewPoints)) # this doesn't work with matrix :(
    newFaceNewPoints = []
    for elem in faceNewPoints:
        if elem not in newFaceNewPoints:
            newFaceNewPoints.append(elem)
    faceNewPoints = newFaceNewPoints
    
    
    # now we want the 3 other points (the form the squares for the polygon draw function)
    print(len(faceNewPoints))
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
        
        #print(square)
        squaresLOL.append(square)
        print(" ")
    
print(len(squaresLOL))
    # now we know which coor stays the same
    # the rest will go from -1 to 1 (for the 2 other coors) in increments of 2/3 each time (2 = 1-(-1) the delta)
