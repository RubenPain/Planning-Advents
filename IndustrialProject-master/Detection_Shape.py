import cv2
import numpy as np
import imutils

class Shape():
    def __init__(self, image):
        #  we need to keep in mind aspect ratio so the image does
        #  not look skewed or distorted -- therefore, we calculate
        #  the ratio of the new image to the old image
        r = 1000.0 / image.shape[1]
        dim = (1000, int(image.shape[0] * r))

        #  perform the actual resizing of the image and change its mode to HSV
        self.resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        self.hsv = cv2.cvtColor(self.resized, cv2.COLOR_BGR2HSV)

        # pass the image in gray an make a canny image
        # to have only shape
        gray = cv2.cvtColor(self.resized, cv2.COLOR_BGR2GRAY)
        self.edges = cv2.Canny(gray, 100, 170, apertureSize=3)

    def Lines(self):
        # create lines by the canny img
        lines = cv2.HoughLines(self.edges, 1, np.pi / 700, 150)
        # variable to draw only lines wanted
        prev_x = None
        ordered_lines = sorted(lines, key=lambda x: x[0][0]*np.cos(x[0][1]))
        img_line = self.resized.copy()
        timeline = []
        for [[rho, theta]] in ordered_lines:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * a)
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * a)
            # to draw only vertical lines and only columns
            if abs(x1 - x2) >= 3:
                continue
            if prev_x is not None:

                if abs(prev_x - x1)<50:
                    continue
            # draw
            cv2.line(img_line, (x1, y1), (x2, y2), (255, 0, 0), 2)
            # append coordinate
            timeline.append(x1*2)
            prev_x = max(x1, x2)


        #cv2.imshow('t', img_line)
        #cv2.waitKey(0)
        return timeline

    def CC(self):
        #  Boundaries RED GREEN
        boundaries = [
        ([2, 100, 100], [10, 255, 255]),
        ([44, 37, 74], [79, 255, 255])
        ]

        output_shape = []


        # To detect the contours of shape, its colors and its coordinates
        for (lower, upper) in boundaries:
            if lower == [2, 100, 100]:
                color = "red"
            else:
                color = "green"
            #  create NumPy arrays from the boundaries
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")
            #  find the colors within the specified boundaries and create
            #   the mask
            mask = cv2.inRange(self.hsv, lower, upper)

            # apply the mask
            output = cv2.bitwise_and(self.resized, self.resized, mask=mask)

            # find contours on the mask
            contours = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            for cnt in contours:
                rect = cv2.minAreaRect(cnt)
                area = abs(cv2.contourArea(cnt, True))
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
                # coordinate shape
                x, y, w, h = cv2.boundingRect(approx)
                # Draw only contours wanted and omit the img's noise
                # approximate but it works
                if h >= 15 or w >= 55:
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(output, [box], 0, (0, 0, 255), 2)
                    cv2.drawContours(output, cnt, -1, (0, 255, 0), 2)

                    # Just verification /Draw one diagonal
                    # cv2.line(output, (box[2][0], box[2][1]), (box[0][0], box[0][1]), (255, 0, 0), 2)

                    # Detect the type of shape
                    # approximate but it works
                    if h/w>=1 and h/w<=1.6:
                        shape = "Losange"
                        cv2.putText(output, "LOS", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    elif area <= 250:
                        shape = "Flag"
                        cv2.putText(output, "FLA", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    else:
                        shape = "Rectangle"
                        cv2.putText(output, "RCT", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    # coordinate*2 to have same with the azure's API
                    output_shape.append([shape, x*2, (x+w)*2, y*2, (y+h)*2, color])
            #cv2.imshow('out', output)
            #cv2.waitKey(0)
        return output_shape
