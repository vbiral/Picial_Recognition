import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
gpio.setup(12, gpio.OUT) #Pino da trinca

while (True):
    gpio.output(12,0)
    time.sleep(1)
    gpio.output(12,1)
