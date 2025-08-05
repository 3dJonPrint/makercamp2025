from board import SCL, SDA
import busio
import time
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50

channel = pca.channels[0]  # Beispiel: CH1

def set_pwm_us(us):
    duty = int(us / 1000000 * pca.frequency * 65536)
    channel.duty_cycle = duty

# Stopp (meist 1500 µs)
set_pwm_us(1500)
time.sleep(2)

# Vorwärts
set_pwm_us(1600)
time.sleep(3)

# Rückwärts
set_pwm_us(1400)
time.sleep(3)

# Stopp
set_pwm_us(1500)
