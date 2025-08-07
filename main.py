
from board import SCL, SDA
import busio
import time
from time import sleep
from adafruit_pca9685 import PCA9685
from xbox360controller import Xbox360Controller

debug = True
user_in = []

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50

pos_us = [0, 0, 0, 0, 0]
limit = [[], [500, 2600], [500, 2600], [500, 2600], [500, 2600], [500, 2600]]

def duty_calc(us):
    if type(us) != int:
        print("pleas enter an int")
        return
    duty = int(us / 1000000 * pca.frequency * 65536)
    return(duty)


def limit_2_calc():
    global limit_2
    limit_2 = [max(-pos_us[1]+3100,limit[2][0]),
               min(-pos_us[1]+4100, limit[2][1])]

def move_servo(servo, pos):
    if servo == 2:
        limit_2_calc()
        limit = limit_2
    else:
        limit = limit[servo]

    pos = min(limit[1],max(limit[0],pos))
    if debug:
        print(duty_calc(pos))
    else:
        servo = pca.channels[servo]
        servo.duty_cycle = duty_calc(pos)

try:
    while True:
        user_in[0] = input("servo")
        user_in[1] = input("pos")
        move_servo(user_in[0],user_in[1])
except KeyboardInterrupt:
    print("Programm Exit")
    exit()