from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin
import convert as c
from Keypad import K
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


class JT(object) :

    def __init__( self) :
        self.type="JTE"
        self.Vjet=0
        self.Vjetu=0
        self.s=0
        self.av=0
        self.avu=0
        self.ma=0
        self.mau=0
        self.mf=0
        self.mfu=0
        self.cv=0
        self.D=0
        self.Du=0
        self.da=0
        self.sv=0
        self.mr=0
        self.mru=0
        self.img = 'jt.bmp'
        self.graph1 = ["Prope","THe","Overalle"]
        self.graph2 = []
        self.graph = "efficiency"
        
    def stage1(self):
        tft.fill(TFT.BLACK )
        c=0
        d=0
        tft.text((c, d), "Enter the Values: ", TFT.GREEN, sysfont, 1)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "1) jet velocity :", TFT.GREEN, sysfont, 1)
        self.Vjet = k.Read(tn*16,tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)m/s  2)km/hr  3)miles/hr", TFT.GREEN, sysfont, 1)
        self.Vjetu = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        d +=4*tn
        tft.text((c, d), "2) velocity ratio :", TFT.GREEN, sysfont, 1)
        self.s = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "3) aircraft velocity", TFT.GREEN, sysfont, 1)
        self.av = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)m/s  2)km/hr  3)miles/hr", TFT.GREEN, sysfont, 1)
        self.jvu = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
    
    def stage2(self):
        tft.fill(TFT.BLACK )
        c=0
        d=0
        tft.text((c, d), "5)Mass of air(ma):", TFT.GREEN, sysfont, 1)
        self.ma = k.Read(tn*16,-tn)
        utime.sleep(0.3)
        d += 2.4*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)Kg/s  2)Kg/min", TFT.GREEN, sysfont, 1)
        self.mau = k.Read(tn*16,d)
        utime.sleep(0.3)
        d += 2.4*tn;
        tft.text((c, d), "8)Mass of fuel(mf):", TFT.GREEN, sysfont, 1)
        self.mf = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        d += 2.4*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)Kg/s  2)Kg/min", TFT.GREEN, sysfont, 1)
        self.mfu = k.Read(tn*16,d)
        utime.sleep(0.3)
        d += 2.4*tn;
        tft.text((c, d), "9)calorific value:", TFT.GREEN, sysfont, 1)
        self.cv = k.Read(tn*14,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "10)nozzle diameter:", TFT.GREEN, sysfont, 1)
        self.D = k.Read(tn*14,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)cm  2)mm 3)m", TFT.GREEN, sysfont, 1)
        self.Du = k.Read(tn*16,d)
        utime.sleep(0.3)
    
    def calculate(self):
        try:
            self.ma = c.mass(self.ma, self.mau)
            self.mf = c.mass(self.mf, self.mfu)
            if (self.Vjetu == 1):
                self.Vjet = self.Vjet
            elif (self.Vjetu == 2):
              self.Vjet = self.Vjet * (5 / 18)
            elif (self.Vjetu == 3):
              self.Vjet = self.Vjet / 2.237
            if (self.s != 0):
                self.av = self.s * self.Vjet;
            else :
                if (self.avu == 1):
                    self.av = self.av
                elif (self.avu == 2):
                    self.av = self.av * (5 / 18)
                elif (self.avu == 3):
                    self.av = self.av / 2.237
                self.s = self.av / self.Vjet
            self.D = c.diameter(self.D, self.Du);
            Ae = float(math.pi*((self.D*self.D)/ 4))
            self.F = ((self.ma + self.mf) * (self.Vjet - self.av) / 1000)
            self.Fmom = self.ma * self.Vjet
            self.Sthrust = ((self.F * 1000) / (self.ma + self.mf))
            self.Isp = ((self.F * 1000) / ((self.ma +self.mf)* 9.81))
            self.Pthrust = (self.F * self.av)
            self.PPropulsion = ((self.ma * (((self.Vjet * self.Vjet) - (self.av * self.av)) / 2)) / 1000)
            self.Prope = ((self.Pthrust / self.PPropulsion) * 100)
            self.Te = (self.PPropulsion / (self.mf * self.cv) * 100)
            self.Overalle = ((self.Prope * self.Te) / 100)
            self.graph2 = [self.Prope,self.Te,self.Overalle]
            return True
        except: 
            tft.text((3*tn, 2*tn),"INCORRECT ", TFT.GREEN, sysfont, 2)
            tft.text((3*tn, 6*tn),"  INPUT ", TFT.GREEN, sysfont, 2)
            tft.text((3*tn, 9*tn),"TRY AGAIN", TFT.GREEN, sysfont, 2)
            return False
        
    def table(self):
        c=tn
        d=0
        tft.text((c, d), "1)Thrust :", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,0 ),str(round(self.F,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,0 ),"KN", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "2) S-Thrust:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.Sthrust,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d ),"N/kg", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.5*tn;
        tft.text((c, d), "3) ISP:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.Isp,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"sec", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "4)Pthrust:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.Pthrust,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"KW", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "5)PProp:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.PPropulsion,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"KW", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "6)Prope:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.Prope,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"%", TFT.GREEN, sysfont, 1)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "7)THe:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.Te,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"%", TFT.GREEN, sysfont, 1)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "8)Overalle:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.Overalle,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"%", TFT.GREEN, sysfont, 1)
        