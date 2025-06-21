from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin
import convert as c
from Keypad import K
import utime
import math

tn = sysfont["Height"]
n =sysfont["Height"]*18
R = 0.287
CP = 1.005;
CV = 0.716

spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)

k = K()


class GT(object) :

    def __init__( self) :
        self.p=0
        self.p1u=0
        self.t1=0
        self.t1u=0
        self.t2=0
        self.t2u=0
        self.t3=0
        self.t3u=0
        self.t4=0
        self.t4u=0
        self.pr=0
        self.v=0
        self.THe=0
        self.pow=0
        self.bwr=0
        self.Wnet=0
        self.WT=0
        self.WC=0
        self.Ce=0
        self.Te=0
        self.img = "gt.bmp"
        self.graph1 = ["THe","Te","Ce","BWR"]
        self.graph2 = []
        self.graph = "efficiency"

    def stage1(self):
        tft.fill(TFT.BLACK )
        c=0
        d=0
        tft.text((c, d), "Enter the Values: ", TFT.GREEN, sysfont, 1)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "1) pressure (P)1 :", TFT.GREEN, sysfont, 1)
        self.p = k.Read(tn*16,tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)bars 2)KN/m^2  3)pascls", TFT.GREEN, sysfont, 1)
        self.p1u = k.Read(tn*16,d)
        utime.sleep(0.3)
        d +=4*tn
        tft.text((c, d), "2)Tempurature T1:", TFT.GREEN, sysfont, 1)
        self.t1 = k.Read(tn*14,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)celsius  2)Kelvin 3)fahrenheit", TFT.GREEN, sysfont, 1)
        self.t1u = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        d +=4*tn
        tft.text((c, d), "4) pressure ratio :", TFT.GREEN, sysfont, 1)
        self.pr = k.Read(tn*16,d-tn)
        
        
    def stage2(self):
        tft.fill(TFT.BLACK )
        c=0
        d=0
        utime.sleep(0.3)
        tft.text((c, d), "5)Tempurature T2:", TFT.GREEN, sysfont, 1)
        self.t2 = k.Read(tn*14,d-tn)
        utime.sleep(0.3)
        d +=2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)celsius  2)Kelvin 3)fahrenheit", TFT.GREEN, sysfont, 1)
        self.t2u = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        d += 4*tn;
        tft.text((c, d), "6)Tempurature T3:", TFT.GREEN, sysfont, 1)
        self.t3 = k.Read(tn*14,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)celsius  2)Kelvin 3)fahrenheit", TFT.GREEN, sysfont, 1)
        self.t3u = k.Read(tn*16,d)
        
    def stage3(self):
        tft.fill(TFT.BLACK )
        c=0
        d=0
        utime.sleep(0.3)
        tft.text((c, d), "7)Tempurature T4:", TFT.GREEN, sysfont, 1)
        self.t4 = k.Read(tn*14,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)celsius  2)Kelvin 3)fahrenheit", TFT.GREEN, sysfont, 1)
        self.t4u = k.Read(tn*16,d)
        utime.sleep(0.3)
        d += 4*tn;  
        tft.text((c, d), "8)  Volume:", TFT.GREEN, sysfont, 1)
        self.v = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        
    def calculate(self):
        try:
            self.p = c.diameter(self.p,(self.p1u))
            self.t2 = c.tempurature(self.t2,(self.t2u))
            self.t1 = c.tempurature(self.t1,self.t1u)
            self.t3 = c.tempurature(self.t3,(self.t3u))
            self.t4 = c.tempurature(self.t4,(self.t4u))
            n = 1.4;
            T2x = self.t1 * math.pow(self.pr, (n - 1) / n)
            T4x = self.t3 / (math.pow(self.pr, (n - 1) / n))
            if (self.t2==0) :
                self.WC = (CP * (T2x - self.T1))
            else :
                self.WC = (CP * (self.t2 -self.t1))
        
            if (self.t4 == 0):
                self.WT = (CP * (self.t3 - T4x))
            else:
                self.WT = (CP * (self.t3 - self.t4))
        
            self.Wnet = (self.WT - self.WC)
            qin = CP * (self.t3 - self.t2)
            qout = CP * (self.t4 - self.t1)
            self.THe = ((self.Wnet / qin) * 100)
            self.Te = (((self.t3 - self.t4) / (self.t3 - T4x)) * 100)
            self.Ce = (((T2x - self.t1) / (self.t2 - self.t1)) * 100)
            self.bwr = ((self.WC / self.WT) * 100)
            ma = (self.p * self.v) / R * self.t1;
            self.pow = ma * self.Wnet;
            self.graph2 = [self.THe,self.Te,self.Ce,self.bwr]
            return True
        except: 
            tft.text((3*tn, 2*tn),"INCORRECT ", TFT.GREEN, sysfont, 2)
            tft.text((3*tn, 6*tn),"  INPUT ", TFT.GREEN, sysfont, 2)
            tft.text((3*tn, 9*tn),"TRY AGAIN", TFT.GREEN, sysfont, 2)
            return False
    def table(self):
        c=tn
        d=0
        tft.text((c, d), "1)WC :", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,0 ),str(round(self.WC,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,0 ),"KW", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "2) WT:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.WT,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d ),"KW", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "3) Wnet:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.Wnet,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"KW", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "4) Pow:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.pow,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"KW", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "5)THe:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.THe,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"%", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "6)Te:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.Te,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"%", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "7)Ce:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.Ce,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"%", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "9)bwr:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.bwr,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"%", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        