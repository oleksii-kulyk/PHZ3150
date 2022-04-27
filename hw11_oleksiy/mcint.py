""" The module that contains functions needed for Monte Carlo integration"""
import numpy as np

N = 10**6 # the number of sample points for the mcint function

def test_mcint():
    """Tests the 'mcint' Monte Carlo integratrion function by running several predefined tests on it.
    
    Returns
    -------
    bool : True or False
    
    See Also
    --------
    mcint(a, b, func, N) : the numerical integration function that is tested by this function.
    
    """
    one = lambda x : 1  # the helper function for test_mcint that always returns 1 e.i. f(x) = 1
    ramp = lambda x : x # the helper function      -//-      that always returns x e.i. f(x) = x
    
    # The following tests make sure that mcint integrates to the range of integration:
    one_passed = []
    one_passed.append( bool( abs( mcint(-2, 1, one) - 3 )  <= 3*0.01 ) )  #1
    one_passed.append( bool( abs( mcint(-5,-4, one) - 1 )  <= 1*0.01 ) )  #2
    one_passed.append( bool( abs( mcint( 0, 5, one) - 5 )  <= 5*0.01 ) )  #3
    one_passed.append( bool( abs( mcint(-1, 0, one) - 1 )  <= 1*0.01 ) )  #4
    one_passed.append( bool( abs( mcint(-10,5, one) - 15 ) <= 15*0.01) )  #5
    print ()
    
    # The following tests make sure that mcint integrates to 0 for the ranges symmetric about 0:
    ramp_passed = []
    ramp_passed.append( bool( abs( mcint(-2, 2, ramp) ) <= 2*0.01 ) )           #1
    ramp_passed.append( bool( abs( mcint(-4, 4, ramp) ) <= 4*0.01 ) )           #2
    ramp_passed.append( bool( abs( mcint(-0, 0, ramp) ) <= 0*0.01 ) )           #3
    ramp_passed.append( bool( abs( mcint(-0.01, 0.01, ramp) ) <= 0.01*0.01 ) )  #4
    ramp_passed.append( bool( abs( mcint(-20, 20, ramp, N = 10**8) ) <= 20*0.01 ) )#5
    #this case needs many more sample points. The use of 10**8 pretty much guarantees that this case will 
    #pass 100% of times. If you are running this of a slower computer, changing N to 10**7 makes the test 
    #pass about 70% of times.
    
    if (all(one_passed) and all(ramp_passed)):
        print("All tests passed!")
        return True
    else:   
        print("Something went wrong\nHere's a summary of the tests:\n")
        print("One function:\n",   one_passed)
        print("Ramp function:\n", ramp_passed, "\n")
        return False

def mcint(a, b, func, N = N):
    """The Monte Carlo integration function.
    
    Integrates the given function by evaluating it in multiple random uniformly disrtibuted points on dx inteval.
    
    Parameters
    ----------
    N : int
        Number of points to take from the interval.
    a : float
        The lower bound of the interval over which the function will be integrated.
    b : float
        The upper bound of the interval over which the function will be integrated (not included).
    func : function object
        The function the will be integrated over the given interval with the given number of sample points.
        
    Returns
    -------
    a number : float
        The integral of a function over the given interval with the given number of sample points.
    
    See Also
    --------
    test_mcint : runs a number of predifined tests on this function.
        
    References
    ----------
    https://en.wikipedia.org/wiki/Monte_Carlo_integration
    
    """
    points = np.random.uniform(a, b, N) # N uniform values on the half-open interval [a, b)
    vfunc = np.vectorize(func) # makes the function take and return and array
    results = vfunc(points)
    return sum(results) * ((b - a) / N) # from the algorithm given in hw11.pdf
    
#Extra Credit
def test_gaussian():
    """
    """
    
def gaussian(x, mu, sigma):
    """
    """
    
