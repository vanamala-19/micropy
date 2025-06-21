from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin
import utime
import math

tn = sysfont["Height"]
n = sysfont["Height"]*18

spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)

class K(object) :
    def __init__( self) :
        self.col_list=[1,2,3,4]
        self.row_list=[5,6,7,8]
        for x in range(0,4):
            self.row_list[x]=Pin(self.row_list[x], Pin.OUT)
            self.row_list[x].value(1)


        for x in range(0,4):
            self.col_list[x] = Pin(self.col_list[x], Pin.IN, Pin.PULL_UP)
    
        self.key_map=[["del","#","0","."],
                        ["C","9","8","7"],
                        ["B","6","5","4"],
                        ["=","3","2","1"]]

    def Keypad(self,cols,rows):
      for r in rows:
        r.value(0)
        result=[cols[0].value(),cols[1].value(),cols[2].value(),cols[3].value()]
        if min(result)==0:
          key=self.key_map[int(rows.index(r))][int(result.index(0))]
          r.value(1) # manages key keept pressed
          return(key)
        r.value(1)
    
    def Read(self,c,d,z=False):
        ans =str()
        key = 0
        j=0
        if(c >= n):
            c = 2*tn
            d += 2*tn
        else:
            d += tn
        while True:
            key = self.Keypad(self.col_list, self.row_list)
            if key != None:
                if key == '=':
                    break
                elif (key == 'B'):
                    return False
                elif key == 'C':
                    if(z):
                        return 'c'
                    else:
                        return True
                elif key == 'del':
                    if(ans == ''):
                        continue
                    l = len(ans)
                    m = ans[l-1]
                    temp = str()
                    for i in range(0,l-1):
                        temp +=ans[i]
                    ans = temp
                    if(c<=0):
                        c=nt
                        d -=2*tn
                    else:
                        c -= tn*1.2
                    tft.text((c, d),str(m), TFT.BLACK,sysfont, 1)
                    utime.sleep(0.5)
                else:
                    tft.text((c,d),key, TFT.WHITE, sysfont, 1)
                    c += tn*1.2
                    ans = ans + key
                    utime.sleep(0.3)
        if(ans == ''):
            return 0
        else:
            return float(ans)