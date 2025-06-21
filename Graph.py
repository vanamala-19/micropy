from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin
import utime


tn = sysfont["Height"] 
n =sysfont["Height"]*18

spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)


class G(object):
    
    def __init__( self) :
        self.x = [30,66,100,135]
        self.tx = [35,72,102,138]
        self.y = 0
        self.h =0
        self.c = [TFT.WHITE,TFT.BLUE,TFT.GREEN,TFT.RED]
    
    def graph(self,g1,g2,g):
        tft.fill(TFT.BLACK )
        tft.line((20,6),(20,120),TFT.WHITE)
        tft.line((12,108),(160,108),TFT.WHITE)
        if(g == "efficiency"):
            
            x=8
            z = 2
            p = 100
            
            for y in range(0,6):
                tft.line((18,x),(22,x),TFT.WHITE)
                v = p
                tft.text((z,x),str(v),TFT.WHITE, sysfont,1)
                x += 20
                p -= 20
            l = len(g1)
            for i in range(0,l):
                if(g2[i]>=100):
                    self.y = 8
                    self.h = 100
                elif(g2[i]>=90):
                    self.y = 18
                    self.h = 90
                elif(g2[i]>=80):
                    self.y = 28
                    self.h = 80
                elif(g2[i]>=70):
                    self.y = 38
                    self.h = 70
                elif(g2[i]>=60):
                    self.y = 48
                    self.h = 60
                elif(g2[i]>=50):
                    self.y = 58
                    self.h = 50
                elif(g2[i]>=40):
                    self.y = 68
                    self.h = 40
                elif(g2[i]>=30):
                    self.y = 78
                    self.h = 30
                elif(g2[i]>=20):
                    self.y = 88
                    self.h = 20
                elif(g2[i]>=10):
                    self.y = 98
                    self.h = 10
                else:
                    self.y = 108
                    self.h = 0
                utime.sleep(0.1)
                tft.fillrect((self.x[i],self.y),(20,self.h),self.c[i])
                tft.text((self.tx[i],112),g1[i],TFT.WHITE, sysfont,1,nowrap=True)
                tft.text((self.x[i],self.y-tn),str(round(g2[i],2)),TFT.WHITE, sysfont,1,nowrap=True)
            return
        elif(g == "power"):    
            m1 = max(g2)
            l = len(g1)
            for i in range(0,l):
                val = (g2[i]/m1)*100
                if(val>=100):
                    self.y = 8
                    self.h = 100
                elif(val>=90):
                    self.y = 18
                    self.h = 90
                elif(val>=80):
                    self.y = 28
                    self.h = 80
                elif(val>=70):
                    self.y = 38
                    self.h = 70
                elif(val>=60):
                    self.y = 48
                    self.h = 60
                elif(val>=50):
                    self.y = 58
                    self.h = 50
                elif(val>=40):
                    self.y = 68
                    self.h = 40
                elif(val>=30):
                    self.y = 78
                    self.h = 30
                elif(val>=20):
                    self.y = 88
                    self.h = 20
                elif(val>=10):
                    self.y = 98
                    self.h = 10
                else:
                    self.y = 108
                    self.h = 0
                utime.sleep(0.1)
                tft.fillrect((self.x[i],self.y),(20,self.h),self.c[i])
                tft.text((self.tx[i],112),g1[i],TFT.WHITE, sysfont,1,nowrap=True)
                tft.text((self.x[i],self.y-tn),str(round(g2[i],2)),TFT.WHITE, sysfont,1,nowrap=True)
            return


