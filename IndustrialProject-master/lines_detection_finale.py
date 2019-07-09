import numpy as np
import cv2
image = cv2.imread('img/3.jpg')

# the ratio of the new image to the old image
r = 1000.0 / image.shape[1]
dim = (1000, int(image.shape[0] * r))

# perform the actual resizing of the image and show it
resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
#cv2.imshow("resized", resized)
#cv2.waitKey(0)


# Grayscale and Canny Edges extracted
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 170, apertureSize = 3)

# Run HoughLines using a rho accuracy of 1 pixel
# theta accuracy of np.pi / 180 which is 1 degree
# Our line threshold is set to 240 (number of points on line)
lines = cv2.HoughLines(edges,1, np.pi / 700, 150)

time_line=[]

print("Lines: ",lines)
# We iterate through each line and convert it to the format
# required by cv.lines (i.e. requiring end points)
prev_x = None
ordered_lines = sorted(lines,key = lambda x: x[0][0]*np.cos(x[0][1]))
for [[rho, theta]] in ordered_lines:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    if abs(x1 - x2) >= 3:
        continue
    if prev_x is not None:

        if abs(prev_x - x1)<50:
            continue
        #print abs(prev_x - x1)


    time_line.append(x1)
    cv2.line(resized, (x1, y1), (x2, y2), (255, 0, 0), 2)
    prev_x = max(x1,x2)


print(time_line)
cv2.imshow('Hough Lines', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()