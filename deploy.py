import cv2
import numpy as np
import matplotlib.pyplot as plt
from ExtractStudentInfo import ExtractStudentInfo
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image

extractor = ExtractStudentInfo()
if __name__ == '__main__':
    # Load and preprocess the image
    img_ori = cv2.imread('data_test/1 (11).jpg')
    img= cv2.resize(img_ori, (600, 500))
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_smooth= extractor.smoothing(img_gray, extractor.kernel)

    #Find the boundaries
    img_edge = extractor.findEdge(img_smooth)
    lines = extractor.findLines(img_edge)
    # Find lines using Hough transform or any other method
    # Draw the lines on the edge image
    line_img = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2BGR)
    for line in lines:
        rho, theta = line
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(line_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    # Find intersection points
    intersection_points = extractor.point_inter(lines)

    # Draw the intersection points on the original image
    for point in intersection_points:
        cv2.circle(img, (int(point[0]), int(point[1])), 5, (255, 0, 0), -1)
    
    #Flatten image
    scan = extractor.flatten(img, intersection_points)
    scan = cv2.cvtColor(scan, cv2.COLOR_BGR2RGB)

    #Crop the informations
    info_img = extractor.cropInfo(scan)

    #Read the informations
    informations = extractor.readInfo(info_img)

    print(informations)

#hihi
    