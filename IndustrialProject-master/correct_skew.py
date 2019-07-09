import cv2
import numpy as np
from scipy.ndimage.morphology import binary_fill_holes
import matplotlib.pyplot as plt
import skimage.measure
import csv
import math
import matplotlib.patches as mpatches

#Correcting skew using the red and green horizontal lines
class Skew():
   def __init__(self, filename):

      image = cv2.imread(filename)

      r = 1000.0 / image.shape[1]
      dim = (1000, int(image.shape[0] * r))

      # perform the actual resizing of the image and show it
      resized = cv2.resize\
         (image, dim, interpolation=cv2.INTER_AREA)
      #cv2.imshow("resized", resized)

      # Convert BGR to HSV
      hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

      lower = np.array([0, 100, 100], dtype="uint8")
      upper = np.array([10, 255, 255], dtype="uint8")
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
      th, im_th = cv2.threshold(output,0,255, cv2.THRESH_BINARY);
      plt.imshow(im_th)
      plt.title("WithHoles")
      plt.show()

      imwithoutholes=binary_fill_holes(im_th[:,:,0], structure=np.ones((3,3))).astype(int)


      plt.imshow(imwithoutholes)
      plt.title("imwithoutholes")
      plt.show()

      #gris = cv2.cvtColor(imwithoutholes, cv2.COLOR_BGR2GRAY)
      edges = cv2.Canny(gray, 100, 170, apertureSize=3)
      #cv2.imshow('edges', edges)

      lines = cv2.HoughLines(edges,1, np.pi / 700, 150)

      for [[rho, theta]] in lines:
         a = np.cos(theta)
         b = np.sin(theta)
         x0 = a * rho
         y0 = b * rho
         x1 = int(x0 + 1000 * (-b))
         y1 = int(y0 + 1000 * (a))
         x2 = int(x0 - 1000 * (-b))
         y2 = int(y0 - 1000 * (a))

         cv2.line(resized, (x1, y1), (x2, y2), (255, 0, 0), 2)
         angle=-math.degrees(theta)
         print (angle)
         if angle < -45:
             angle = -(90 + angle)
             # otherwise, just take the inverse of the angle to make
             #  it positive
         else:
             angle = -angle


      #cv2.imshow('Hough Lines', resized)
      #cv2.waitKey(0)

      (h, w) = resized.shape[:2]
      center = (w // 2, h // 2)
      M = cv2.getRotationMatrix2D(center, angle, 1.0)
      rotated = cv2.warpAffine(resized, M, (w, h),flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

      # draw the correction angle on the image so we can validate it
      cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
                  (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

      # show the output image
      print("[INFO] angle: {:.3f}".format(angle))
      #cv2.imshow("Input", resized)
      #cv2.imshow("Rotated", rotated)
      #cv2.waitKey(0)
      #cv2.imwrite(filename, rotated)




