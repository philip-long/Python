# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 10:09:21 2015

@author: philip
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def arduinomap( x,  in_min,  in_max,  out_min,  out_max):
  return (((x - in_min) * (out_max - out_min) ) / (in_max - in_min)) + out_min
  
def func(x, a, b, c):
    return a*np.exp(-b*x)+c
    
def func2(x, a, b):
    return (a*((x)**b))

def main():
    Measure=np.array([0.06,0.08,0.9,0.1,0.12,0.14,0.16,0.18,0.2,0.22,0.24,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.36,0.37,0.38,0.39,0.4,0.42,0.44,0.46,0.48,0.5,0.52,0.54,0.56,0.58,0.6,0.62,0.64,0.66,0.68,0.70,0.72,0.74,0.76,0.78,0.79,0.80,0.81,0.82])
    Voltage=np.array([630,580,530,475,402,342,306,276,248,230,210,204,195,190,182,176,170,168,165,158,150,148,145,143,137,135,127,121,119,114,110,109,107,104,103,100,95,95,93,91,90,89,87,86,85,84,83,82])
    
    Voltagefromraw=arduinomap(Voltage,0,1023,0,5000)
    Estimated_distance=27.728*pow(Voltagefromraw/1000.,-1.2045)
    popt, pcov=curve_fit(func2,Voltagefromraw/1000.,Measure)
    Estimated_distance_cruvefit=func2(Voltagefromraw/1000.,*popt)
    
    
    plt.figure(1)
    plt.hold()
    # Current Law is  puntualDistance=61.573*pow(voltFromRaw/1000, -1.1068);
    plt.plot(Voltage,Measure*100,'ro',label="measured")
    plt.plot(Voltage,Estimated_distance,'b',label="using sharp law")   
    plt.plot(Voltage,Estimated_distance_cruvefit*100,'g',label="using my law")     
    legend = plt.legend(loc='upper center', shadow=True, fontsize='x-large')

    
if __name__ == '__main__': main()    