import smbus
import RPi.GPIO as GPIO
from time import sleep
import datetime

GPIO.setmode(GPIO.BCM)
bus = smbus.SMBus(1)

bus.write_byte_data(0x53,0x31,0x2B) #initial data format and fall edge interrupt
bus.write_byte_data(0x53,0x24,0x16) #set ACT THREHOLD
bus.write_byte_data(0x53,0x25,0x16) #set INACT THREHOLD
bus.write_byte_data(0x53,0x26,0x01) 
bus.write_byte_data(0x53,0x27,0x66) #set ACT_x ACT_y INACT_x INACT_y
bus.write_byte_data(0x53,0x2F,0x10) #set INT2 pin receive ACT interrupt
#bus.write_byte_data(0x53,0x2E,0x10) #enable ACT INACT interrupt
bus.write_byte_data(0x53,0x2E,0x18) #enable ACT INACT interrupt
bus.write_byte_data(0x53,0x2D,0x08) #start measure

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP) #interrupt
GPIO.setup(26, GPIO.OUT) #ana


def my_callback(channel):
    print('Interrupt')
    GPIO.output(26, True)

GPIO.add_event_detect(4, GPIO.FALLING, callback = my_callback, bouncetime = 300)

start_time = datetime.datetime.now()
print(start_time)

'''
conf = {}
conf['GPIO_mode'] = GPIO.BOARD
conf['pin'] = 26
conf['freq'] = 10

GPIO.setwarnings(False)
GPIO.setup(conf['pin'], GPIO.OUT)

def blink(conf):
    GPIO.output(conf['pin'], GPIO.HIGH)
    sleep(0.5/conf['freq'])
    GPIO.output(conf['pin'], GPIO.LOW)
    sleep(0.5/conf['freq'])
    return
'''


try:
    while True:
        
        inter = bus.read_byte_data(0x53,0x30)
        GPIO.output(26, False)

        if (datetime.datetime.now() - start_time).seconds == 5:
            start_time = datetime.datetime.now()
            print(start_time)
        
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()


