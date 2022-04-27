#!/usr/bin/env python3
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.tri as mtri
from mcint import *

plt.ion()
print("====Problem 1 ====")
def piston(V, P0 = 1, V0 = 1, T0 = 300, gamma = 1.4):
#gamma, the adiabatic constant, defaluts to the value for dry air. P0 = 1 atm., V0 = 1 liter, T0 = 300K 
    const = (P0 * V0) / T0
    P = np.array(const / V**gamma)
    T = (P * V) / const
    Fin = np.array((P, V, T))
    Fin.shape = (len(V), 3)
    return Fin
    
V = np.array((1., 0.5, 1.5, 0.1))
fig = plt.figure()
ax = fig.gca(projection='3d')
ax = fig.add_subplot(111, projection='3d')
args = piston(V)                    # X,Y,Z values for the surface
tri = mtri.Triangulation(args[:, 0], args[:, 1])
surf = ax.plot_trisurf(args[:, 0], args[:, 1], args[:, 2], triangles=tri.triangles, cmap=plt.cm.plasma, linewidth=0.5, antialiased=True)
plt.savefig("hw11_oleksiy_graphic_1")
print("The graph is being displayed\nThe graph was saved as hw11_oleksiy_graphic_1")

print("\n====Problem 2 ====")
print("Calling function test_mcint. Docs availible.\nWarning!!! One of the tests uses 10**8 sample points. More explanation in docs.\nAll other tests use 10**6 sample points.")
print("\nWarning! Computation intensive part ahead!\nPress Enter to continue (ctrl+c Enter to exit).")
input()
print("Running sanity checks for Monte Carlo numerical integrator...")
test_mcint()

print("\n====Problem 3 ====")
print("The Monte Carlo numerical integrator is in mcint.py module. Docs for mcint functon are availible.")

print("\n====Problem 4 ====")
print("Warning! Computation intensive part ahead! Number of sample points is 10**7.\nPress Enter to continue (ctrl+c Enter to exit).")
input()
print("Integrating np.sin(x) on [0, 2*pi)")
print(mcint(0, 2*np.pi, np.sin, N = 10**7))
print("\nShowing that integral of cos(x)dx on 0 to x is equall to sin(x)")
print("     Monte Carlo       numpy.sin(x)")
print("x = pi/4:\n {} {}" .format(mcint(0, np.pi/4, np.cos, N = 10**7), np.sin(np.pi/4)))
print("x = pi/2:\n {} {}" .format(mcint(0, np.pi/2, np.cos, N = 10**7), np.sin(np.pi/2)))
print("x = 3*pi/4:\n {} {}" .format(mcint(0, 3*np.pi/4, np.cos, N = 10**7), np.sin(3*np.pi/4)))
print("x = pi:\n {} {}" .format(mcint(0, np.pi, np.cos, N = 10**7), np.sin(np.pi)))
print("x = 5*pi/4:\n {} {}" .format(mcint(0, 5*np.pi/4, np.cos, N = 10**7), np.sin(5*np.pi/4)))
print("x = 3*pi/2:\n {} {}" .format(mcint(0, 3*np.pi/2, np.cos, N = 10**7), np.sin(3*np.pi/2)))
print("x = 7*pi/4:\n {} {}" .format(mcint(0, 7*np.pi/4, np.cos, N = 10**7), np.sin(7*np.pi/4)))
print("x = 2*pi:\n {} {}" .format(mcint(0, 2*np.pi, np.cos, N = 10**7), np.sin(2*np.pi)))

