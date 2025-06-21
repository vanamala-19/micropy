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


class Ic(object) :

    def __init__( self) :
        self.img = 'ic1.bmp'
        self.D=0
        self.du=0
        self.L=0
        self.lu=0
        self.N=0
        self.k=0
        self.st=0
        self.pm=0
        self.pmu=0
        self.cv=0
        self.rm=0
        self.ma=0
        self.mau=0
        self.bf=0
        self.T=0
        self.bwd=0
        self.bwdu=0
        self.av=0
        self.sv=0
        self.IP=0
        self.BP = 0
        self.FP = 0
        self.BSFC = 0
        self.ISFC = 0
        self.BTe = 0
        self.ITe = 0
        self.Me = 0
        self.Ve =0
        self.graph1 = ["Me","Ve","ITe","BTe"]
        self.graph2 = []
        self.graph = "efficiency"

    def stage1(self):
        tft.fill(TFT.BLACK )
        c=0
        d=0
        tft.text((c, d), "Enter the Values: ", TFT.GREEN, sysfont, 1)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "1) Piston Diameter :", TFT.GREEN, sysfont, 1)
        self.D = k.Read(tn*16,tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)CM  2)MM  3)M", TFT.GREEN, sysfont, 1)
        self.du = k.Read(tn*16,d)
        utime.sleep(0.3)
        d +=3*tn
        tft.text((c, d), "2) Stroke Length :", TFT.GREEN, sysfont, 1)
        self.L = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)CM  2)MM  3)M", TFT.GREEN, sysfont, 1)
        self.lu = k.Read(tn*16,d)
        utime.sleep(0.3)
        d += 3*tn;
        tft.text((c, d), "3) Speed in RPM", TFT.GREEN, sysfont, 1)
        self.N = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "4) No of Cylinders", TFT.GREEN, sysfont, 1)
        self.k = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
    
    def stage2(self):
        tft.fill(TFT.BLACK )
        c=0
        d=0
        tft.text((c, d), "5) Strokes 2 or 4 :", TFT.GREEN, sysfont, 1)
        self.st = k.Read(tn*16,-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "6) Mean Pressure :", TFT.GREEN, sysfont, 1)
        self.pm = k.Read(tn*16,tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units:", TFT.GREEN, sysfont, 1)
        tft.text((2*tn, d+tn), "1)Bars   2)KN/m^2   3)Pascls", TFT.GREEN, sysfont, 1)
        self.pmu = k.Read(tn*16,d)
        utime.sleep(0.3)
        d +=4*tn
        tft.text((c, d), "7)Calorific Value :", TFT.GREEN, sysfont, 1)
        self.cv = k.Read(tn*14,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "8) Air/Fuel ratio:", TFT.GREEN, sysfont, 1)
        self.rm = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "9)Mass of air(ma):", TFT.GREEN, sysfont, 1)
        self.ma = k.Read(tn*14,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units", TFT.GREEN, sysfont, 1)
        tft.text((tn*3, d+tn), "1)Kg/s  2)Kg/hr", TFT.GREEN, sysfont, 1)
        self.mau = k.Read(tn*16,d)
        utime.sleep(0.3)
    
    def stage3(self):
        tft.fill(TFT.BLACK )
        c=0
        d=0
        tft.text((c, d), "10)Brake Force (N) :", TFT.GREEN, sysfont, 1)
        self.bf = k.Read(tn*16,-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "11) Torque :", TFT.GREEN, sysfont, 1)
        self.T = k.Read(tn*16,tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "12)Brake Wheel Diameter  :", TFT.GREEN, sysfont, 1)
        self.bwd = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "Units:", TFT.GREEN, sysfont, 1)
        tft.text((2*tn, d+tn), "1)CM   2)MM  3)Meter", TFT.GREEN, sysfont, 1)
        self.bwdu = k.Read(tn*16,d)
        utime.sleep(0.3)
        d +=4*tn
        tft.text((c, d), "13) Actual Volume:", TFT.GREEN, sysfont, 1)
        self.av = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
        d += 2*tn;
        tft.text((c, d), "14) Swept Volume :", TFT.GREEN, sysfont, 1)
        self.sv = k.Read(tn*16,d-tn)
        utime.sleep(0.3)
    
    def calculate(self):
        try:
            str(self.du)
            D = c.diameter(self.D,(self.du))
            L = c.diameter(self.L,(self.lu))
            if((self.st) == 4):
                self.img = 'ic2.bmp'
                self.N = self.N/2
            self.pm = c.pressure(self.pm,(self.pmu))
            ma = c.hmass(self.ma,self.mau)
            mf = self.ma/self.rm
            bwd = c.diameter(self.bwd,(self.bwdu))
            A = float(math.pi*((D*D)/ 4))
            self.IP = float((self.pm*L*A*self.N*self.k)/60)
            if (self.T == 0):
                if (bwd == 0):
                    self.T = (self.bf * (D / 2))
            else:
                self.T = (self.bf * (bwd / 2))
            self.BP = ((2*math.pi*self.N*self.T)/60000)
            self.FP = (self.IP - self.BP)
            self.BSFC = (mf / self.BP)
            self.ISFC = (mf / self.IP)
            self.BTe = (self.BP / (mf / 3600 * self.cv))
            self.ITe = (self.IP / (mf / 3600 * self.cv))
            self.Me = ((self.BP / self.IP) * 100)
            if (self.av == 0 or self.sv == 0):
                ra = A * L * self.N * self.k;
                self.Ve = ((ma/3600)/(A*L*ra*(self.N/60))*100)
            else :
                self.Ve = ((self.av/self.sv)*100)
            self.graph2 = [self.Me,self.Ve,self.ITe,self.BTe]
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
        tft.text((c, d), "4)BSFC:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.BSFC,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"Kg/KWh  ", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "5)ISFC:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.ISFC,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"Kg/KWh  ", TFT.GREEN, sysfont, 1,nowrap=True)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "6)Me:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.Me,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"%", TFT.GREEN, sysfont, 1)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "7)Ve:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.Ve,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"%", TFT.GREEN, sysfont, 1)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "8)ITe:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.ITe,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"%", TFT.GREEN, sysfont, 1)
        utime.sleep(0.2)
        d += 1.8*tn;
        tft.text((c, d), "9)BTe:", TFT.GREEN, sysfont, 1)
        tft.text((tn*9,d),str(round(self.BTe,2)), TFT.GREEN, sysfont, 1)
        tft.text((tn*15,d),"%", TFT.GREEN, sysfont, 1)
        utime.sleep(0.2)
    

    