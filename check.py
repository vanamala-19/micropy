from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin
from Keypad import K
import framebuf
import utime
import math

tn = sysfont["Height"]
n =sysfont["Height"]*18

spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)

k = K()
print(k.Keypad(k.col_list,k.row_list))
