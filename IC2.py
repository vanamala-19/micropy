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


class IC2(object) :

    def __init__( self) :
        self.type = "IC"
        self.img = 'ic1.bmp'
        self.D=0
        self.L=0
        self.dl=0
        self.N=0
        self.K=0
        self.st=2
        self.pm=0
        self.cv=0
        self.rm=0
        self.ma=0
        self.mf=0
        self.bf=0
        self.T=0
        self.bwd=0
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
        self.graph1 = []
        self.graph2 = []
        self.graph = ""
        self.sv = [self.D,self.L,self.dl,self.N,self.K,self.st,self.pm,self.rm,self.ma,self.mf,self.cv,self.T,self.bf,self.bwd
                   ,self.av,self.sv,self.IP,self.BP,self.FP,self.Me,self.Ve,self.ITe,self.BTe,self.BSFC]
        self.s =  ["Piston Diameter","Stroke Length","Diameter/Length","Speed (N)","No.of Cylinders","No of Strokes","Mean Pressure",
                   "Air/Fuel (a/f)","mass of air(ma)","mass of fuel(mf)","Calorific Value","Torque","Brake Force(N)",
                   "Brake-W-Diameter","Actual Volume","Swept Volume","Indicated Power","Brake Power","Frictional Power","Mech efficiency",
                   "Vol efficiency","I T efficiency","B T efficiency","fuel consumption"]
        self.val =  ["","","","","","","","","","","","","","","","","","","","","","","",""]
        self.unit = [["Cm", "Mm", "M"],["Cm", "Mm", "M"],[],[],[],[],["bar","KN/m^2", "Pa"],[],
                     ["Kg/s","Kg/hr"],["Kg/s","Kg/hr"],[],[],[],["Cm", "MM", "M"],[],[],[],[],[],[],[],[],[],[]]
    def stage1(self):
        tft.fill(TFT.BLACK )
        c=0
        d=tn
        for i in range(0,8):
            if(i>=len(self.s)):
                break
            s = str(i+1)+") "+str(self.s[i])+ "  :"
            tft.text((c,d),s, TFT.GREEN, sysfont, 1,nowrap=True)
            d += 1.8*tn
            if(d >= 120):
                c += 9*tn
                d = tn
    def stage2(self):
        tft.fill(TFT.BLACK )
        c=0
        d=tn
        for i in range(8,16):
            if(i>=len(self.s)):
                break
            s = str(i+1)+") "+str(self.s[i])+ "  :"
            tft.text((c,d),s, TFT.GREEN, sysfont, 1,nowrap=True)
            d += 1.8*tn
            if(d >= 120):
                c += 9*tn
                d = tn
    def stage3(self):
        tft.fill(TFT.BLACK )
        c=0
        d=tn
        for i in range(16,24):
            if(i>=len(self.s)):
                break
            s = str(i+1)+") "+str(self.s[i])+ "  :"
            tft.text((c,d),s, TFT.GREEN, sysfont, 1,nowrap=True)
            d += 1.8*tn
            if(d >= 120):
                c += 9*tn
                d = tn
    
    def calculate(self):
        A = 0
        for i in range(0,len(self.s)):
            if(self.val[i] != ""):
                self.sv[i] = float(self.val[i])
#         try:
        if(self.Me != 0 and self.BP == 0 or self.IP == 0):
            if(self.BP == 0):
                self.BP = float((self.Me*self.IP)/100)
            elif(self.IP == 0):
                self.IP = float((self.BP*100)/self.Me)
                
        if(self.st == 4):
            self.N = self.N/2
            self.img = 'ic2.bmp'
        if(self.D != 0):
            A = float(math.pi*((self.D*self.D)/ 4))
            print("huhu")
        if(self.dl != 0 and self.L != 0 or self.D !=0):
            if(self.D != 0):
                self.L = float(self.d/self.dl)
            elif(self.L != 0):
                self.D = float(self.L*self.dl)
        if(self.dl == 0 and self.L != 0 or self.D != 0):
            if(self.L == 0 and self.D != 0 and self.IP != 0 and self.pm != 0 and A != 0 and self.K !=0 and self.N != 0):
                self.L = float((selp.IP*60)/(self.pm*A*self.N*self.k))
            elif(self.D == 0 and self.L != 0 and self.IP !=0 and self.pm != 0 and A!=0 and self.K !=0 and self.N !=0):
                A = float((selp.IP*60)/(self.pm*self.L*self.N*self.k))
                self.D = math.sqrt((4*A)/math.pi)
        print(A)
        print(self.D)
         
        if(self.IP == 0 and self.D != 0 and self.L != 0 and self.pm != 0 and A != 0 and self.K !=0 and self.N != 0):
             self.IP = float((self.pm*self.L*A*self.N*self.k)/60)
                
        if(self.pm == 0 and self.D != 0 and self.IP !=0 and self.L != 0 and A!=0 and self.K !=0 and self.N !=0):
            self.pm = float((selp.IP*60)/(self.L*A*self.N*self.k))
        elif(self.N == 0 and self.D != 0 and self.IP !=0 and self.L != 0 and A!=0 and self.K !=0 and self.N !=0):
            self.N = float((selp.IP*60)/(self.L*A*self.pm*self.k))
        elif(self.K == 0 and self.D != 0 and self.IP !=0 and self.L != 0 and A!=0 and self.K !=0 and self.N !=0):
            self.K = float((selp.IP*60)/(self.L*A*self.pm*self.N))
            
            
        if(self.T == 0 and self.BP != 0 and self.N != 0):
            self.T = float((selp.BP*60000)/(2*math.pi*self.N))
        elif(self.T == 0 and self.BP == 0 and self.bwd != 0 and self.bf !=0):
            self.T = float((self.bf * (self.bwd / 2)))
        elif(self.T == 0 and self.BP == 0 and self.D != 0 and self.bf !=0):
            self.T = float((self.bf * (self.D / 2)))
            
        if(self.BP == 0 and self.T != 0 and self.N != 0):
            self.BP = float((2*math.pi*self.N*self.T)/60000)
                
        if(self.FP == 0 and self.BP != 0 and self.IP != 0):
            self.FP = float(self.IP - self.BP)
            
        if(self.BSFC == 0 and self.BP != 0 and self.mf != 0):
            self.BSFC = float(mf / self.BP)
                
        if(self.BTe == 0 and self.BP != 0 and self.mf != 0 and self.cv != 0):
            self.BTe = float(self.BP / (mf / 3600 * self.cv))
            
        if(self.BTe == 0 and self.IP != 0 and self.mf != 0 and self.cv != 0):
            self.ITe = (self.IP / (mf / 3600 * self.cv))
                
        if(self.Me == 0 and self.BP != 0 and self.IP != 0):
            self.Me = ((self.BP / self.IP) * 100)
            
            
#         if (self.av == 0 or self.sv == 0 and self.N != 0 and self.L != 0 and self.K !=0 and A != 0):
#             ra = A * self.L * self.N * self.K
#             self.Ve = ((self.ma/3600)/(A*self.L*ra*(self.N/60))*100)
#         elif(self.av != 0 or self.sv != 0) :
#             self.Ve = ((self.av/self.sv)*100)
        self.graph2 = [self.Me,self.Ve,self.ITe,self.BTe]
#             return True
#         except: 
#             tft.text((3*tn, 2*tn),"INCORRECT ", TFT.GREEN, sysfont, 2)
#             tft.text((3*tn, 6*tn),"  INPUT ", TFT.GREEN, sysfont, 2)
#             tft.text((3*tn, 9*tn),"TRY AGAIN", TFT.GREEN, sysfont, 2)
#             return False