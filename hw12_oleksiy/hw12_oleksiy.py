#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
plt.ion()
print("====Problem1====")
from scipy.interpolate import interp1d
#reading the data
wavl1 = np.loadtxt("hw12_prob1_data.txt", usecols = 0)
spec1 = np.loadtxt("hw12_prob1_data.txt", usecols = 1)
wavl2 = np.loadtxt("hw12_prob1_data.txt", usecols = 2)
spec2 = np.loadtxt("hw12_prob1_data.txt", usecols = 3)
#plotting data
plt.plot(wavl1, spec1, 'bo', label = "spectrum1")
plt.plot(wavl2, spec2, 'ro', label = "spectrum2")
#making interpolation funcs
lininterp = interp1d(wavl2, spec2, fill_value = 0, bounds_error = 0)
cubinterp = interp1d(wavl2, spec2, kind = 'cubic', fill_value = 0, bounds_error = 0)
#evaluating interpolation funcs
interpx = np.linspace(wavl1[0], wavl1[-1], len(spec1))
wavl1linint = lininterp(interpx)
wavl1cubint = cubinterp(interpx)
#calculating mean abs deviation
MADlin = np.mean(abs(interpx - spec1))
MADcub = np.mean(abs(interpx - spec1))
print("Mean absolute difference for linear interpolation for wavl1:\n", MADlin)
print("Mean absolute difference for cubic  interpolation for wavl1:\n", MADcub)
#plotting interpolated data
plt.plot(interpx, wavl1linint, 'b', label = "linear interpolation")
plt.plot(interpx, wavl1cubint, 'g', label = "cubic interpolation")
plt.xlim(1.28, 1.32)
plt.ylim(40, 50)
plt.legend()
plt.savefig("hw12_prob1_graphic1.pdf")
plt.clf()

print("\n====Problem2,3====")
import scipy.optimize as spo
line = lambda p, x: p[1]*x + p[0]            #defining helper functions from 3.a p should be a 1d array
quad = lambda p, x: p[2]*x**2 + p[1]*x + p[0]#of parameters and x is an array of values.
                                             #Indicies for the values of the p array should match the
                                             #powers of x.
def normresid(p, x, y, sigma, func): # returns normalized residuals
    return (y - func(p, x)) / sigma
#reading the data
x =      np.loadtxt("hw12_prob3_data.txt", usecols = 0)
y1 =     np.loadtxt("hw12_prob3_data.txt", usecols = 1)
sigma1 = np.loadtxt("hw12_prob3_data.txt", usecols = 2)
y2 =     np.loadtxt("hw12_prob3_data.txt", usecols = 3)
sigma2 = np.loadtxt("hw12_prob3_data.txt", usecols = 4)
#plotting data
plt.errorbar(x, y1, yerr = sigma1, label = "y1 error", fmt = '.')
#fitting a line
args = (x, y1, sigma1, line)
p = (3., 0.5)
pcoef = spo.leastsq(normresid, p, args=args, full_output=True)
chisq = sum(((y1 - line(pcoef[0], x)) / sigma1)**2)
redchisq = chisq / (len(x) - 2)
linfit = line(pcoef[0], x)
plt.plot(x, linfit, label = "linear interpolation")
print("The reduced chi squared factor for a line is:\n", redchisq)
#fitting a quadratic
args = (x, y1, sigma1, quad)
p = (3., 0.5, 2)
pcoef = spo.leastsq(normresid, p, args=args, full_output=True)
chisq = sum(((y1 - quad(pcoef[0], x)) / sigma1)**2)
redchisq = chisq / (len(x) - 3)
quadfit = quad(pcoef[0], x)
plt.plot(x, quadfit, label = "quadratic interpolation")
print("The reduced chi squared factor for a quadratic is:\n", redchisq)
plt.legend()
plt.savefig("hw12_prob3_graphic1.pdf")
plt.clf()

print("\n====Problem2,4====")
#plotting the data
plt.errorbar(x, y2, yerr = sigma2, label = "y2 error", fmt = '.')
#fitting a line
args = (x, y2, sigma2, line)
p = (3., 0.5)
pcoef = spo.leastsq(normresid, p, args=args, full_output=True)
chisq = sum(((y2 - line(pcoef[0], x)) / sigma2)**2)
redchisq = chisq / (len(x) - 2)
linfit = line(pcoef[0], x)
plt.plot(x, linfit, label = "linear interpolation")
print("The reduced chi squared factor for a line is:\n", redchisq)
#fitting a quadratic
args = (x, y2, sigma2, quad)
p = (3., 0.5, 2)
pcoef = spo.leastsq(normresid, p, args=args, full_output=True)
chisq = sum(((y2 - quad(pcoef[0], x)) / sigma2)**2)
redchisq = chisq / (len(x) - 3)
quadfit = quad(pcoef[0], x)
plt.plot(x, quadfit, label = "quadratic interpolation")
print("The reduced chi squared factor for a quadratic is:\n", redchisq)
plt.legend()
plt.savefig("hw12_prob4_graphic1.pdf")
plt.clf()

