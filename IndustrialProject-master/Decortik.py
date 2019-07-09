import cv2
import numpy as np
from scipy.ndimage.morphology import binary_fill_holes
import matplotlib.pyplot as plt
import skimage.measure
import csv

def Time_event(x_activity,t_unity,t0):
    return ((x_activity-t0)/t_unity)-1

fig, ax = plt.subplots(figsize=(10, 6))
image = cv2.imread("img/3.jpg")
csvfile = open("lala.csv", 'w')

fieldnames = ['name', 'color', 'form', 'start', 'end']

writer = csv.writer(csvfile)
writer.writerow(fieldnames)

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 10,
        }

# we need to keep in mind aspect ratio so the image does
# not look skewed or distorted -- therefore, we calculate
# the ratio of the new image to the old image
r = 1000.0 / image.shape[1]
dim = (1000, int(image.shape[0] * r))

# perform the actual resizing of the image
resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# Convert BGR to HSV
hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

#################Pour la detection des lignes

# Grayscale and Canny Edges extracted
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
#Detection des formes sur l'image grise
edges = cv2.Canny(gray, 100, 170, apertureSize=3)


# Run HoughLines using a rho accuracy of 1 pixel
# theta accuracy of np.pi / 180 which is 1 degree
# Our line threshold is set to 240 (number of points on line)
lines = cv2.HoughLines(edges, 5, np.pi / 180, 150)

print(lines)

#Define time line info
time_line = []

# We iterate through each line and convert iy1t to the format
# required by cv.lines (i.e. requiring end points)

print("Lines: ", lines)
# We iterate through each line and convert it to the format
# required by cv.lines (i.e. requiring end points)
prev_x = None
ordered_lines = sorted(lines, key=lambda x: x[0][0]*np.cos(x[0][1]))
for [[rho, theta]] in ordered_lines:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * a)
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * a)
    if abs(x1 - x2) >= 3:
        continue
    if prev_x is not None:
        if abs(prev_x - x1) < 50:
            continue
    time_line.append(x1)
    prev_x = max(x1, x2)
t_unity = time_line[1]-time_line[0]



# Boundaries RED GREEN BLUE
boundaries = [
    ([0, 100, 100], [10, 255, 255]),
    ([45, 50, 50], [80, 255, 255])
]


# Threshold the HSV image to get only blue colors
for (lower, upper) in boundaries:
    #Define the color: cela juste en premier temps C'est à optimisé => JE CONFIRME
    if (lower == [0, 100, 100]) and (upper == [10, 255, 255]):
        color = "Red"
    else:
        color = "Green"

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    #  the mask
    mask = cv2.inRange(hsv, lower, upper)

    output = cv2.bitwise_and(resized, resized, mask=mask)
    # Define contours

    # Grayscale
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    # Threshold.
    # Set values equal to or above 220 to 0.
    # Set values below 0 to 0.

    th, im_th = cv2.threshold(output, 0, 255, cv2.THRESH_BINARY)
    plt.imshow(im_th)
    plt.title("WithHoles")
    plt.show()

    imwithoutholes = binary_fill_holes(im_th[:, :, 0], structure=np.ones((3, 3))).astype(int)

    plt.imshow(imwithoutholes)
    plt.title("imwithoutholes")
    plt.show()

    labeled_array, num_features = skimage.measure.label(imwithoutholes, return_num=True)
    plt.imshow(labeled_array)
    plt.title(num_features)
    plt.show()


    ax.imshow(labeled_array)

    regions = skimage.measure.regionprops(labeled_array)

    fig, ax = plt.subplots()
    ax.imshow(labeled_array, cmap=plt.cm.gray)
    i=0
    for props in regions:

        y0, x0 = props.centroid

        if (props.area>90):
            minr, minc, maxr, maxc = props.bbox
            bx = (minc, maxc, maxc, minc, minc)
            by = (minr, minr, maxr, maxr, minr)
            ax.plot(bx, by, '-b', linewidth=1)
            #debut de l'activité
            ax.plot(minc, y0, '.g', markersize=5)
            #fin de l'activité
            ax.plot(maxc, y0, '.g', markersize=5)
            ax.plot((maxc, minc), (y0, y0), '-r', markersize=5)
            ax.plot((x0, x0), (minr, maxr), '-r', markersize=5)


            #calcule de l'air

            bboxarea=(maxc-minc)*(maxr-minr)

            print("****** label  ", i)
            print("bboxarea/props.area: ", bboxarea / props.area)
            print("aria of th object :", props.area)
            print("aria of the bbox", bboxarea)

            if (bboxarea/props.area <1.5) and (bboxarea/props.area >1):
                print("pseudo Rectangle area: ", bboxarea/props.area)
                plt.text(x0, y0, str(i)+" :Activity", fontdict=font)
                form = "Rectangle"
            if (bboxarea / props.area <3.4) and (bboxarea / props.area > 2):
                print("Flag area: ", bboxarea / props.area)
                plt.text(x0, y0, str(i)+" :Flag", fontdict=font)
                form = "Flag"

            if (bboxarea / props.area <2) and (bboxarea / props.area > 1.60):
                print("Losange area: ", bboxarea / props.area)
                plt.text(x0, y0, str(i)+" :Losange", fontdict=font)
                form = "Losange"