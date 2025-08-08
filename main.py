
from board import SCL, SDA
import busio
import time
from time import sleep
import math
import sys
from adafruit_pca9685 import PCA9685
from xbox360controller import Xbox360Controller

debug = False
gamecont = True
user_in = [0, 0]

move_speed = 1

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50

pos_us = [0, 0, 0, 0, 0]
hard_limit = [[500, 900], [500, 2600], [500, 2600], [500, 2600], [500, 2600], [500, 2600]]

def duty_calc(us):
    if type(us) != int:
        print("pleas enter an int")
        return
    duty = int(us / 1000000 * pca.frequency * 65536)
    return(duty)


def limit_calc():
    global limit
    limit = [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None]]
    limit[1] = [max((pos_us[2]-3100)/-1, hard_limit[1][0]),
                min((pos_us[2]-4100)/-1, hard_limit[1][1])]
    limit[2] = [max(-pos_us[1]+3100, hard_limit[2][0]),
                min(-pos_us[1]+4100, hard_limit[2][1])]
    for i in range(len(limit)):
        if limit[i] == [None, None]:
            limit[i] = hard_limit[i]

def move_servo(servo, pos):
    global pos_us
    limit_calc()
    limit = hard_limit[servo]
    pos = min(limit[1],max(limit[0],pos))
    pos_us[servo] = pos
    duty = duty_calc(pos)
    if debug:
        print(duty)
    else:
        servo = pca.channels[servo]
        servo.duty_cycle = duty

def clean_cont_number(number):
    number *= 10
    number = math.floor(number)
    return number

def start_pos():
    move_servo(0, 700)
    move_servo(1, 1000)
    move_servo(2, 1500)

print("LOADED MODULES:")
for name in sys.modules:
    print(name, "→", sys.modules[name])

try:
    start_pos()
    if gamecont:
        while True:
            with Xbox360Controller(0, axis_threshold=0) as joy:
                l_x = clean_cont_number(joy.axis_l.x)
                l_y = clean_cont_number(joy.axis_l.y)
                l_x *= move_speed
                l_y *= move_speed
                print(l_x, l_y)
                print(pos_us[1]+l_x, pos_us[2]+l_y)
                move_servo(1,pos_us[1]+l_x)
                move_servo(2, pos_us[2]+l_y)

    else:
        while True:
                user_in[0] = int(input("servo"))
                user_in[1] = int(input("pos"))
                move_servo(user_in[0],user_in[1])
except KeyboardInterrupt:
    print("Programm Exit")
    exit()