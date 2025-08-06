from board import SCL, SDA
import busio
import time
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50

#channel = pca.channels[0]  # Beispiel: CH1

def set_pwm_us(us):
    duty = int(us / 1000000 * pca.frequency * 65536)
    channel.duty_cycle = duty

try:
    channel = None
    while True:
        user_in = input()
        if "ch" in user_in:
            user_in = user_in[2:]
            user_in = user_in.strip()
            channel = pca.channels[int(user_in)]
        if channel == None:
            print("pleas select ch")
            continue
        set_pwm_us(int(user_in))
except KeyboardInterrupt:
    print("Programm End")
    exit()
