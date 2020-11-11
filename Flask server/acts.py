import RPi.GPIO as GPIO

enA = 25
in1 = 24
in2 = 23
in3 = 18
in4 = 15
enB = 14
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT), GPIO.setup(in2, GPIO.OUT), GPIO.setup(enA, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT), GPIO.setup(in4, GPIO.OUT), GPIO.setup(enB, GPIO.OUT)
GPIO.output(in1, GPIO.LOW), GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW), GPIO.output(in4, GPIO.LOW)
freq = 1000
speed = 100
p1, p2 = GPIO.PWM(enA, freq), GPIO.PWM(enB, freq)
p1.start(speed), p2.start(speed)

def forward():
    print("Forward")
    GPIO.output(in1, GPIO.LOW), GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW), GPIO.output(in4, GPIO.HIGH)

def stop():
    print("Stop")
    GPIO.output(in1, GPIO.LOW), GPIO.output(in2, GPIO.LOW), p1.ChangeDutyCycle(speed)
    GPIO.output(in3, GPIO.LOW), GPIO.output(in4, GPIO.LOW), p2.ChangeDutyCycle(speed)

def back():
    print("Backward")
    GPIO.output(in1, GPIO.HIGH), GPIO.output(in2, GPIO.LOW), p1.ChangeDutyCycle(speed)
    GPIO.output(in3, GPIO.HIGH), GPIO.output(in4, GPIO.LOW), p2.ChangeDutyCycle(speed)

def left():
    print("Left")
    GPIO.output(in1, GPIO.LOW), GPIO.output(in2, GPIO.HIGH), p1.ChangeDutyCycle(speed-25)
    GPIO.output(in3, GPIO.LOW), GPIO.output(in4, GPIO.LOW), p2.ChangeDutyCycle(speed)

def right():
    print("Right")
    GPIO.output(in1, GPIO.LOW), GPIO.output(in2, GPIO.LOW), p1.ChangeDutyCycle(speed)
    GPIO.output(in3, GPIO.LOW), GPIO.output(in4, GPIO.HIGH), p2.ChangeDutyCycle(speed-25)

def gear1():
    print("Speed: 25%")
    speed = 25
    p1.ChangeDutyCycle(speed)
    p2.ChangeDutyCycle(speed)

def gear2():
    print("Speed: 50%")
    speed = 50
    p1.ChangeDutyCycle(speed)
    p2.ChangeDutyCycle(speed)

def gear3():
    print("Speed: 75%")
    speed = 75
    p1.ChangeDutyCycle(speed)
    p2.ChangeDutyCycle(speed)

def gear4():
    print("Speed: 100%")
    speed = 100
    p1.ChangeDutyCycle(speed)
    p2.ChangeDutyCycle(speed)
