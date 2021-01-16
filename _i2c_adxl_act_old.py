import smbus
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

bus = smbus.SMBus(1)

#activity detect config
bus.write_byte_data(0x53,0x24,10)
int_act = 0x10
intEnable = bus.read_byte_data(0x53,0x2E)
bus.write_byte_data(0x53,0x2E, intEnable | int_act)

#inactivity detect config
bus.write_byte_data(0x53,0x25,10)
bus.write_byte_data(0x53,0x26,1)
int_inact = 0x08
intEnable = bus.read_byte_data(0x53,0x2E)
bus.write_byte_data(0x53,0x2E, intEnable | int_inact)

def my_callback(channel):
    print('AAA')

#GPIO.add_event_detect(4, GPIO.FALLING, callback = my_callback, bouncetime = 300)

while True:
    inter = bus.read_byte_data(0x53,0x30)
    if((inter&0x10)==0x10):
        print("ACT detected\n")
    if((inter&0x08)==0x08):
        print("INACT detected\n")

