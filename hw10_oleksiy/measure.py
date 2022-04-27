""" This is a measure.py module that contains a class Measurement that represents measurements with uncertainties. """

from math import log1p
class Measurement:
    """The main measurement class. 
    Measurement(val=0, unc=0)
    
    Represents a measurement with uncertainty
    
    Parameters
    ----------
    val : float; value of measurement.
    unc : float; uncertainty of the number.
    
    Attributes
    ----------
    val : float; value of a number with uncertainty.
    unc : float; uncertainty of the number.
    
    """
    def __init__(self, val=0, unc=0):
        """(a)Every object has two attributes assigned to it: its value `val` and uncertainty `unc`"""
        self.val = val
        self.unc = unc
        if self.unc < 0: #Checks for valid value of uncertainty
            raise ValueError('Uncertainty cannot be negative!')
    
    def __repr__(self):
        """(b)The string representation of a value with uncertainty for interactive mode"""
        return '%f \u00B1 %f' %(self.val, self.unc)
    
    def __str__(self):
        """(b)Prints the value with uncertainty"""
        return '%f \u00B1 %f' %(self.val, self.unc)
    
    def __eq__(self, other):
        """(c)Compares two values with uncertainties. Returns True if `self.val` == `other.val` and `self.unc` == `other.unc`. Otherwise returns False."""
        return True if (self.val == other.val and self.unc == other.unc) else False
        
    def __ne__(self, other):
        """(c)Defines when two measurements with uncertainties are not equal. Two measurements are not equal when either of their parts are not equal to each other."""
        return True if (self.val != other.val or self.unc != other.unc) else False    
    
    def __add__(self, other):
        """(d)Defines addition of two numbers with uncertainties. __radd__ is equivalent to __add__ so doesn't have to be defined separately."""
        summ = Measurement()
        if not isinstance(other, Measurement):
            summ.val = (self.val + other)
            summ.unc = self.unc
        else:
            summ.val = (self.val + other.val)
            summ.unc = (self.unc**2 + other.unc**2)**(1/2)            
        return summ
    
    def __sub__(self, other):
        """(d)Defines subtraction of two numbers with uncertainties. __rsub__ is equivalent to __sub__ so doesn't have to be defined separately."""
        sub = Measurement()
        if not isinstance(other, Measurement):
            sub.val = (self.val - other)
            sub.unc = self.unc
        else:
            sub.val = (self.val - other.val)
            sub.unc = (self.unc**2 + other.unc**2)**(1/2)
        return sub

    def __mul__(self, other):
        """(e)Defines multiplication of two numbers with uncertainties. __rmul__ is equivalent so doesn't have to be defined separately."""
        mul = Measurement()
        if not isinstance(other, Measurement):
            mul.val = (self.val * other)
            mul.unc = self.val * other * (self.unc / self.val)
        else:
            mul.val = self.val * other.val
            mul.unc = self.val * other.val * ( (self.unc / self.val)**2 + (other.unc / other.val)**2 )**(1/2)
        return mul
        
    def __truediv__(self, other):
        """(f)Defines regular division of two numbers with uncertainties. __rtruediv__ is equivalent so doesn't have to be defined separately."""
        div = Measurement()
        if not isinstance(other, Measurement):
            mul.val = (self.val / other)
            mul.unc = (self.val / other) * (self.unc / self.val)
        else:
            div.val = self.val / other.val
            div.unc = self.val / other.val * ( (self.unc / self.val)**2 + (other.unc / other.val)**2 )**(1/2)
        return div
        
    def __pow__(self, other):
        """(g)Defines raising a numbers with uncertainty to a power of the number with uncertainty. __rpow__ is equivalent so doesn't have to be defined separately."""
        powr = Measurement()
        if not isinstance(other, Measurement):
            powr.val = (self.val ** other)
            powr.unc = self.unc * other * self.val**(other-1)
        else:
            powr.val = self.val**other.val
            powr.unc = ( self.unc**2 * other.val**2 * self.val**(2 * other.val - 2) + other.unc**2 * self.val**(2 * other.val) * (log1p(self.val - 1))**2 )**(1/2)
        #I'm using log1p(x) which returns ln(1+x) because It's more accurate near zero
        return powr
        
def test():
    """(h)Function for testing the Measurement class. Doesn't take any arguments. The tests are added manually from the code so are the values of the variables.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    bool
    
    """
    a = Measurement()
    b = Measurement()
    res = Measurement()
    #(i)
    a.val, a.unc = 2, 3
    b.val, b.unc = 6, 4
    res.val, res.unc = 8, 5
    if ((a + b) != res):
        print("Didn't pass (i)")
        return False
    #(j)
    a.val, a.unc = 6, 3
    b.val, b.unc = 6, 4
    res.val, res.unc = 0, 5
    if ((a - b) != res):
        print("Didn't pass (j)")
        return False
    #(k)
    a.val, a.unc = 9, 3
    b.val, b.unc = 16, 4
    res.val, res.unc = 144, 60
    if ((a * b) != res):
        print("Didn't pass (k)")
        return False 
    #(l)
    res.val, res.unc = 0.5625, 0.234375
    if ((a / b) != res):
        print("Didn't pass (l)")
        return False 
    #(m)
    a.val, a.unc = 17, 3
    b.val, b.unc = 3, 0.2
    res.val, res.unc = 4913, 3809.906315357625
    if ((a**b) != res):
        print("Didn't pass (m)")
        return False 
    #(n)
    a.val, a.unc = 178, 9
    b = 3
    res.val, res.unc = 5639752, 855468
    if ((a**b) != res):
        print("Didn't pass (n)")
        return False 
    return True

