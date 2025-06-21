from machine import SPI,Pin
import utime
import math

def diameter(D,dunit):
    if (dunit == 1.0):
        D = D/100
    elif (dunit == 2.0):
        D = D/1000
    elif (dunit == 3.0):
        D = D
    return D

def pressure(P, punit):
    if (punit == 1.0):
        P = P * 100
    elif (punit == 2.0):
        P = P
    elif (punit == 3.0):
        P = P/1000
    return P

def tempurature(T, tunit):
    if (tunit == 1.0):
        T = ((T) + 273.15)
    elif (tunit == 2.0):
        T = T + 0.00
    elif (tunit == 3.0):
        T = (T - 32) * (5 / 9) + 273.15
    return T

def mass(M, munit):
    if (munit == 1.0):
        M = M
    elif (munit == 2.0):
        M = M / 60
    return M


def hmass(M, munit):
    if (munit == 1.0):
        M = M * 3600
    elif (munit == 2.0):
        M = M
    return M

