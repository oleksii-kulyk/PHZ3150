#! /usr/bin/env python3

#(1) Preliminaries
print("Importing the libraries.")
import matplotlib.pyplot as plt
from project_module_oleksiy import *
plt.ion()
print("#You can change the probem constants in the (1)Preliminary part of code.")
print("Setting the constants.")

cannon = airship.Cannon(1337)
fig = plt.figure()
ax = fig.add_subplot (111, projection='3d')
pos_target = (-50., 1.234, 150)
#This is the current position of Krakatoa in cylindrical (z, φ, ρ)
#coordinates relative to you in the airship (at the origin).
v_wind = (-1.5, -1, 2)
#This is the current wind velocity in Cartesian (z, y, x) coordinates.

#(2) Circles
print("\n#testing the xycirlce function")
print(xycircle((0,0,0), 2, 5))

#(3) Setup
print("\n#Setting up the plot")
plotsetup(pos_target, ax)
plt.savefig("project_oleksiy_part3_graphic1.pdf")
input()

#(4) Trajectory
print("\ncalctrajectory() uses a lightly different approach then described in project.pdf")
print("Making the first shot.")
traj = calctrajectory(cannon, v_wind)
ax.plot(traj[:, 2], traj[:, 1], traj[:, 0], label = "The First Shot")
plt.savefig("project_oleksiy_part4_graphic1.pdf")
input()

#(5) Landing
print('\n#testing landingpos()')
print(landingpos(calctrajectory(cannon, v_wind), pos_target[0]))

#(6) PID iteration   
print('\n#testing piditer()')
print(piditer(np.arange(10), 5, 1, 1.5, 1.5, 1.5))

#(7) PID controller
print("\nTime to shoot some Furbys")
error, pow_sig = pid(cannon, ax, pos_target, v_wind)
plt.savefig("project_oleksiy_part7_graphic1.pdf")
input()

#(8) Final Report
plt.clf()
x = np.arange(len((error[0])))
plt.plot(x, error[0], label="azimuthal error")
plt.plot(x, error[1], label="distance error")
plt.title("Errors")
plt.xlabel("# of iteration")
plt.ylabel("Error in units of measurement")
plt.legend()
plt.savefig("project_oleksiy_part8_graphic1.pdf")
input()

plt.clf()
plt.plot(x, pow_sig[0], label="power to angle motor")
plt.plot(x, pow_sig[1], label="power to speed motor")
plt.title("Power Signals")
plt.xlabel("# of iteration")
plt.ylabel("Power in units of measurement")
plt.legend()
plt.savefig("project_oleksiy_part8_graphic2.pdf")
input()

