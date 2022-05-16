import cv2
import numpy as np


def convertToHSV(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


def calculateWhitePointRatio(frame):
    return round(np.count_nonzero(frame) / np.size(frame), 2)


def applyYellowMask(frame):
    hsv = convertToHSV(frame)
    return cv2.inRange(hsv, (30, 70, 120), (50, 255, 255))


def applyRedMask(frame):
    hsv = convertToHSV(frame)
    return cv2.inRange(hsv, (0, 100, 20), (10, 255, 255))


def applyGreenMask(frame):
    hsv = convertToHSV(frame)
    return cv2.inRange(hsv, (50, 100, 100), (70, 255, 255))


def detectRedTrafficSign(frame):
    roi = frame[:40, 400:640]
    return calculateWhitePointRatio(applyRedMask(roi))


def detectGreenTrafficSign(frame):
    roi = frame[:120, 40:160]
    return calculateWhitePointRatio(applyGreenMask(roi))


def detectYellowFrame(frame):
    roi = frame[140:300, 500:]
    return calculateWhitePointRatio(applyYellowMask(roi))


def findTheLane(frame):
    roi = frame[420:480, :]
    return calculateWhitePointRatio(applyYellowMask(roi))


def findDirection(frame):
    # Crop the left rectangle from the frame and apply yellow mask to it
    leftRectangle = frame[420:480, 100:197]
    leftRectangleMasked = applyYellowMask(leftRectangle)
    
    # Crop the right rectangle from the frame and apply yellow mask to it
    rightRectangle = frame[420:480, 442:539]
    rightRectangleMasked = applyYellowMask(rightRectangle)

    leftRecWhitePointRatio = calculateWhitePointRatio(leftRectangleMasked)
    rightRecWhitePointRatio = calculateWhitePointRatio(rightRectangleMasked)

    return leftRecWhitePointRatio, rightRecWhitePointRatio
