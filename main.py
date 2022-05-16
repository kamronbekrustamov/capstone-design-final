import cv2
import image
import time
from car import Car


camera = cv2.VideoCapture(0)


def waitForGreenSignal():
    while True:
        estimate = 0
        for i in range(0, 6):
            ret, frame = camera.read()
            estimate += image.detectGreenTrafficSign(frame)
        if estimate > 0.02:
            break


def doTurn(car):
    car.stop()
    time.sleep(1)
    car.turnRight()
    while True:
        ret, frame = camera.read()
        yellowRatio = image.detectYellowFrame(frame)
        if yellowRatio >= 0.1:
            break
    car.goForward()
    while True:
        ret, frame = camera.read()
        yellowRatio = image.findTheLane(frame)
        if yellowRatio >= 0.1:
            break
    car.turnLeft()
    time.sleep(0.4)


def start(car):
    waitForGreenSignal()
    
    obstacleCount = 0
    trafficRedSign = 0
    while True:
        ret, frame = camera.read()
        leftRatio, rightRatio = image.findDirection(frame)
        
        if trafficRedSign == 0:
            redRatio = image.detectRedTrafficSign(frame)
            if redRatio >= 0.1:
                print("Red Traffic Sign")
                trafficRedSign += 1
                car.stop()
                time.sleep(5)
                
        if car.isRightIROn():
            obstacleCount += 1
            print("ObstacleCount =", obstacleCount)
            if obstacleCount == 1:
                car.stop()
                time.sleep(7)
            elif obstacleCount == 2:
                car.turnLeft()
                time.sleep(0.4)
            elif obstacleCount == 3:
                doTurn(car)
        elif leftRatio > 0.2 and rightRatio < 0.2:
            car.turnRight()
        elif rightRatio > 0.2 and leftRatio < 0.2:
            car.turnLeft()
        elif leftRatio > 0.2 and rightRatio > 0.2:
            car.turnLeft()
            time.sleep(0.6)
            car.goForward()
            time.sleep(1.5)
            break
        else:
            car.goForward()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    with Car(40) as car:
        start(car)
