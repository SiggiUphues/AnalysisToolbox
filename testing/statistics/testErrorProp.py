#!/usr/bin/env python3

#
# testErrorProp.py                                                               
# 
# H. Sandmeyer, D. Clarke
# 
# Quick test of the error propagation function.
#

import matplotlib.pyplot as plt
import numpy as np
from latqcdtools.math.math import print_results
from latqcdtools.statistics.statistics import error_prop, error_prop_func, plot_func
from latqcdtools.physics.constants import M_mu_phys 
import latqcdtools.base.logger as logger


logger.set_log_level('INFO')


def func(x, p, OPT):
    A, B = p
    return OPT*A**2*np.sin(x)+B

def grad(x, p, OPT):
    A, B = p
    return [OPT*2*A*np.sin(x), 1]

def err_func(x, p, p_err, OPT):
    A, B = p
    A_err, B_err = p_err
    return np.sqrt((OPT*2*A*np.sin(x)*A_err)**2+B_err**2)


pi                     = np.pi
gamma_E                = np.euler_gamma
m_mu_MeV, m_mu_MeV_err = M_mu_phys(2020,"MeV",True)


def K_G(data):
    t    = data[0]
    m_mu = data[1]
    a    = data[2]
    th   = m_mu*a*t
    return ( pi**2*th**4/9 + pi**2*th**6  *( 120 *np.log(th) + 120 *gamma_E - 169  )/5400
             + pi**2*th**8  *( 210 *np.log(th) + 210 *gamma_E - 401  )/88200
             + pi**2*th**10 *( 360 *np.log(th) + 360 *gamma_E - 787  )/2916000
             + pi**2*th**12 *( 3080*np.log(th) + 3080*gamma_E - 7353 )/768398400
             ) / (a*m_mu)**2


def testErrorProp():

    x_test = [0.5, 0.1, 2]
    a      = 1
    b      = 2
    a_err  = 0.1
    b_err  = 0.2
    opt    = 2

    res_true = err_func(x_test, [1,2], [a_err,b_err], opt)

    res = error_prop_func(x_test, func, params=[1,2], params_err=[a_err,b_err], args=(opt,))
    print_results(res, res_true, text = "Error_prop using numerical derivative")

    res = error_prop_func(x_test, func, grad=grad, params=[1,2], params_err=[a_err,b_err], args=(opt,))
    print_results(res, res_true, text = "Error_prop using analytic gradient")

    plot_func(func, params = (a,b), args=(opt,), func_err = err_func, params_err=[a_err,b_err], xmin=-1, xmax=1)
    plot_func(func, params = (a,b), args=(opt,), params_err = [a_err,b_err], xmin=-1, xmax=1)
    plot_func(func, params = (a,b), args=(opt,), params_err = [a_err,b_err], grad = grad,
              title = "Please check if all error bands are the same", xmin=-1,xmax=1)

    plt.savefig("errorprop.pdf")

    amean, aerr = 0.09, 0.001
    mean, err   = error_prop(K_G, [1,m_mu_MeV,amean], [0,m_mu_MeV_err,aerr])
    REFmean     = 176798.90810433426
    REFerr      = 21366.184730206216

    print_results(mean, REFmean, err, REFerr, text = "Test on BM kernel.")


if __name__ == '__main__':
    testErrorProp()