from board import SCL, SDA
import busio
import time
from time import sleep
import math
from adafruit_pca9685 import PCA9685
from xbox360controller import Xbox360Controller

debug = False
gamecont = True
user_in = [0, 0]

move_speed = 0.1

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50

pos_us = [0, 0, 0, 0, 0, 0]
joy_value = [0, 0, 0, 0, 0, 0]
hard_limit = [[500, 900], [500, 2600], [500, 2600], [500, 2600], [500, 2600], [500, 2600]]

def duty_calc(us):
    if debug:
        print("duty_calc", us)
        print(type(us))
    if type(us) != int:
        print("pleas enter an int")
        return
    duty = int(us / 1000000 * pca.frequency * 65536)
    return(duty)


def limit_calc():
    global limit
    limit = [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None]]
    limit[1] = [int(max((pos_us[2]-3100)/-1, hard_limit[1][0])),
                int(min((pos_us[2]-4100)/-1, hard_limit[1][1]))]
    limit[2] = [int(max(-pos_us[1]+3100, hard_limit[2][0])),
                int(min(-pos_us[1]+4100, hard_limit[2][1]))]
    for i in range(len(limit)):
        if limit[i] == [None, None]:
            limit[i] = hard_limit[i]
    if debug:
        print(limit)

def move_servo(servo, pos, ignore_limit=False):
    global pos_us
    if not ignore_limit:
        limit_calc()
        lim = limit[servo]
    else:
        lim = hard_limit[servo]
    pos = min(lim[1],max(lim[0],pos))
    pos_us[servo] = pos
    duty = duty_calc(pos)
    if debug:
        print(duty)
    else:
        servo = pca.channels[servo]
        servo.duty_cycle = duty

def clean_cont_number(number):
    number *= 10
    number *= move_speed
    number = math.floor(number)
    if debug:
        print(type(number))
    return number

def start_pos():
    move_servo(0, 700)
    move_servo(1, 1000, True)  # Ignore limit for initial position
    move_servo(2, 1500)

try:
    start_pos()
    if gamecont:
        with Xbox360Controller(0, axis_threshold=0) as joy:
            while True:
                joy_value[2] = clean_cont_number(joy.axis_l.x)
                joy_value[1] = clean_cont_number(joy.axis_l.y)
                joy_value[4] = clean_cont_number(joy.axis_r.y)
                joy_value[3] = clean_cont_number(joy.axis_r.x)
                print(joy_value)
                for i in range(len(joy_value)):
                    if joy_value[i] != 0:
                        move_servo(i, pos_us[i] + joy_value[i])


    else:
        while True:
                user_in[0] = int(input("servo"))
                user_in[1] = int(input("pos"))
                move_servo(user_in[0],user_in[1])
except KeyboardInterrupt:
    print("Programm Exit")
    exit()