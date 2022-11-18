#
# utilities.py
#
# D. Clarke, L. Altenkort
#
# Some utilities that you might use in any program.
#
from subprocess import run, PIPE
import numpy as np
import concurrent.futures, time, re
import latqcdtools.base.logger as logger


def envector(*args):
    """ Change obj to a numpy array if it's a scalar. Sometimes required when, e.g., using np.vectorize. """
    result = ()
    for obj in args:
        try:
            obj[0]
        except (TypeError,IndexError):
            obj = np.array([obj])
        result += (obj,)
    if len(result)==1:
        return result[0]
    else:
        return result


def getArgs(parser):
    """ Get arguments from the ArgumentParser. Complain if you don't get exactly the correct arguments. """
    args, invalid_args = parser.parse_known_args()
    if len(invalid_args)>0:
        logger.TBError("Received unrecognized arguments",invalid_args,".")
    return args


def printArg(message,param):
    """ Some arguments are None by default, and you only want to print them if they are set. """
    if param is not None:
        print(message,param)


def printDict(dic):
    """ Prints key, value pairs line by line. """
    if not isinstance(dic,dict):
        logger.TBError("printDict should take a dictionary as argument.")
    for key in dic:
        print(key,dic[key])


def printClean(*args,label=None):
    data = ()
    form = ''
    if label is not None:
        form += '%14s: '
        data += (label,)
    for col in args:
        if isinstance(col,complex):
            data += (col.real,)
            data += (col.imag,)
            form += '(%.8e  %.8e)  '
        else:
            data += (col,)
            form += '%.8e  '
    print(form % data)


def shell(*args):
    """ Carry out the passed arguments args in the shell. Can be passed as a single
        string or as a list. Captures and returns output of shell command. E.g.
          shell('ls -lah')
    """
    args = [str(s) for s in args]
    process = run(' '.join(args),shell=True,check=True,stdout=PIPE,universal_newlines=True)
    return process.stdout


def shellVerbose(*args):
    """ Same as shell, but instead of capturing output, print it to screen. """
    args = [str(s) for s in args]
    process = run(' '.join(args),shell=True,check=True,stdout=PIPE,universal_newlines=True)
    print(process.stdout)


def naturalSort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def find_nearest_idx(array, value):
    """ Find the index of the element of array nearest to value. """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


class timer:

    """ A class to facilitate doing rudimentary timings in the Toolbox. """

    def __init__(self):
        print("\n  Timer initialized.\n")
        self._tstart = time.time()
        self._tend   = self._tstart


    def printTiming(self, message=None):
        self._tstart = self._tend
        self._tend   = time.time()
        timing = self._tend - self._tstart
        if message is None:
            print("\n  Time to finish: %12.8f [s].\n" % timing)
        else:
            print("\n  Time to finish "+message+": %12.8f [s].\n" % timing)


    def resetTimer(self):
        self._tstart = time.time()
        self._tend   = self._tstart


class ComputationClass:

    """ A class to parallelize functions. To be used with parallel_function_eval for convenience. """

    def __init__(self, func, input_array, nproc, *add_param):
        self._nproc = nproc  # number of processes
        self._input_array = input_array
        self._function = func

        # additional arguments for actual_computation
        self._add_param = add_param

        # compute the result when class is initialized
        self._result = self.parallelization_wrapper()

    def parallelization_wrapper(self):
        with concurrent.futures.ProcessPoolExecutor(max_workers=self._nproc) as executor:
            result = executor.map(self.pass_argument_wrapper, self._input_array)
        return list(result)

    def pass_argument_wrapper(self, single_input):
        return self._function(single_input, *self._add_param)

    def getResult(self):
        return self._result


def parallel_function_eval(func, input_array, nproc, *add_param):
    computer = ComputationClass(func, input_array, nproc, *add_param)
    return computer.getResult()