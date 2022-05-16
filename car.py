import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by "
          "using 'sudo' to run your script")

IN1_PIN = 12
IN2_PIN = 16
IN3_PIN = 18
IN4_PIN = 22

LEFT_TRACER_PIN = 24
RIGHT_TRACER_PIN = 26

RIGHT_IR_PIN = 32
LEFT_IR_PIN = 36

TRIG_PIN = 38
ECHO_PIN = 40

FREQUENCY = 100

turnRatio = 1.5


class Car(object):

    def __init__(self, speed: int):
        self.speed = speed
        # Board Setup
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        # DC Motor Pins Setup
        GPIO.setup(IN1_PIN, GPIO.OUT)
        GPIO.setup(IN2_PIN, GPIO.OUT)
        GPIO.setup(IN3_PIN, GPIO.OUT)
        GPIO.setup(IN4_PIN, GPIO.OUT)
        # IR Sensor Setup
        GPIO.setup(RIGHT_IR_PIN, GPIO.IN)
        GPIO.setup(LEFT_IR_PIN, GPIO.IN)
        # Ultrasonic Setup
        GPIO.setup(TRIG_PIN, GPIO.OUT)
        GPIO.setup(ECHO_PIN, GPIO.IN)
        # Lane Tracer Setup
        GPIO.setup(RIGHT_TRACER_PIN, GPIO.IN)
        GPIO.setup(LEFT_TRACER_PIN, GPIO.IN)

        self.leftForward = GPIO.PWM(IN1_PIN, FREQUENCY)
        self.leftForward.start(0)
        self.leftBackward = GPIO.PWM(IN2_PIN, FREQUENCY)
        self.leftBackward.start(0)
        self.rightForward = GPIO.PWM(IN3_PIN, FREQUENCY)
        self.rightForward.start(0)
        self.rightBackward = GPIO.PWM(IN4_PIN, FREQUENCY)
        self.rightBackward.start(0)

    def goForward(self):
        self.leftForward.ChangeDutyCycle(self.speed)
        self.leftBackward.ChangeDutyCycle(0)
        self.rightForward.ChangeDutyCycle(self.speed)
        self.rightBackward.ChangeDutyCycle(0)

    def goBackward(self):
        self.leftForward.ChangeDutyCycle(0)
        self.leftBackward.ChangeDutyCycle(self.speed)
        self.rightForward.ChangeDutyCycle(0)
        self.rightBackward.ChangeDutyCycle(self.speed)

    def turnRight(self):
        self.leftForward.ChangeDutyCycle(self.speed * turnRatio)
        self.leftBackward.ChangeDutyCycle(0)
        self.rightForward.ChangeDutyCycle(0)
        self.rightBackward.ChangeDutyCycle(self.speed * turnRatio)

    def turnLeft(self):
        self.leftForward.ChangeDutyCycle(0)
        self.leftBackward.ChangeDutyCycle(self.speed * turnRatio)
        self.rightForward.ChangeDutyCycle(self.speed * turnRatio)
        self.rightBackward.ChangeDutyCycle(0)

    def stop(self):
        self.leftForward.ChangeDutyCycle(0)
        self.leftBackward.ChangeDutyCycle(0)
        self.rightForward.ChangeDutyCycle(0)
        self.rightBackward.ChangeDutyCycle(0)

    def getDistance(self) -> int:
        GPIO.output(TRIG_PIN, GPIO.LOW)
        time.sleep(0.00002)
        GPIO.output(TRIG_PIN, GPIO.HIGH)
        time.sleep(0.00002)
        GPIO.output(TRIG_PIN, GPIO.LOW)

        while not GPIO.input(ECHO_PIN):
            pass
        startTime = time.clock_gettime_ns(time.CLOCK_MONOTONIC)

        while GPIO.input(ECHO_PIN):
            pass
        endTime = time.clock_gettime_ns(time.CLOCK_MONOTONIC)

        distance = (endTime - startTime) // 58000
        return distance

    def isRightIROn(self) -> bool:
        return not GPIO.input(RIGHT_IR_PIN)

    def isRightIROff(self) -> bool:
        return GPIO.input(RIGHT_IR_PIN)

    def isLeftIROn(self) -> bool:
        return not GPIO.input(LEFT_IR_PIN)

    def isLeftIROff(self) -> bool:
        return GPIO.input(LEFT_IR_PIN)

    def isRightTracerOn(self) -> bool:
        return not GPIO.input(RIGHT_TRACER_PIN)

    def isRightTracerOff(self) -> bool:
        return GPIO.input(RIGHT_TRACER_PIN)

    def isLeftTracerOn(self) -> bool:
        return not GPIO.input(LEFT_TRACER_PIN)

    def isLeftTracerOff(self) -> bool:
        return GPIO.input(LEFT_TRACER_PIN)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        GPIO.cleanup()
        if type is None or type is KeyboardInterrupt:
            print("Cleaning and Exiting")
            return True
        return False
