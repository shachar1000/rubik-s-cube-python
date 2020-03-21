import cv2 
import numpy as np 
import math  
  
# Let's load a simple image with 3 black squares 
#image = cv2.imread('cube.jpg') 

cap = cv2.VideoCapture(0)
#backSub = cv2.createBackgroundSubtractorMOG2()

_, first_frame = cap.read()
first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
first_gray = cv2.GaussianBlur(first_gray, (5, 5), 0)

while (True):
    
    # ret, frame = cap.read()
    # fgMask = backSub.apply(frame)
    
    _, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    
    
    
    difference = cv2.absdiff(first_gray, gray_frame)
    _, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY_INV)
    
    floodfill = difference.copy()

    h, w = difference.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    cv2.floodFill(floodfill, mask, (0,0), 255);

    floodfill_inv = cv2.bitwise_not(floodfill)
    
    im_out = difference | floodfill_inv
    
    final = cv2.bitwise_and(frame, frame, mask = im_out)
    
    cv2.imshow("1", final)
    
    
  
    
    gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY) 
    edged = cv2.Canny(gray, 30, 200) 
    
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    correctAreas = []
    approxList = []
     
    removeList = [0]*len(contours)
    for count, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        approxList.append(approx)
    
        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            if (ar >= 0.80 and ar <= 1.20):
                correctAreas.append(area)
            removeList[count] = not (ar >= 0.80 and ar <= 1.20) # if it's true (meaning we have a square) than remove = False
    
    try:
        averageArea = sum(correctAreas) / len(correctAreas)
        for count, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if math.isclose(area, averageArea, rel_tol=0.1) and (len(approxList[count]) is 6 or len(approxList[count]) is 5):
                removeList[count] = False
    
    except:
        pass
    filteredContours = [contours[i] for i in range(len(contours)) if removeList[i] is False]
    
    cv2.imshow('Canny Edges After Contouring', edged) 
    
    print("Number of Contours found = " + str(len(filteredContours))) 
    
    cv2.drawContours(final, filteredContours, -1, (0, 255, 0), 3) 
    
    cv2.imshow('Contours', final) 
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
cap.release()
cv2.destroyAllWindows() 
