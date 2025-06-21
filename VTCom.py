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

spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)

k = K()


class VTC(object) :
    def __init__( self) :
        self.N=0
        self.p1=0
        self.p1u=0
        self.p2=0
        self.p2u=0
        self.p3=0
        self.p3u=0
        self.v=0
        self.t1=0
        self.t1u=0
        self.ma=0
        self.mau=0
        self.T=0
        self.IP=0
        self.BP=0
        self.FP=0
        self.Wvane=0
        self.Me=0
        self.Vanee=0
        self.img = 'vt.bmp'
        self.graph1 = ["Wvane","IP","BP","FP"]
        self.graph2 = []
        self.graph = "power"

    def stage1(self):
        tft.fill(TFT.BLACK )
        c=0
        d=0
        tft.text((c, d), "Enter the Values: ", TFT.GREEN, sysfont, 1)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "1) No of vanes :", TFT.GREEN, sysfont, 1)
        self.N = k.Read(tn*16,tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "2) Pressure p1 :", TFT.GREEN, sysfont, 1)
        self.p1 = k.Read(tn*16,d)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units:", TFT.GREEN, sysfont, 1)
        tft.text((2*tn, d+tn), "1)Bars   2)KN/m^2   3)Pascls", TFT.GREEN, sysfont, 1)
        self.p1u = k.Read(tn*16,d)
        utime.sleep(0.3)
        d +=4*tn
        tft.text((c, d), "3) Pressure p2 :", TFT.GREEN, sysfont, 1)
        self.p2 = k.Read(tn*16,d)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units:", TFT.GREEN, sysfont, 1)
        tft.text((2*tn, d+tn), "1)Bars   2)KN/m^2   3)Pascls", TFT.GREEN, sysfont, 1)
        self.p2u = k.Read(tn*16,d)
        utime.sleep(0.3)
        
    def stage2(self):
        tft.fill(TFT.BLACK )
        c=0
        d=0
        tft.text((c, d), "4) Pressure p3 :", TFT.GREEN, sysfont, 1)
        self.p2 = k.Read(tn*16,-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units:", TFT.GREEN, sysfont, 1)
        tft.text((2*tn, d+tn), "1)Bars   2)KN/m^2   3)Pascls", TFT.GREEN, sysfont, 1)
        self.p3u = k.Read(tn*16,d)
        utime.sleep(0.3)
        d +=4*tn
        tft.text((c, d), "5)  Volume:", TFT.GREEN, sysfont, 1)
        self.v = k.Read(tn*14,d-tn)
        utime.sleep(0.3)
        d +=2*tn
        tft.text((c, d), "6)Tempurature T1:", TFT.GREEN, sysfont, 1)
        self.t1 = k.Read(tn*14,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)celsius  2)Kelvin 3)fahrenheit", TFT.GREEN, sysfont, 1)
        self.t1u = k.Read(tn*16,d)
        utime.sleep(0.3)
        
        
    def stage3(self):
        c=0
        d=0
        d += 2*tn;
        tft.text((c, d), "7)Mass flow rate(ma):", TFT.GREEN, sysfont, 1)
        self.ma = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)Kg/s  2)Kg/min", TFT.GREEN, sysfont, 1)
        self.mau = k.Read(tn*16,d)
        utime.sleep(0.3)
        d += 3*tn;
        tft.text((c, d), "8) Torque :", TFT.GREEN, sysfont, 1)
        self.T = k.Read(tn*16,d)
        utime.sleep(0.3)

    def calculate(self):
        try:
            self.p1 = c.diameter(self.p1,(self.p1u))
            self.p2 = c.diameter(self.p2,(self.p2u))
            self.p3 = c.diameter(self.p3,(self.p3u))
            self.t1 = tempurature(self.t1,self.t1u)
            ma = c.mass(self.ma,self.mau)
            if (isNaN(v)) :
                if (ma != 0 and T != 0) :
                    self.v = (self.ma * R * self.t1) / self.p1   
            n = 1.4;
            W1 = (n / (n - 1) * (p1 * v) * (math.pow((p2 / p1), (n - 1) / n) - 1))
            v2 = self.v * math.pow((self.p1 / self.p2), (1 / n))
            W2 = (v2 * (self.p3 - self.p2))
            self.Wvane = (self.N * (W1 + W2))
            self.IP = (self.W1 + self.W2);
            self.Vanee = ((self.W2) / IP)
            self.BP = ((2*math.pi*self.N*self.T)/60000)
            self.FP = (self.IP - self.BP)
            self.Me = ((self.IP / self.BP) * 100)
            self.graph2 = [self.Wvane,self.IP,self.BP,self.FP]
            return True
        except: 
            tft.text((3*tn, 2*tn),"INCORRECT ", TFT.GREEN, sysfont, 2)
            tft.text((3*tn, 6*tn),"  INPUT ", TFT.GREEN, sysfont, 2)
            tft.text((3*tn, 9*tn),"TRY AGAIN", TFT.GREEN, sysfont, 2)
            return False
    
    def table(self):
        c=tn
        d=0
        tft.text((c, d), "1)IP :", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,0 ),str(round(self.IP,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,0 ),"KW", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "2) BP:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.BP,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d ),"KW", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.5*tn;
        tft.text((c, d), "3) FP:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.FP,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"KW", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "4)Me:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.Me,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"%", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "4)Vanee:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.Vanee,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"%", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "5)Wvane:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.Wvane,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"KW", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
    

    