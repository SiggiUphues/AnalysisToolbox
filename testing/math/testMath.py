# 
# testMath.py                                                               
# 
# D. Clarke
# 
# For testing some of the basic math functions.
#
import numpy as np
import math
import latqcdtools.base.logger as logger
from latqcdtools.math.math import fallFactorial, riseFactorial, invert 
from latqcdtools.testing import print_results, concludeTest


logger.set_log_level('INFO')

mat = [[ 1,2,-1],
       [ 2,1, 2],
       [-1,2, 1]]
mat = np.array(mat)

def testMath():

    lpass = True

    lpass *= print_results(fallFactorial(23,23),1.*math.factorial(23),text='fallFactorial 23!')
    lpass *= print_results(fallFactorial(6,3),6*5*4,text='fallFactorial 6_fall_3')

    inv = invert(mat,'scipy')

    lpass *= print_results(inv,invert(mat,'numpy'),text='scipy vs numpy')
    lpass *= print_results(inv,invert(mat,'svd'),text='scipy vs svd')

    concludeTest(lpass)


if __name__ == '__main__':
    testMath()