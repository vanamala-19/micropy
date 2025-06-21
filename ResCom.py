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


class RESC(object) :

    def __init__( self) :
       self.n=0
       self.k=0
       self.tps=0
       self.N=0
       self.D=0
       self.du=0
       self.L=0
       self.lu=0
       self.p1=0
       self.p1u=0
       self.p2=0
       self.p2u=0
       self.p4=0
       self.p4u=0
       self.t1=0
       self.t1u=0
       self.t3=0
       self.t3u=0
       self.v=0
       self.ma=0
       self.mau=0
       self.IP=0
       self.BP=0
       self.FP=0
       self.Me=0
       self.Mpow=0
       self.T=0
       self.img = 'res.bmp'
       self.graph1 = ["Mpow","IP","BP","FP"]
       self.graph2 = []
       self.graph = "power"




    def stage1(self):
        tft.fill(TFT.BLACK )
        c=0
        d=0
        tft.text((c, d), "Enter the Values: ", TFT.GREEN, sysfont, 1)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "1) Types of Process :", TFT.GREEN, sysfont, 1)
        tft.text((tn, d+tn), "1)isothermal  2)adibatic  3)polytropic", TFT.GREEN, sysfont, 1)
        self.n = k.Read(tn*16,tn)
        utime.sleep(0.3)
        d += 4*tn;
        tft.text((c, d), "2) Types of Compressors", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)single acting   2)double acting", TFT.GREEN, sysfont, 1)
        self.k = k.Read(tn*16,d)
        utime.sleep(0.3)
        d += 4*tn;
        tft.text((c, d), "3) Types of Stages", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)single stage    2)double Stage", TFT.GREEN, sysfont, 1)
        self.tps = k.Read(tn*16,d)
        utime.sleep(0.3)
        d += 4*tn;
        tft.text((c, d), "4) Speed in RPM", TFT.GREEN, sysfont, 1)
        self.N = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        
    
    def stage2(self):
        tft.fill(TFT.BLACK )
        c=0
        d=0
        tft.text((c, d), "5) Piston Diameter :", TFT.GREEN, sysfont, 1)
        self.D = k.Read(tn*16,-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)CM  2)MM  3)M", TFT.GREEN, sysfont, 1)
        self.du = k.Read(tn*16,d)
        utime.sleep(0.3)
        d += 3*tn;
        tft.text((c, d), "6) Stroke Length :", TFT.GREEN, sysfont, 1)
        self.L = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)CM  2)MM  3)M", TFT.GREEN, sysfont, 1)
        self.lu = k.Read(tn*16,d)
        utime.sleep(0.3)
        d += 3*tn
        tft.text((c, d), "7) Pressure p1 :", TFT.GREEN, sysfont, 1)
        self.p1 = k.Read(tn*16,d)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units:", TFT.GREEN, sysfont, 1)
        tft.text((2*tn, d+tn), "1)Bars   2)KN/m^2   3)Pascls", TFT.GREEN, sysfont, 1)
        self.p1u = k.Read(tn*16,d)
        utime.sleep(0.3)
    
    def stage3(self):
        tft.fill(TFT.BLACK )
        c=0
        d=0
        tft.text((c, d), "8) Pressure p2 :", TFT.GREEN, sysfont, 1)
        self.p2 = k.Read(tn*16,-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units:", TFT.GREEN, sysfont, 1)
        tft.text((2*tn, d+tn), "1)Bars   2)KN/m^2   3)Pascls", TFT.GREEN, sysfont, 1)
        self.p2u = k.Read(tn*16,d)
        utime.sleep(0.3)
        d +=4*tn
        tft.text((c, d), "9)Tempurature T1:", TFT.GREEN, sysfont, 1)
        self.t1 = k.Read(tn*14,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)celsius  2)Kelvin 3)fahrenheit", TFT.GREEN, sysfont, 1)
        self.t1u = k.Read(tn*16,d)
        utime.sleep(0.3)
        d += 4*tn;
        tft.text((c, d), "10)  Volume:", TFT.GREEN, sysfont, 1)
        self.v = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "11) Torque :", TFT.GREEN, sysfont, 1)
        self.T = k.Read(tn*16,d)
        utime.sleep(0.3)
        
    
    def stage4(self):
        tft.fill(TFT.BLACK )
        c=0
        d=0
        tft.text((c, d), "12)Mass flow rate(ma):", TFT.GREEN, sysfont, 1)
        self.ma = k.Read(tn*16,d)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)Kg/s  2)Kg/min", TFT.GREEN, sysfont, 1)
        self.mau = k.Read(tn*16,d)
        utime.sleep(0.3)
        if(self.tps == 2):
            d += 3*tn;
            tft.text((c, d), "13)Tempurature T3:", TFT.GREEN, sysfont, 1)
            self.t3 = k.Read(tn*16,d-tn)
            utime.sleep(0.3)
            d += 2*tn;
            tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
            tft.text((tn*3, d+tn), "1)celsius  2)Kelvin 3)fahrenheit", TFT.GREEN, sysfont, 1)
            self.t3u = k.Read(tn*16,d)
            utime.sleep(0.3)
            d +=4*tn
            tft.text((c, d), "14) Pressure p4 :", TFT.GREEN, sysfont, 1)
            self.p4 = k.Read(tn*16,d)            
            utime.sleep(0.3)
            d +=2*tn
            tft.text((c, d), "Units:", TFT.GREEN, sysfont, 1)
            tft.text((2*tn, d+tn), "1)Bars   2)KN/m^2   3)Pascls", TFT.GREEN, sysfont, 1)
            self.p4u = k.Read(tn*16,d+tn)
            utime.sleep(0.3)
            
    def calculate(self):
        try:
            if(self.n == 2):
                self.n = 1.3
            elif(self.n == 3):
                self.n = 1.4
            else:
                self.n = 1
            D = c.diameter(self.D,(self.du))
            L = c.diameter(self.L,(self.lu))
            self.p1 = c.pressure(self.p1,(self.p1u))
            self.p2 = c.pressure(self.p2,(self.p2u))
            self.t1 = c.tempurature(self.t1, self.t1u)
            if(self.tps == 2):
                p3 = self.p2
                self.p4 = c.pressure(self.p4,(self.p4u))
                self.t3 = c.tempurature(self.t3, self.t3u)
                T4 = self.t3 * math.pow((self.p4 / p3), (self.n - 1) / self.n)
            ma = c.mass(self.ma,self.mau)
            if (self.ma == 0 ):
                ma = ((self.p1 * self.v) / (R * self.t1))
            mf = 1.4;
            T2 = self.t1 * math.pow((self.p2 / self.p1), ((mf - 1) / mf))
            if (self.n == 1):
                self.Win = self.p1 * self.v * (math.log(self.p2 / self.p1))
            else:
                self.Win = (self.n / (self.n - 1) * (self.p1 * self.v) * (math.pow((self.p2 / self.p1), (self.n - 1) / self.n)))
            if (self.tps == 1):
                self.IP = (self.Win * self.N * self.k / 60)
            else:
                if (ma == 0) :
                    IP1 = (self.Win * self.N * self.k / 60)
                else :
                    IP1 = ((mf / (mf - 1)) * self.ma * R * (T2 - self.t1))
                IP2 = (self.n / (self.n - 1) * self.ma * R * (T4 - self.t3))
                self.IP = IP1 + IP2;
            self.BP = ((2*math.pi*self.N*self.T )/60000)
            self.FP = (self.IP - self.BP)
            self.Me = ((self.IP / self.BP) * 100)
            print(self.IP)
            print(self.BP)
            print(self.FP)
            print(self.Me)
            self.Mpow = (self.BP / self.Me)
            self.graph2 = [self.Mpow,self.IP,self.BP,self.FP]
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
        tft.text((c, d), "5)Mpow:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.Mpow,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"KW", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
    

