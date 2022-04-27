import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import airship


#(2) Circles
def xycircle (center, rad, res=100):
    """
    This is a helper function that returns the coordinates of a circle with the given center and radius that lies parallel to the xy-plane.
    
    Parameters
    ----------
    center : numpy.ndarray
        An array-like object of the Cartesian (z, y, x) coordinates of the center of the cicle with shape (3,)
    rad : float, int
        A numerical value for the radius of the circle.
    res : int, optional
        The resolution of the circle. How many points you want the function to return. 
    
    Returns
    -------
    numpy.ndarray : A 2D array of shape (3, res) that has the coordinates of the circle IN! z,y,x order.
    
    Examples
    -------
    >>> xycircle((0,0,0), 5, res=10)
    array([[ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
         0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
         0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
         0.00000000e+00],
       [ 0.00000000e+00,  3.21393805e+00,  4.92403877e+00,
         4.33012702e+00,  1.71010072e+00, -1.71010072e+00,
        -4.33012702e+00, -4.92403877e+00, -3.21393805e+00,
        -1.22464680e-15],
       [ 5.00000000e+00,  3.83022222e+00,  8.68240888e-01,
        -2.50000000e+00, -4.69846310e+00, -4.69846310e+00,
        -2.50000000e+00,  8.68240888e-01,  3.83022222e+00,
         5.00000000e+00]])

    """
    theta = np.linspace(0, 2*np.pi, res)
    zcir = np.full(res, center[0])
    ycir = rad * np.sin(theta) + center[1]
    xcir = rad * np.cos(theta) + center[2]
    coords = np.ndarray((3, res))
    coords[0,:] = zcir
    coords[1,:] = ycir
    coords[2,:] = xcir
    return coords

#(3) Setup
def plotsetup(pos_target, ax, rad_cannon = 8, radii_target=(5,12,20)):
    """
    This function sets up the plot for later functions that graph Furby's trajectory. It draws a circle that indicates the cannon, and three circles around the target.
    
    Parameters
    ----------
    pos_target : array-like
        An array-like object of the Cylindrical (z, φ, ρ) coordinates that gives the position of the target. Has a shape (3,)
    ax : the axes object for 3D graphing
    rad_cannon : float, int, optional
        The radius of the circle to draw around the cannon.
    radii_target : array-like, optional
        An array-like object of the radii of the three circles to draw around the target.
    
    Returns
    -------
    Draws objects on the 3D plot.
    
    Examples
    --------
    >>> plotsetup((-50., 1.234, 150), ax)
    
    """
    lim = max(abs(pos_target[0]), abs(pos_target[2]))
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)    
    cannon_cir = xycircle ((0,0,0), rad_cannon)
    ax.plot(cannon_cir[2,:], cannon_cir[1,:], cannon_cir[0,:], label = "cannon circle")
    pos_target_rect = (pos_target[0], pos_target[2] * np.sin(pos_target[1]), \
                                      pos_target[2] * np.cos(pos_target[1]))
    target_cir3 = xycircle(pos_target_rect, radii_target[0])
    target_cir7 = xycircle(pos_target_rect, radii_target[1])
    target_cir15= xycircle(pos_target_rect, radii_target[2])
    ax.plot(target_cir3 [2,:], target_cir3 [1,:], target_cir3 [0,:], label = "target circle 3")
    ax.plot(target_cir7 [2,:], target_cir7 [1,:], target_cir7 [0,:], label = "target circle 7")
    ax.plot(target_cir15[2,:], target_cir15[1,:], target_cir15[0,:], label = "target circle 15")

#(4) Trajectory
def calctrajectory(cannon, v_wind=(0,0,0), time=10, steps=1000, k=.003, pos_target = (-50., 1.234, 150)):
    """
    This function calculates the trajectory of a Furby via numerical integrtion taking wind into account.
    
    Parameters
    ----------
    cannon : airship.Cannon instance
        See airship.py for more explanation.
    v_wind : array-like, optional
        An array-like object of the Cartesian (z, y, x) coordinates that define the velocity of wind. Has shape (3,). The default value for wind velocity is zero.
    time : float, int, optional
        Together with `steps` defines the time interval for numerical integration.
    steps : float, int, optional
        Together with `time` defines the time interval for numerical integration.
    k : float, optional
        The proportionality constant that combines several physical constants for the formulas used here.
    pos_target : array-like, optional
        An array-like object of the Cartesian (z, y, x) coordinates that define the target position. Has shape (3,). Has to be here because of the dynamic approach that I took to this problem. If you want to change your target position, make sure you change this variable!
    
    Returns
    -------
    numpy.ndarray : A numpy array of shape (n, 3) that contains points that define Furby's trajectory. `n` gives the number of points in trajectory before Furby falls under the z component of the target's position.
    
    Examples
    --------
    >>> calctrajectory(cannon, (0,0,0), time = 1, steps = 10, k=.003, pos_target=(-50., 1.234, 150))
    array([[  0.        ,   0.        ,   0.        ],
           [  1.36521356,   0.        ,   1.41421356],
           [  2.62818448,   0.        ,   2.82418448],
           [  3.78509848,   0.        ,   4.22581449],
           ...,
           [-41.05804512,   0.        ,  59.52295152],
           [-44.01771938,   0.        ,  60.60599247],
           [-47.04865002,   0.        ,  61.67891056],
           [-50.14959358,   0.        ,  62.74158902]])

    """
    g = np.array((-9.8, 0, 0)) #m/s^2
    v_wind = np.asarray(v_wind)
    v_furby = np.ndarray(3)
    v_furby[0] = cannon.vel * np.cos(cannon.theta)
    v_furby[1] = cannon.vel * np.sin(cannon.theta)*np.sin(cannon.phi)
    v_furby[2] = cannon.vel * np.sin(cannon.theta)*np.cos(cannon.phi)
    #the coordinates of Furby's velocity are also in order z,y,x
    delta_t = time / steps
    
    #defining initial conditions according to project.pdf
    r = np.ndarray((0, 3))
    r = np.append(r, [[0.,0.,0.]], axis = 0)
    #initial v_furby is already assigned above
    a = np.array(g)
    v_af = v_wind - v_furby                              #calcualte instant velocity reltive to air
    
    #defining helper functions for integration
    rvec = lambda v, a : r[-1, :] + v * delta_t + 1/2 * a * delta_t**2 #calculate instant position
    velupdt  = lambda : v_furby + a * delta_t                          #update instant velocity
    accupdt  = lambda a : g + k * (np.linalg.norm(v_af)) * v_af        #update instant acceleration
    #the integration loop:
    while (r[-1, 0] >= pos_target[0]): # checks if last z coordinate of furby is below the target
        r = np.append(r, [rvec(v_furby, a)], axis = 0)
        v_furby = velupdt()
        a = accupdt(a)
        v_af = v_wind - v_furby
    return r

#(5) Landing
def landingpos(traj , z_target=-50):
    """
    This function takes the array from calctrajectory() and looks for the landing position of the Furby in it. Because of the dynamic approach, the landing position it's just the point in the trajectory array.
    
    Parameters
    ----------
    traj : numpy.ndarray
        An array-like object of the Cartesian (z, y, x) coordinates of points that describe Furby's trajectory. Has shape (3,).
    z_target : float, int
        The z-component of the target position. Because of the dynamic approach doesn't need to be here.
    
    Returns
    -------
    tuple : A tuple of coordinates in Polar (θ, ρ) that define Furby's landing position.
    
    Examples
    --------
    >>> canon = airship.Cannon(1337)
    >>> landingpos(calctrajectory(cannon, (0,0,0)))
    (0.0, 62.720727114244134)
        
    """
    phi_l = np.arctan2(traj[-1, 1], traj[-1, 2])
    ro = np.linalg.norm((traj[-1, 1], traj[-1, 2]))
    return phi_l, ro

#(6) PID iteration
def piditer(error, i, dt, kp, ki, kd):
    """
    Takes an array of errors from each time step, a time step index, and PID k values and returns a PID output value. A helper function for pid().
    
    Parameters
    ----------
    error : numpy.ndarray
        A one-dimensional array of errors.
    i : int
        An iteration index.
    dt : float
        A time step length
    kp : float
        PID constant for proportional term.
    ki : float
        PID constant for integral term.
    kd : float
        PID constant for derivative term.
    
    Returns
    -------
    float : The PID output value to be fed into pid().
    
    Examples
    --------
    >>> piditer(np.arange(10), 5, 1, 1.5, 1.5, 1.5)
    31.5
    
    """
    Pi = kp * error[i]
    Ii = ki * dt * sum(error[ :i+1])
    Di = kd * [(error[i] - error[i-1]) / dt if (i > 0) else 0][0]
    u_i = Pi + Ii + Di
    return u_i
    
#(7) PID controller
def pid(cannon, ax, pos_target, v_wind = np.zeros(3), steps = 50, \
                k_phi = (1.7 ,1.5 , .00125), k_vel = (.25, 1.5, .005)):
    """
    This is the main PID controller function. Calculates and plots the trajectory of the Furby. Calculates the error in angle and distance to be used in piditer(). Calculates the power signal to be sent to the cannon motors and adjusts the cannon.
    
    Parameters
    ----------
    cannon : airship.Cannon instance
        See airship.py for more explanation.
    ax : the axes object for 3D graphing
    pos_target : array-like
        An array-like object of the Cylindrical (z, φ, ρ) coordinates that gives the position of the target. Has a shape (3,)
    v_wind : array-like, optional
        An array-like object of the Cartesian (z, y, x) coordinates that define the velocity of wind. Has shape (3,). The default value for wind velocity is zero.
    steps : int
        The number of trials for the PID controller. This is the number of shots as well.
    k_phi : tuple of floats, optional
        The PID constants of angle for piditer(). The default value is (1.7 ,1.5 , .00125).
    k_vel : tuple of floats, optional
        The PID constants of velocity for piditer(). The default value is (.25, 1.5, .005).
    
    Returns
    -------
    error, pow_sig : numpy.ndarray
        A tuple of numpy arrays of errors and power signals for the motor.
    Draws an object on the 3D plot.
    Adjusts the cannon.
    
    Examples
    --------
    >>> canon = airship.Cannon(1337)
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot (111, projection='3d')
    >>> pid(cannon, ax, pos_target)
    (array([[ 1.23400000e+00, -8.91713604e-01,  5.37232886e-01,
              ..., 
             -9.29558326e-03, -8.86939263e-03, -8.50340962e-03],
            [ 8.72792729e+01,  7.52975346e+01,  6.24360058e+01,
              ..., 
             -4.17802249e+00, -4.01907801e+00, -3.61032602e+00 ]]), 
     array([[ 2.19035000e+00, -1.54338449e+00,  1.01498351e+00,
              ..., 
             -6.72802623e-02, -6.72200437e-02, -6.72371335e-02],
            [ 2.83657637e+01,  2.98194704e+01,  3.11988096e+01,
              ..., 
              1.06842840e-01, -1.44138124e-01, -2.87743827e-01]]))

    """
    error = np.empty((2, steps))
    #first row is for the azimuthal error of landing angle, second - distance error
    pow_sig = np.empty((2, steps))
    #first row is for the power for azimuthal aiming angle motor, second - velocity changing motor
    
    for i in range(steps):
        #calculating and plotting trajectory
        traj = calctrajectory(cannon, v_wind)
        ax.plot(traj[:, 2], traj[:, 1], traj[:, 0], label = "Furby's trajectory", 
                                                color = plt.cm.viridis(i/steps))
        #calculating the error and saving it in error[:, i]
        err_phi_l, err_ro = np.array([pos_target[1], pos_target[2]]) - np.array(landingpos(traj))
        err_phi_l = [(err_phi_l - 2*np.pi) if (err_phi_l > np.pi) \
                else (err_phi_l + 2*np.pi) if (err_phi_l < -np.pi) else (err_phi_l)][0]
        error[:, i] = (err_phi_l, err_ro)
    
        #calculating the power to supply to the motors
        phipower = piditer(error[0, :], i, cannon.adjt, *k_phi) #Careful! This has a tuple argument!
        velpower = piditer(error[1, :], i, cannon.adjt, *k_vel) #Careful! This has a tuple argument!
        pow_sig[:, i] = (phipower, velpower)
    
        #adjusting the cannon
        cannon.adjust(phipower, velpower)
    return error, pow_sig


