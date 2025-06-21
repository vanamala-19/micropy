from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin
from IC import Ic
import convert as C
from IC2 import IC2
from ResCom import RESC
from RTBCom import RTBC
from VTCom import VTC
from CFCom import CFC
from GTE import GT
from JTE import JT
from RE import R
from Photo import P
from Keypad import K
from Graph import G
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

engine = 0

conversion = ["Area","Energy","Force","Distance","Mass","Power","Pressure","Speed / Velocity","Tempurature","Torque","Volume"]


unit = [["sq.cm", "sq.m", "sq.km", "sq.inches"],["Joule", "Kilo Watt hour", "kP m", "K cal", "BTU"],["N", "Kp", "P", "Oz", "Ibf"],
        ["mm", "cm", "m", "inch", "foot", "km", "mile"],["gram", "Kg", "Lb", "Ton"],["Kilo Watt", "PS", "Horse power", "Kp m/s", "K cal/s"],
        ["bar", "Pa", "atm", "PSI", "Kg/cm^2"],["cm/s", "m/s", "Km/hr", "mile/hr"],["celsius", "Kelvin", "Farenheit"],
        ["N cm", "N m", "N mm", "dyn m", "Kgf m", "gf m"],["mili liter", "liter", "cubic meter", "cubic inch", "cubic feet"]];
factor = [[1, 0.0001, 0.0000000001, 0.15],[1, 0.2778, 0.1019, 0.0002388, 0.0009478],[1, 0.1019, 101.972, 3.59694, 0.2248],
          [1, 0.1, 0.001, 0.03937, 0.003280, 0.000001, 0.0000006213],[1, 0.001, 0.002204, 0.000001102],[1, 1.35962, 1.34102, 101972, 0.2388],
          [1, 100000, 0.9869, 14.504, 1.0197],[1, 0.01, 0.036, 0.02237],[1, 273.15, 1.8 + 32],
          [1, 0.01, 10, 1000, 0.001019716, 1.019716213],[1, 0.001, 0.000001, 0.061023744094732, 0.000035314666721489]];

def start():
    tft.fill(TFT.BLACK )
    c=0
    d=0
    tft.text((c, d), "Choose the domain", TFT.GREEN, sysfont, 1)
    utime.sleep(0.3)
    d += 1.8*tn;
    tft.text((c, d), "1) Internal   Combustion     Engine", TFT.GREEN, sysfont, 1)
    utime.sleep(0.3)
    d += 3*tn;
    tft.text((c, d), "2) Turbine Engine", TFT.GREEN, sysfont, 1)
    utime.sleep(0.3)
    d += 1.8*tn;
    tft.text((c, d), "3) Jet Engine", TFT.GREEN, sysfont, 1)
    utime.sleep(0.3)
    d += 1.8*tn;
    tft.text((c, d), "4) Compressors Engine", TFT.GREEN, sysfont, 1)
    utime.sleep(0.3)
    d += 1.8*tn;
    tft.text((c, d), "5) Rocket Engine", TFT.GREEN, sysfont, 1)
    utime.sleep(0.3)
    d += 1.8*tn;
    tft.text((c, d), "6) Unit Conversion", TFT.GREEN, sysfont, 1)
    
def convertor():
    tft.fill(TFT.BLACK )
    c=0
    d=tn
    for i in range(0,len(conversion)):
        s = str(i+1)+") "+str(conversion[i])+ "  :"
        tft.text((c,d),s, TFT.GREEN, sysfont, 1)
        d += 1.5*tn
        if(d >= 120):
            c += 9*tn
            d = tn
#     print("c :{} and d :{}".format(c+2*tn,d))

    

def press():
    tft.text((5*tn, 12*tn), "press Any Key", TFT.WHITE , sysfont, 1)  
    for i in range(0,2): 
        utime.sleep(0.5)
        tft.fillrect((5*tn,12*tn),(80,20),TFT.BLACK)
        utime.sleep(0.2)
        tft.text((5*tn, 12*tn), "press Any Key", TFT.WHITE , sysfont, 1)
     
        
        
def compressor():
    tft.fill(TFT.BLACK )
    tft.text((0,tn), "Choose Type Of Compressor:", TFT.GREEN, sysfont, 1)
    utime.sleep(0.5)
    tft.text((0,tn*3), "1)Resiprocatory Compressor:", TFT.GREEN, sysfont, 1)
    utime.sleep(0.3)
    tft.text((0,tn*5), "2)Rotary Compressor :", TFT.GREEN, sysfont, 1)
    ct = k.Read(tn*16,4*tn)
    if(ct == 1):
        engine = RESC()
        tft.fill(TFT.BLACK )
        tft.text((4*tn, 2*tn), "You  have", TFT.GREEN, sysfont, 2)
        tft.text((4*tn, 6*tn), "choosen", TFT.GREEN, sysfont, 2)
        tft.text((tn, 9*tn), "Resiprocatory", TFT.GREEN, sysfont, 2)
        tft.text((3*tn, 12*tn), "Compressor", TFT.GREEN, sysfont, 2)
        utime.sleep(1)
        tft.fill(TFT.BLACK )
        engine.stage1()
        tft.fill(TFT.BLACK )
        engine.stage2()
        tft.fill(TFT.BLACK )
        engine.stage3()
        tft.fill(TFT.BLACK )
        engine.stage4()
        tft.fill(TFT.BLACK )
        return engine

    elif(ct == 2):
        tft.fill(TFT.BLACK )
        tft.text((4*tn, 2*tn), "You  have", TFT.GREEN, sysfont, 2)
        tft.text((4*tn, 6*tn), "choosen", TFT.GREEN, sysfont, 2)
        tft.text((5*tn, 9*tn), "Rotary", TFT.GREEN, sysfont, 2)
        tft.text((3*tn, 12*tn), "Compressor", TFT.GREEN, sysfont, 2)
        utime.sleep(1)
        tft.fill(TFT.BLACK )
        tft.text((0,tn), "Choose Type Of Compressor:", TFT.GREEN, sysfont, 1)
        utime.sleep(0.5)
        tft.text((0,tn*3), "1)Root Blower Compressor:", TFT.GREEN, sysfont, 1)
        utime.sleep(0.3)
        tft.text((0,tn*5), "2)Vane-Type Compressor :", TFT.GREEN, sysfont, 1)
        utime.sleep(0.3)
        tft.text((0,tn*7), "3)Centrifugal Compressor :", TFT.GREEN, sysfont, 1)
        utime.sleep(0.3)
        tft.text((0,tn*9), "4)Axial Flow Compressor :", TFT.GREEN, sysfont, 1)
        utime.sleep(0.3)
        ct = k.Read(tn*16,11*tn)
        if(ct == 1):
            engine = RTBC()
            tft.fill(TFT.BLACK )
            tft.text((4*tn, 2*tn), "You  have", TFT.GREEN, sysfont, 2)
            tft.text((4*tn, 6*tn), "choosen", TFT.GREEN, sysfont, 2)
            tft.text((2*tn, 9*tn), "Root Blower", TFT.GREEN, sysfont, 2)
            tft.text((3*tn, 12*tn), "Compressor", TFT.GREEN, sysfont, 2)
            utime.sleep(1)
            tft.fill(TFT.BLACK )
            engine.stage1()
            tft.fill(TFT.BLACK )
            engine.stage2()
            tft.fill(TFT.BLACK )
            return engine
        elif(ct == 2):
            engine = VTC()
            tft.fill(TFT.BLACK )
            tft.fill(TFT.BLACK )
            tft.text((4*tn, 2*tn), "You  have", TFT.GREEN, sysfont, 2)
            tft.text((4*tn, 6*tn), "choosen", TFT.GREEN, sysfont, 2)
            tft.text((3*tn, 9*tn), "Vane-Type", TFT.GREEN, sysfont, 2)
            tft.text((3*tn, 12*tn), "Compressor", TFT.GREEN, sysfont, 2)
            utime.sleep(1)
            tft.fill(TFT.BLACK )
            engine.stage1()
            tft.fill(TFT.BLACK )
            engine.stage2()
            tft.fill(TFT.BLACK )
            engine.stage3()
            tft.fill(TFT.BLACK )
            return engine
        elif(ct == 3):
            engine = CFC()
            engine.img = 'cf.bmp'
            tft.fill(TFT.BLACK )
            tft.text((4*tn, 2*tn), "You  have", TFT.GREEN, sysfont, 2)
            tft.text((4*tn, 6*tn), "choosen", TFT.GREEN, sysfont, 2)
            tft.text((3*tn, 9*tn), "Centrifugal", TFT.GREEN, sysfont, 2)
            tft.text((3*tn, 12*tn), "Compressor", TFT.GREEN, sysfont, 2)
            utime.sleep(1)
            tft.fill(TFT.BLACK )
            engine.stage1()
            tft.fill(TFT.BLACK )
            engine.stage2()
            tft.fill(TFT.BLACK )
            return engine
        elif(ct == 4):
            engine = CFC()
            engine.img = 'af.bmp'
            tft.fill(TFT.BLACK )
            tft.text((4*tn, 2*tn), "You  have", TFT.GREEN, sysfont, 2)
            tft.text((4*tn, 6*tn), "choosen", TFT.GREEN, sysfont, 2)
            tft.text((3*tn, 9*tn), "Axial Flow", TFT.GREEN, sysfont, 2)
            tft.text((3*tn, 12*tn), "Compressor", TFT.GREEN, sysfont, 2)
            tft.fill(TFT.BLACK )
            engine.stage1()
            tft.fill(TFT.BLACK )
            engine.stage2()
            tft.fill(TFT.BLACK )
            return engine
        else:
            tft.fill(TFT.BLACK )
            tft.text((3*tn, 2*tn),"INCORRECT ", TFT.GREEN, sysfont, 2)
            tft.text((3*tn, 6*tn),"  INPUT ", TFT.GREEN, sysfont, 2)
            tft.text((3*tn, 9*tn),"TRY AGAIN", TFT.GREEN, sysfont, 2)
            utime.sleep(1)
            tft.fill(TFT.BLACK )
            compressor() 
        
    else:
        tft.fill(TFT.BLACK )
        tft.text((3*tn, 2*tn),"INCORRECT ", TFT.GREEN, sysfont, 2)
        tft.text((3*tn, 6*tn),"  INPUT ", TFT.GREEN, sysfont, 2)
        tft.text((3*tn, 9*tn),"TRY AGAIN", TFT.GREEN, sysfont, 2)
        utime.sleep(1)
        tft.fill(TFT.BLACK )
        compressor()

            
def test_main():
    tft.fill(TFT.BLACK )
    tft.rotation(1)
    tft.text((2*tn, 4*tn), "MECHANICAL", TFT.GREEN, sysfont, 2)
    utime.sleep(0.5)
    tft.text((5*tn, 8*tn), "CALCULATOR", TFT.GREEN, sysfont, 2)
    utime.sleep(0.3)
    press()
    test = False
    while True:
        key = k.Keypad(k.col_list,k.row_list)
        if(key != None):
            tft.fill(TFT.BLACK )
            start()
            c= 2*tn
            d=104
            utime.sleep(0.3)
            opt = k.Read(10*tn,d)
            utime.sleep(0.5)
            tft.fill(TFT.BLACK )
            if(opt == 1):
                engine = Ic()
                tft.text((4*tn, 2*tn), "You  have", TFT.GREEN, sysfont, 2)
                tft.text((4*tn, 6*tn), "choosen", TFT.GREEN, sysfont, 2)
                tft.text((4*tn, 11*tn), "IC Engine", TFT.GREEN, sysfont, 2)
                utime.sleep(1)
                tft.fill(TFT.BLACK )
                engine.stage1()
                tft.fill(TFT.BLACK )
                engine.stage2()
                tft.fill(TFT.BLACK )
                engine.stage3()
                tft.fill(TFT.BLACK )
                test = engine.calculate()
            elif(opt == 2):
                engine = GT()
                tft.text((4*tn, 2*tn), "You  have", TFT.GREEN, sysfont, 2)
                tft.text((4*tn, 6*tn), "choosen", TFT.GREEN, sysfont, 2)
                tft.text((0, 11*tn), "Turbine Engine", TFT.GREEN, sysfont, 2)
                utime.sleep(1)
                tft.fill(TFT.BLACK )
                engine.stage1()
                tft.fill(TFT.BLACK )
                engine.stage2()
                tft.fill(TFT.BLACK )
                engine.stage3()
                tft.fill(TFT.BLACK )
                test = engine.calculate()
            elif(opt == 3):
                engine = JT()
                tft.text((4*tn, 2*tn), "You  have", TFT.GREEN, sysfont, 2)
                tft.text((5*tn, 6*tn), "choosen", TFT.GREEN, sysfont, 2)
                tft.text((3*tn, 11*tn), "Jet Engine", TFT.GREEN, sysfont, 2)
                utime.sleep(1)
                tft.fill(TFT.BLACK )
                engine.stage1()
                tft.fill(TFT.BLACK )
                engine.stage2()
                tft.fill(TFT.BLACK )
                test = engine.calculate()
            elif(opt == 4):
                tft.text((4*tn, 2*tn), "You  have", TFT.GREEN, sysfont, 2)
                tft.text((4*tn, 6*tn), "choosen", TFT.GREEN, sysfont, 2)
                tft.text((3*tn, 11*tn), "Compressors", TFT.GREEN, sysfont, 2)
                utime.sleep(1)
                engine = compressor()
                test = engine.calculate()
            elif(opt == 5):
                engine = R()
                tft.text((4*tn, 2*tn), "You  have", TFT.GREEN, sysfont, 2)
                tft.text((4*tn, 6*tn), "choosen", TFT.GREEN, sysfont, 2)
                tft.text((tn, 11*tn), "Rocket Engine", TFT.GREEN, sysfont, 2)
                utime.sleep(1)
                tft.fill(TFT.BLACK )
                engine.stage1()
                tft.fill(TFT.BLACK )
                engine.stage2()
                tft.fill(TFT.BLACK )
                test = engine.calculate()
            elif(opt == 6):
                engine = R()
                tft.text((4*tn, 2*tn), "You  have", TFT.GREEN, sysfont, 2)
                tft.text((4*tn, 6*tn), "choosen", TFT.GREEN, sysfont, 2)
                tft.text((5*tn, 10*tn), " Unit", TFT.GREEN, sysfont, 2)
                tft.text((3*tn, 13*tn), "Conversion", TFT.GREEN, sysfont, 2)
                utime.sleep(1)
                tft.fill(TFT.BLACK)
                convertor()
                utime.sleep(0.3)
                opt = int(k.Read(88,32))
                utime.sleep(0.5)
                tft.fill(TFT.BLACK )
                tft.text((tn, 0), "Enter the value :", TFT.GREEN, sysfont, 1)
                utime.sleep(0.3)
                val = int(k.Read(88,16))
                utime.sleep(0.5)
                tft.fill(TFT.BLACK )
                c=tn
                d=0
                tft.text((c, d), "Choose the units", TFT.GREEN, sysfont, 1)
                utime.sleep(0.3)
                d+= 2*tn
                for i in range(0,len(unit[opt-1])):
                    s = str(i+1)+") "+ unit[opt-1][i]
                    tft.text((c,d),s, TFT.GREEN, sysfont, 1)
                    d += 2*tn
                utime.sleep(0.3)
                u = int(k.Read(12*tn,12*tn))
                utime.sleep(0.5)
                tft.fill(TFT.BLACK )
                c=tn
                d=0
                tft.text((c, d), "the values are:", TFT.GREEN, sysfont, 1)
                utime.sleep(0.3)
                d+= 2*tn
                if(opt == 9):
                    if(u == 2):
                      val = val-273.15
                    if(u == 3):
                        val = (val-32)/1.8
                    t = [val,val+273.15,(val*1.8)+32]
                    for i in range(0,3):
                        s = str(i+1)+") "+str(t[i])+ " " +unit[opt-1][i]
                        tft.text((c,d),s, TFT.GREEN, sysfont, 1)
                        d += 2*tn
                
                else:
                    val = val/factor[opt-1][u-1]
                    for i in range(0,len(unit[opt-1])):
                        s = str(i+1)+") "+str(val*factor[opt-1][i])+ " " +unit[opt-1][i]
                        tft.text((c,d),s, TFT.GREEN, sysfont, 1)
                        d += 2*tn
            elif(opt == 6054):
                engine = IC2()
                tft.text((4*tn, 2*tn), "You  have", TFT.GREEN, sysfont, 2)
                tft.text((4*tn, 6*tn), "choosen", TFT.GREEN, sysfont, 2)
                tft.text((4*tn, 11*tn), "IC Engine", TFT.GREEN, sysfont, 2)
                utime.sleep(1)
                index = 0
#                 print("haha") 
                while True:
                    if(index == 0):
                        tft.fill(TFT.BLACK )
                        engine.stage1()
                    elif index == 1:
                        tft.fill(TFT.BLACK )
                        engine.stage2()
                    elif index == 2:
                        tft.fill(TFT.BLACK )
                        engine.stage3()
                    elif index == 3:
                        tft.fill(TFT.BLACK )
                        tft.text((3*tn, 2*tn), " Do you ", TFT.GREEN, sysfont, 2)
                        tft.text((4*tn, 6*tn), "want to", TFT.GREEN, sysfont, 2)
                        tft.text((4*tn, 10*tn), "Calculate ?", TFT.GREEN, sysfont, 2,nowrap=True)
                        ans = k.Read(16*tn,8*tn)
                        if(ans == True):
                            engine.calculate()
                            index = 0
                            while True:
                                if(index == 0):
                                    tft.fill(TFT.BLACK )
                                    c=0
                                    d=tn
                                    for i in range(0,8):
                                        s =  str(i+1)+")"+str(engine.s[(i)])+" :"
                                        tft.text((c,d),s, TFT.GREEN, sysfont, 1)
                                        s = str(engine.sv[i])
                                        tft.text((120,d),s, TFT.GREEN, sysfont, 1)
                                        d += 1.8*tn
                                elif index == 1:
                                    tft.fill(TFT.BLACK )
                                    c=0
                                    d=tn
                                    for i in range(8,16):
                                        if(i>=len(engine.s)):
                                            break
                                        s =  str(i+1)+")"+str(engine.s[(i)])+" :"
                                        tft.text((c,d),s, TFT.GREEN, sysfont, 1)
                                        s = str(engine.sv[i])
                                        tft.text((120,d),s, TFT.GREEN, sysfont, 1)
                                        d += 1.8*tn
                                elif index == 2:
                                    tft.fill(TFT.BLACK )
                                    c=0
                                    d=tn
                                    for i in range(16,24):
                                        if(i>=len(engine.s)):
                                            break
                                        s =  str(i+1)+")"+str(engine.s[(i)])+" :"
                                        tft.text((c,d),s, TFT.GREEN, sysfont, 1)
                                        s = str(engine.sv[i])
                                        tft.text((120,d),s, TFT.GREEN, sysfont, 1)
                                        d += 1.8*tn
                                elif index == 3:
                                    tft.fill(TFT.BLACK )
                                    p = P()
                                    p.selectPhoto(engine.img)
                                elif index == 4:
                                    tft.fill(TFT.BLACK )
                                    g = G()
                                    g.graph(engine.graph1,engine.graph2,engine.graph)
                                elif index == 5:
                                    tft.fill(TFT.BLACK )
                                    tft.text((3*tn, 2*tn), " Do you ", TFT.GREEN, sysfont, 2)
                                    tft.text((4*tn, 6*tn), "want to", TFT.GREEN, sysfont, 2)
                                    tft.text((5*tn, 10*tn), "Leave ?", TFT.GREEN, sysfont, 2)
                                    ans = k.Read(16*tn,8*tn)
                                    if(ans == True):
                                        del engine
                                        del p
                                        del g
                                        utime.sleep(0.5)
                                        test_main()
                                    else:
                                        index = 4
                                ch = k.Read(500,500)
                                if(ch):
                                    index = index+1
                                elif(index > 0):
                                    index = index -1
                        else:
                            index = 1
                            continue
                    utime.sleep(0.5)
                    ch = k.Read(130,12,z=True)
                    if(ch == 'c'):
                        index += 1
                    elif(0 < ch and ch <= len(engine.s)):
                        ch = int(ch)
                        tft.fill(TFT.BLACK )
                        s = "Enter value of "+str(engine.s[(ch)-1])+" :"
                        tft.text((0,8),s, TFT.GREEN, sysfont, 1)
                        utime.sleep(0.5)
                        v = k.Read(100,32)
                
                        if(engine.unit[int(ch)-1] != []):
                            tft.fill(TFT.BLACK)
                            c=0
                            d=tn
                            for i in range(0,len(engine.unit[(ch)-1])):
                                s =  str(i+1)+")  "+str(engine.unit[(ch)-1][i])+" :"
                                tft.text((c,d),s, TFT.GREEN, sysfont, 1)
                                d += 1.5*tn
                            utime.sleep(0.5)
                            u = k.Read(100,32)
                            if(engine.s[(ch)-1] == "Diameter" or engine.s[(ch)-1] == "Piston Diameter" or engine.s[(ch)-1] == "Stroke Length" or engine.s[(ch)-1] == "Length"):
                                v = C.diameter(v,u)
                            elif(engine.s[(ch)-1] == "Mean Pressure" or engine.s[(ch)-1] == "pressure (P1)" or engine.s[(ch)-1] == "pressure (P2)"
                                 or engine.s[(ch)-1] == "pressure (P3)"or engine.s[(ch)-1] == "pressure (P4)"):
                                v = C.pressure(v,u)
                            elif(engine.s[(ch)-1] == "mass of air(ma)" or engine.s[(ch)-1] == "mass of fuel(mf)"):
                                v = C.hmass(v,u)
                            elif(engine.s[(ch)-1] == "mass of air(ma)" or engine.s[(ch)-1] == "mass of fuel(mf)" and engine.type == "JTE"):
                                v = C.mass(v,u)
                            elif(engine.s[(ch)-1] == "Tempurature T1" or engine.s[(ch)-1] == "Tempurature T2" or engine.s[(ch)-1] == "pressure (P2)"
                                 or engine.s[(ch)-1] == "Tempurature T3"or engine.s[(ch)-1] == "Tempurature T4"):
                                v = C.tempurature(v,u)
                        engine.val[ch-1] = v
                    else:
                        index -= 1
                        
            else:
                tft.text((4*tn, 2*tn), "You  have", TFT.GREEN, sysfont, 2)
                tft.text((4*tn, 6*tn), "choosen", TFT.GREEN, sysfont, 2)
                tft.text((2*tn, 9*tn), "Wrong Option", TFT.GREEN, sysfont, 2)
                press()
                continue
            if(test):
                index = 0
                while True:
                    if(index == 0):
                        tft.fill(TFT.BLACK )
                        engine.table()
                    elif index == 1:
                        tft.fill(TFT.BLACK )
                        p = P()
                        p.selectPhoto(engine.img)
                    elif index == 2:
                        tft.fill(TFT.BLACK )
                        g = G()
                        g.graph(engine.graph1,engine.graph2,engine.graph)
                    elif index == 3:
                        tft.fill(TFT.BLACK )
                        tft.text((3*tn, 2*tn), " Do you ", TFT.GREEN, sysfont, 2)
                        tft.text((4*tn, 6*tn), "want to", TFT.GREEN, sysfont, 2)
                        tft.text((5*tn, 10*tn), "Leave ?", TFT.GREEN, sysfont, 2)
                        ans = k.Read(16*tn,8*tn)
                        if(ans == True):
                            del engine
                            del p
                            del g
                            utime.sleep(0.5)
                            test_main()
                        else:
                            index = 2
                            continue
                    utime.sleep(0.5)
                    ch = k.Read(500,500)
                    if(ch):
                        index = index+1
                    elif(index > 0):
                        index = index -1
test_main()

