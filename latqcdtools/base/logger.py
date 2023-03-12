# 
# logger.py                                                               
# 
# H. Sandmeyer, D. Clarke 
# 
# Methods for logging and output.
# 
import sys, inspect
from colorama import Fore


class bcolors:

    """ Colors for logging messages. """

    def __init__(self):
        pass
    PASS    = Fore.GREEN
    WARNING = Fore.YELLOW 
    FAIL    = Fore.RED 
    ENDC    = '\033[0m'


# Set the log level here.
current_level = 4
log_levels = {
        'ALL' : 0,
        'DEBUG' : 1,
        'DETAILS' : 2,
        'PROGRESS' : 3,
        'INFO' : 4,
        'WARN' : 5,
        'NONE' : 6
        }


recordLog = False
logFile   = None
def createLogFile(filename="Toolbox.log"):
    """ Have output sent also to a log file. """
    global recordLog
    global logFile
    logFile = open(filename,'w')
    recordLog = True


def closeLogFile():
    """ Close the log file. """
    global recordLog
    global logFile
    if not recordLog:
        warn('Attempted to close log file with makeLog=False.')
    logFile.close()
    recordLog = False


def log(outString):
    global recordLog
    global logFile
    if recordLog:
        logFile.write(outString)


def getCallerName(frame):
    """ Gets the name of the function that calls the present function. """
    currframe = inspect.currentframe()
    callframe = inspect.getouterframes(currframe, 2)
    # The way the frame works: Each nested function is labelled by the first index. 0 is the current function, i.e.
    # getCallerName. 1 is the function that called this function, and so on. Second index = 3 retrieves the name.
    callerName = str(callframe[frame][3])
    return callerName


# ----------------------------------------------------------------------------------------------- DEPENDENT ON LOG LEVEL


def isLevel(level):
    return log_levels[level] >= current_level


def set_log_level(level):
    global current_level
    current_level = log_levels[level]



def debug(*args,frame=2):
    if current_level <= 1:
        args = [str(s) for s in args]
        callerName = getCallerName(frame)
        output = '  DEBUG: '+callerName+'--'+(' '.join(args))
        print(output)
        log(output+'\n')


def details(*args):
    if current_level <= 2:
        args = [str(s) for s in args]
        output = '  DETAILS: '+(' '.join(args))
        print(output)
        log(output+'\n')


def progress(*args):
    if current_level <= 3:
        args = [str(s) for s in args]
        output = '  PROGRESS: '+(' '.join(args))
        print(output)
        log(output+'\n')


def info(*args):
    if current_level <= 4:
        args = [str(s) for s in args]
        output = '  INFO: '+(' '.join(args))
        print(output)
        log(output+'\n')


def warn(*args,frame=2):
    if current_level <= 5:
        args = [str(s) for s in args]
        callerName = getCallerName(frame)
        output = bcolors.WARNING+'  WARNING: '+callerName+'--'+(' '.join(args))+bcolors.ENDC
        print(output)
        log(output+'\n')


# --------------------------------------------------------------------------------------------- INDEPENDENT OF LOG LEVEL


def TBFail(*args):
    args = [str(s) for s in args]
    output = bcolors.FAIL+'  FAIL: '+(' '.join(args))+bcolors.ENDC
    print(output)
    log(output + '\n')


def TBError(*args,frame=2):
    args = [str(s) for s in args]
    callerName = getCallerName(frame)
    output = bcolors.FAIL+'  ERROR: '+callerName+'--'+(' '.join(args))+bcolors.ENDC
    print(output)
    log(output + '\n')
    sys.exit(-1)


def TBPass(*args):
    args = [str(s) for s in args]
    output = bcolors.PASS+'  SUCCESS: '+(' '.join(args))+bcolors.ENDC
    print(output)
    log(output + '\n')

