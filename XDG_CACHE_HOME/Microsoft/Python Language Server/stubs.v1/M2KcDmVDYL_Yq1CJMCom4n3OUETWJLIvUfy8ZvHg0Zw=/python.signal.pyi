import exceptions as _mod_exceptions

ITIMER_PROF = 2L
ITIMER_REAL = 0L
ITIMER_VIRTUAL = 1L
class ItimerError(_mod_exceptions.IOError):
    __class__ = ItimerError
    __dict__ = {}
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    __module__ = 'signal'
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    @property
    def __weakref__(self):
        'list of weak references to the object (if defined)'
        pass
    

NSIG = 65
SIGABRT = 6
SIGALRM = 14
SIGBUS = 7
SIGCHLD = 17
SIGCLD = 17
SIGCONT = 18
SIGFPE = 8
SIGHUP = 1
SIGILL = 4
SIGINT = 2
SIGIO = 29
SIGIOT = 6
SIGKILL = 9
SIGPIPE = 13
SIGPOLL = 29
SIGPROF = 27
SIGPWR = 30
SIGQUIT = 3
SIGRTMAX = 64
SIGRTMIN = 34
SIGSEGV = 11
SIGSTOP = 19
SIGSYS = 31
SIGTERM = 15
SIGTRAP = 5
SIGTSTP = 20
SIGTTIN = 21
SIGTTOU = 22
SIGURG = 23
SIGUSR1 = 10
SIGUSR2 = 12
SIGVTALRM = 26
SIGWINCH = 28
SIGXCPU = 24
SIGXFSZ = 25
SIG_DFL = 0
SIG_IGN = 1
__doc__ = 'This module provides mechanisms to use signal handlers in Python.\n\nFunctions:\n\nalarm() -- cause SIGALRM after a specified time [Unix only]\nsetitimer() -- cause a signal (described below) after a specified\n               float time and the timer may restart then [Unix only]\ngetitimer() -- get current value of timer [Unix only]\nsignal() -- set the action for a given signal\ngetsignal() -- get the signal action for a given signal\npause() -- wait until a signal arrives [Unix only]\ndefault_int_handler() -- default SIGINT handler\n\nsignal constants:\nSIG_DFL -- used to refer to the system default handler\nSIG_IGN -- used to ignore the signal\nNSIG -- number of defined signals\nSIGINT, SIGTERM, etc. -- signal numbers\n\nitimer constants:\nITIMER_REAL -- decrements in real time, and delivers SIGALRM upon\n               expiration\nITIMER_VIRTUAL -- decrements only when the process is executing,\n               and delivers SIGVTALRM upon expiration\nITIMER_PROF -- decrements both when the process is executing and\n               when the system is executing on behalf of the process.\n               Coupled with ITIMER_VIRTUAL, this timer is usually\n               used to profile the time spent by the application\n               in user and kernel space. SIGPROF is delivered upon\n               expiration.\n\n\n*** IMPORTANT NOTICE ***\nA signal handler function is called with two arguments:\nthe first is the signal number, the second is the interrupted stack frame.'
__name__ = 'signal'
__package__ = None
def alarm(seconds):
    'alarm(seconds)\n\nArrange for SIGALRM to arrive after the given number of seconds.'
    pass

def default_int_handler():
    'default_int_handler(...)\n\nThe default handler for SIGINT installed by Python.\nIt raises KeyboardInterrupt.'
    pass

def getitimer(which):
    'getitimer(which)\n\nReturns current value of given itimer.'
    pass

def getsignal(sig):
    'getsignal(sig) -> action\n\nReturn the current action for the given signal.  The return value can be:\nSIG_IGN -- if the signal is being ignored\nSIG_DFL -- if the default action for the signal is in effect\nNone -- if an unknown handler is in effect\nanything else -- the callable Python object used as a handler'
    pass

def pause():
    'pause()\n\nWait until a signal arrives.'
    pass

def set_wakeup_fd(fd):
    "set_wakeup_fd(fd) -> fd\n\nSets the fd to be written to (with '\\0') when a signal\ncomes in.  A library can use this to wakeup select or poll.\nThe previous fd is returned.\n\nThe fd must be non-blocking."
    pass

def setitimer(which, seconds, interval=None):
    'setitimer(which, seconds[, interval])\n\nSets given itimer (one of ITIMER_REAL, ITIMER_VIRTUAL\nor ITIMER_PROF) to fire after value seconds and after\nthat every interval seconds.\nThe itimer can be cleared by setting seconds to zero.\n\nReturns old values as a tuple: (delay, interval).'
    pass

def siginterrupt(sig, flag):
    'siginterrupt(sig, flag) -> None\nchange system call restart behaviour: if flag is False, system calls\nwill be restarted when interrupted by signal sig, else system calls\nwill be interrupted.'
    pass

def signal(sig, action):
    'signal(sig, action) -> action\n\nSet the action for the given signal.  The action can be SIG_DFL,\nSIG_IGN, or a callable Python object.  The previous action is\nreturned.  See getsignal() for possible return values.\n\n*** IMPORTANT NOTICE ***\nA signal handler function is called with two arguments:\nthe first is the signal number, the second is the interrupted stack frame.'
    pass

