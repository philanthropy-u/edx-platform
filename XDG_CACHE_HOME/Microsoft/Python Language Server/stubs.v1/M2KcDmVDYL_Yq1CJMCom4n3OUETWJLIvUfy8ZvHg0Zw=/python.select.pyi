import __builtin__ as _mod___builtin__
import exceptions as _mod_exceptions

EPOLLERR = 8
EPOLLET = 2147483648
EPOLLHUP = 16
EPOLLIN = 1
EPOLLMSG = 1024
EPOLLONESHOT = 1073741824
EPOLLOUT = 4
EPOLLPRI = 2
EPOLLRDBAND = 128
EPOLLRDNORM = 64
EPOLLWRBAND = 512
EPOLLWRNORM = 256
PIPE_BUF = 4096
POLLERR = 8
POLLHUP = 16
POLLIN = 1
POLLMSG = 1024
POLLNVAL = 32
POLLOUT = 4
POLLPRI = 2
POLLRDBAND = 128
POLLRDNORM = 64
POLLWRBAND = 512
POLLWRNORM = 256
__doc__ = 'This module supports asynchronous I/O on multiple file descriptors.\n\n*** IMPORTANT NOTICE ***\nOn Windows and OpenVMS, only sockets are supported; on Unix, all file descriptors.'
__name__ = 'select'
__package__ = None
class epoll(_mod___builtin__.object):
    "select.epoll([sizehint=-1])\n\nReturns an epolling object\n\nsizehint must be a positive integer or -1 for the default size. The\nsizehint is used to optimize internal data structures. It doesn't limit\nthe maximum number of monitored events."
    __class__ = epoll
    def __getattribute__(self):
        "x.__getattribute__('name') <==> x.name"
        pass
    
    def __init__(self, sizehint=-1):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    def close(self):
        'close() -> None\n\nClose the epoll control file descriptor. Further operations on the epoll\nobject will raise an exception.'
        pass
    
    @property
    def closed(self):
        'True if the epoll handler is closed'
        pass
    
    def fileno(self):
        'fileno() -> int\n\nReturn the epoll control file descriptor.'
        return 1
    
    @classmethod
    def fromfd(cls, fd):
        'fromfd(fd) -> epoll\n\nCreate an epoll object from a given control fd.'
        pass
    
    def modify(self, fd, eventmask):
        'modify(fd, eventmask) -> None\n\nfd is the target file descriptor of the operation\nevents is a bit set composed of the various EPOLL constants'
        pass
    
    def poll(self):
        'poll([timeout=-1[, maxevents=-1]]) -> [(fd, events), (...)]\n\nWait for events on the epoll file descriptor for a maximum time of timeout\nin seconds (as float). -1 makes poll wait indefinitely.\nUp to maxevents are returned to the caller.'
        pass
    
    def register(self, fd, eventmask=None):
        'register(fd[, eventmask]) -> None\n\nRegisters a new fd or raises an IOError if the fd is already registered.\nfd is the target file descriptor of the operation.\nevents is a bit set composed of the various EPOLL constants; the default\nis EPOLL_IN | EPOLL_OUT | EPOLL_PRI.\n\nThe epoll interface supports all file descriptors that support poll.'
        pass
    
    def unregister(self, fd):
        'unregister(fd) -> None\n\nfd is the target file descriptor of the operation.'
        pass
    

class error(_mod_exceptions.Exception):
    __class__ = error
    __dict__ = {}
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    __module__ = 'select'
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    @property
    def __weakref__(self):
        'list of weak references to the object (if defined)'
        pass
    

def poll():
    'Returns a polling object, which supports registering and\nunregistering file descriptors, and then polling them for I/O events.'
    pass

def select(rlist, wlist, xlist, timeout=None):
    "select(rlist, wlist, xlist[, timeout]) -> (rlist, wlist, xlist)\n\nWait until one or more file descriptors are ready for some kind of I/O.\nThe first three arguments are sequences of file descriptors to be waited for:\nrlist -- wait until ready for reading\nwlist -- wait until ready for writing\nxlist -- wait for an ``exceptional condition''\nIf only one kind of condition is required, pass [] for the other lists.\nA file descriptor is either a socket or file object, or a small integer\ngotten from a fileno() method call on one of those.\n\nThe optional 4th argument specifies a timeout in seconds; it may be\na floating point number to specify fractions of seconds.  If it is absent\nor None, the call will never time out.\n\nThe return value is a tuple of three lists corresponding to the first three\narguments; each contains the subset of the corresponding file descriptors\nthat are ready.\n\n*** IMPORTANT NOTICE ***\nOn Windows and OpenVMS, only sockets are supported; on Unix, all file\ndescriptors can be used."
    return tuple()

