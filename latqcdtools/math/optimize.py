# 
# optimize.py
# 
# H. Sandmeyer
# 
# Some methods related to minimization and Levenberg fits.
#
import multiprocessing
import scipy.optimize as opt
import numpy as np
import latqcdtools.base.logger as logger


def timeout(func, args=(), kwargs={}, timeout_duration=300):
    """ Exit if the fit is taking too long ."""
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    def wrap_func(*wrap_args):
        ret = func(*wrap_args[0], **wrap_args[1])
        wrap_args[2]["ret"] = ret

    p = multiprocessing.Process(target = wrap_func, args = (args, kwargs, return_dict))
    p.start()

    p.join(timeout_duration)

    # If thread is still active
    if p.is_alive():
        # Terminate
        p.terminate()
        p.join()
        raise TimeoutError("Time out for " + str(func))
    return return_dict["ret"]


def minimize(func, jack=None, hess=None, start_params=None, tol=1e-12, maxiter=10000, algorithm=None):

    args = (func, start_params)

    if algorithm == "BFGS":
        kwargs = {'method': algorithm,
                  'jac': jack,
                  'tol': tol,
                  'options': {'gtol': tol, 'maxiter': maxiter}}

    elif algorithm == "TNC":
        kwargs = {'method': algorithm,
                  'jac': jack,
                  'tol': tol,
                  'options': {'maxiter': maxiter}}

    elif algorithm == "COBYLA":
        kwargs = {'method': algorithm,
                  'tol': tol,
                  'options': {'maxiter': maxiter}}

    elif algorithm == "SLSQP":
        kwargs = {'method': algorithm,
                  'jac': jack,
                  'tol': tol,
                  'options': {'maxiter': maxiter}}

    elif algorithm == "L-BFGS-B":
        kwargs = {'method': algorithm,
                  'jac': jack,
                  'tol': tol,
                  'options': {'maxiter': maxiter}}

    elif algorithm == "Powell":
        kwargs = {'method': algorithm,
                  'tol': tol,
                  'options': {'xtol': tol, 'ftol': tol,
                              'maxfev': maxiter}}

    elif algorithm == "Nelder-Mead":
        kwargs = {'method': algorithm,
                  'tol': tol,
                  'options': {'maxiter': maxiter}}

    else:
        kwargs = {'method': algorithm,
                  'jac': jack,
                  'hess': hess,
                  'tol': tol,
                  'options': {'maxiter': maxiter}}

    # At least COBYLA sometimes gets stuck in an endless loop.
    res = timeout(opt.minimize, args=args, kwargs=kwargs, timeout_duration=100)

    params = res.x
    nfev = res.nfev
    if not res.success:
        logger.details(algorithm, res.message)
        raise ValueError(algorithm + ": Minimization did not converge!")

    try:
        params[0]
    except:
        if isinstance(params, (np.ndarray, np.generic)):
            # Somehow numpy 0D arrays have to be converted to scalar explicitly.
            params = [np.asscalar(params)]
        else:
            params = [params]

    return params, nfev
