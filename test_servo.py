import time
from time import sleep
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo


# I2C-Bus initialisieren
i2c = busio.I2C(SCL, SDA)

# PCA9685-Objekt initialisieren
pca = PCA9685(i2c)
pca.frequency = 50  # Servos erwarten 50 Hz

# 6 Servos initialisieren (auf Kanälen 0 bis 5)
servos = [servo.Servo(pca.channels[i]) for i in range(6)]

