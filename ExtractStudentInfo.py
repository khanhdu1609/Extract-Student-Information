import cv2
import numpy as np
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image
class ExtractStudentInfo:
    def __init__(self):
        self.kernel = np.ones([5, 5], np.uint8)

    def smoothing(self, img, kernel):
        dilation = cv2.dilate(img, kernel, iterations=10)
        blur = cv2.GaussianBlur(dilation, (3, 3), 0)
        erosion = cv2.erode(blur, kernel, iterations=10)

        return erosion

    def findEdge(self, img):
        return cv2.Canny(img, 100, 200)

    def findLines(self, edgeImg):
        lines = cv2.HoughLines(edgeImg, 1, np.pi/360, 60)
        lines = lines.reshape(-1, 2)

        notDuplicatedLines = [lines[0]]
        for line in lines[1:]:
            diff = np.abs(np.abs(line) - np.abs(notDuplicatedLines))
            diff = diff.reshape(-1, 2)
            if np.all((diff[:, 0] >= 25) | (diff[:, 1] >= 0.5)):
                notDuplicatedLines.append(line)

        lines = np.asarray(notDuplicatedLines[:4])
        return lines.reshape((lines.shape[0], 2))

    def intersection(self, line1, line2):
        rho1, theta1 = line1
        rho2, theta2 = line2
        A = np.array([[np.cos(theta1), np.sin(theta1)],
                      [np.cos(theta2), np.sin(theta2)]])
        b = np.array([[rho1], [rho2]])
        if (abs(theta1 - theta2) > 0.7 and abs(theta1 - theta2)<2.0):  # avoid parallel lines
            return [[np.round(np.linalg.solve(A, b))]]

    def point_inter(self, lines):
        intersectionPoints = [np.asarray(self.intersection(lines[index], lines[idx])).reshape(2,)
                              for index in range(len(lines))
                              for idx in range(index + 1, len(lines))
                              if self.intersection(lines[index], lines[idx]) is not None
                              and all(np.asarray(self.intersection(lines[index], lines[idx])).reshape(2,) > 0)]
        return intersectionPoints

    def flatten(self, grayImg, intersectionPoints):
        frame = np.zeros((4, 2), dtype='float32')
        sum = np.sum(intersectionPoints, axis=1)
        frame[0] = intersectionPoints[np.argmin(sum)]
        frame[3] = intersectionPoints[np.argmax(sum)]

        reservedPoints = []
        for idx in range(4):
            if idx != np.argmin(sum) and idx != np.argmax(sum):
                reservedPoints.append(intersectionPoints[idx])
        if np.linalg.norm(reservedPoints[0] - frame[0]) > np.linalg.norm(reservedPoints[1] - frame[0]):
            frame[1] = reservedPoints[0]
            frame[2] = reservedPoints[1]
        else:
            frame[1] = reservedPoints[1]
            frame[2] = reservedPoints[0]
        topLeft, topRight, bottomLeft, bottomRight = frame

        width1 = np.sqrt((topLeft[0] - topRight[0]) **
                         2 + (topLeft[1]-topRight[1])**2)
        width2 = np.sqrt((bottomLeft[0] - bottomRight[0])
                         ** 2 + (bottomLeft[1] - bottomRight[1])**2)
        maxWidth = max(int(width1), int(width2))

        height1 = np.sqrt((topLeft[0] - bottomLeft[0]) **
                          2 + (topLeft[1] - bottomLeft[1])**2)
        height2 = np.sqrt((topRight[0] - bottomRight[0]) **
                          2 + (topRight[1] - bottomRight[1])**2)
        maxHeight = max(int(height1), int(height2))
        destination = np.float32(
            [[0, 0], [maxWidth-1, 0], [0, maxHeight-1], [maxWidth-1, maxHeight-1]])
        transformMatrix = cv2.getPerspectiveTransform(frame, destination)
        scan = cv2.warpPerspective(
            grayImg, transformMatrix, (maxWidth, maxHeight))
        scan = cv2.resize(scan, (400, 300))
        return scan

    def cropInfo(self, img):
        info_imgs = list()
        name = img[109:123, 136:227]
        info_imgs.append(name)
        birth = img[130:145, 154:212]
        info_imgs.append(birth)
        sex = img[130:145, 267:297]
        info_imgs.append(sex)
        faculty = img[150:167, 132:219]
        info_imgs.append(faculty)
        major = img[190:215, 160:204]
        info_imgs.append(major)
        gen = img[213:230, 150:235]
        info_imgs.append(gen)
        stdId = img[205:219, 346:398]
        info_imgs.append(stdId)
        return info_imgs
    def readInfo(self, info_img):
        config = Cfg.load_config_from_name('vgg_transformer')
        config['cnn']['pretrained']=True
        config['device'] = 'cpu'
        detector = Predictor(config)
        info = ['Name', 'Date of Birth', 'Sex', 'Faculty', 'Major', 'Gen', 'Student ID']
        info_dict = {}
        for i, img in enumerate(info_img, start=0):
            string = detector.predict(Image.fromarray(img))
            info_dict[info[i]] = string
        return info_dict