"""This is the the exoplanet module that contains the `Planet` class that accepts a string `name` and measurements for mass and radius as `mass` and `radius`; also calculates the density and sets it as a third attribute."""

from measure import *
import numpy as np
class Planet(Measurement):
    """The main Planet class.
    Planet(name, mass, radius)
    
    Represents a planet from exoplanet_eu_catalog.csv
    
    Parameters
    ----------
    name : string; name of a planet
    mass : float; mass of a planet
    radius : float; radius of a planet
    
    Attributes
    ----------
    name : string; name of a planet
    mass : float; mass of a planet
    radius : float; radius of a planet
    density : density of a planet
        All float attributes are converted to MKS system of units.
    
    """
    def __init__(self, name, mass, radius):
        """(a)Planet objects take three arguments but possess four attributes. The last attribute `density` is calculated using error of measurement arithmetic from `measure.py` module."""
        self.name = name
        self.mass = mass
        self.radius = radius
        self.density = mass / (4/3 * np.pi * radius**3)
    
    def __str__(self):
        """(b)Prints the Planet object in the form "`name` `density`", where density is an object of Measurement"""
        return '%s %f \u00B1 %f' %(self.name, self.density.val, self.density.unc)
        
    def __lt__(self, other):
        """(c)Planet objects are compared using their densities. When comparing densities, the error of the measurement is not taken into account."""
        return True if (self.density.val < other.density.val) else False
    
    def __gt__(self, other):
        """(c)Planet objects are compared using their densities. When comparing densities, the error of the measurement is not taken into account."""
        return True if (self.density.val > other.density.val) else False
        
    def input():
        """(d)Reads the data from 'exoplanet_eu_catalog.csv' and assigns the corresponding data to the correct attribute of object Planet. If data is sufficuent to fill all four attributes, converts the values from 'exoplanet_eu_catalog.csv' from Jupiter units to MKS units; assigns the data to correct attributes and appends that Planet object to a list."""
        Planet_list = []
        mass = Measurement()
        radius = Measurement()
        Rjup = Measurement(val = 7.1492e10) # Jovian radius in m has no uncertainty by definition
        Mjup = Measurement(val = 1.89813e27, unc = 0.00019e27) # Jovian mass in kg with uncertainty
        rawdata = np.genfromtxt('exoplanet_eu_catalog.csv', delimiter=',', missing_values={'','nan','inf'}, filling_values=np.nan, usemask=True, usecols=(2,3,4,8,9,10), encoding=None)
        names = np.genfromtxt('exoplanet_eu_catalog.csv', delimiter=',', dtype=None, missing_values={'','nan','inf'}, filling_values='', usemask=True, usecols=(0), encoding=None)
        # Inputting names separately for datatype consistency. If floats are imported with the strings, genfromtxt returns a list of tuples rather then a 2-dim. ndarray, which are unslicible
        # Validaing the data:
        for i in range(rawdata.shape[0]): # Removing rows with missing values. I couldn't figure out how to do it without loop in my case.
            if (any(rawdata.mask[i])):
                names = np.delete(names, i, 0)
        # Processing the data:
                rawdata = np.delete(rawdata, i, 0)
        rawdata[:, 0] = rawdata[:, 0] * Mjup
        rawdata[:, 1] = (rawdata[:, 1] + rawdata[:, 2]) / 2
        rawdata = np.delete(rawdata, 2, 1)
        mass.val = rawdata[:, 0]
        mass.unc = rawdata[:, 1]
        rawdata[:, 3] = rawdata[:, 3] * Rjup
        rawdata[:, 4] = (rawdata[:, 4] + rawdata[:, 5]) / 2
        rawdata = np.delete(rawdata, 5, 1)
        radius.val = rawdata[:, 3]
        radius.unc = rawdata[:, 4]
        # Assigning the data:
        for i in range(rawdata.shape[0]):
            Planet_list.append(Planet(names[i], mass[i], radius[i]))
        # Also couldn't think of a more elegant solution
