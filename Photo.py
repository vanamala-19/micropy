from ST7735 import TFT,TFTColor
from machine import SPI,Pin
spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)

class P(object) :
    def __init__( self) :
        self.p1=0

    def selectPhoto(self,p):
        self.p1 = p
        self.photo()
    def photo(self):
        tft.fill(TFT.BLACK)
        f=open(self.p1, 'rb')
        if f.read(2) == b'BM':  #header
            dummy = f.read(8) #file size(4), creator bytes(4)
            offset = int.from_bytes(f.read(4), 'little')
            hdrsize = int.from_bytes(f.read(4), 'little')
            width = int.from_bytes(f.read(4), 'little')
            height = int.from_bytes(f.read(4), 'little')
            if int.from_bytes(f.read(2), 'little') == 1: #planes must be 1
                depth = int.from_bytes(f.read(2), 'little')
                if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:#compress method == uncompressed
                    rowsize = (width * 3 + 3) & ~3
                    if height < 0:
                        height = -height
                        flip = False
                    else:
                        flip = True
                    w, h = width, height
                    if h > 128: h = 128
                    if w > 160: w = 160
                    tft._setwindowloc((0,0),(w - 1,h - 1))
                    for row in range(h):
                        if flip:
                            pos = offset + (height - 1 - row) * rowsize
                        else:
                            pos = offset + row * rowsize
                        if f.tell() != pos:
                            dummy = f.seek(pos)
                        for col in range(w):
                            bgr = f.read(3)
                            tft._pushcolor(TFTColor(bgr[0],bgr[1],bgr[2]))
        spi.deinit()


