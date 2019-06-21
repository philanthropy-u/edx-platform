import __builtin__ as _mod___builtin__
import exceptions as _mod_exceptions

EX_CANTCREAT = 73
EX_CONFIG = 78
EX_DATAERR = 65
EX_IOERR = 74
EX_NOHOST = 68
EX_NOINPUT = 66
EX_NOPERM = 77
EX_NOUSER = 67
EX_OK = 0
EX_OSERR = 71
EX_OSFILE = 72
EX_PROTOCOL = 76
EX_SOFTWARE = 70
EX_TEMPFAIL = 75
EX_UNAVAILABLE = 69
EX_USAGE = 64
F_OK = 0
NGROUPS_MAX = 65536
O_APPEND = 1024
O_ASYNC = 8192
O_CREAT = 64
O_DIRECT = 16384
O_DIRECTORY = 65536
O_DSYNC = 4096
O_EXCL = 128
O_LARGEFILE = 0
O_NDELAY = 2048
O_NOATIME = 262144
O_NOCTTY = 256
O_NOFOLLOW = 131072
O_NONBLOCK = 2048
O_RDONLY = 0
O_RDWR = 2
O_RSYNC = 1052672
O_SYNC = 1052672
O_TRUNC = 512
O_WRONLY = 1
R_OK = 4
ST_APPEND = 256
ST_MANDLOCK = 64
ST_NOATIME = 1024
ST_NODEV = 4
ST_NODIRATIME = 2048
ST_NOEXEC = 8
ST_NOSUID = 2
ST_RDONLY = 1
ST_RELATIME = 4096
ST_SYNCHRONOUS = 16
ST_WRITE = 128
TMP_MAX = 238328
WCONTINUED = 8
def WCOREDUMP(status):
    "WCOREDUMP(status) -> bool\n\nReturn True if the process returning 'status' was dumped to a core file."
    return True

def WEXITSTATUS(status):
    "WEXITSTATUS(status) -> integer\n\nReturn the process return code from 'status'."
    return 1

def WIFCONTINUED(status):
    "WIFCONTINUED(status) -> bool\n\nReturn True if the process returning 'status' was continued from a\njob control stop."
    return True

def WIFEXITED(status):
    "WIFEXITED(status) -> bool\n\nReturn true if the process returning 'status' exited using the exit()\nsystem call."
    return True

def WIFSIGNALED(status):
    "WIFSIGNALED(status) -> bool\n\nReturn True if the process returning 'status' was terminated by a signal."
    return True

def WIFSTOPPED(status):
    "WIFSTOPPED(status) -> bool\n\nReturn True if the process returning 'status' was stopped."
    return True

WNOHANG = 1
def WSTOPSIG(status):
    "WSTOPSIG(status) -> integer\n\nReturn the signal that stopped the process that provided\nthe 'status' value."
    return 1

def WTERMSIG(status):
    "WTERMSIG(status) -> integer\n\nReturn the signal that terminated the process that provided the 'status'\nvalue."
    return 1

WUNTRACED = 2
W_OK = 2
X_OK = 1
__doc__ = 'This module provides access to operating system functionality that is\nstandardized by the C Standard and the POSIX standard (a thinly\ndisguised Unix interface).  Refer to the library manual and\ncorresponding Unix manual entries for more information on calls.'
__name__ = 'posix'
__package__ = None
def _exit(status):
    '_exit(status)\n\nExit to the system with specified status, without normal exit processing.'
    pass

def abort():
    "abort() -> does not return!\n\nAbort the interpreter immediately.  This 'dumps core' or otherwise fails\nin the hardest way possible on the hosting operating system."
    pass

def access(path, mode):
    'access(path, mode) -> True if granted, False otherwise\n\nUse the real uid/gid to test for access to a path.  Note that most\noperations will use the effective uid/gid, therefore this routine can\nbe used in a suid/sgid environment to test if the invoking user has the\nspecified access to the path.  The mode argument can be F_OK to test\nexistence, or the inclusive-OR of R_OK, W_OK, and X_OK.'
    pass

def chdir(path):
    'chdir(path)\n\nChange the current working directory to the specified path.'
    pass

def chmod(path, mode):
    'chmod(path, mode)\n\nChange the access permissions of a file.'
    pass

def chown(path, uid, gid):
    'chown(path, uid, gid)\n\nChange the owner and group id of path to the numeric uid and gid.'
    pass

def chroot(path):
    'chroot(path)\n\nChange root directory to path.'
    pass

def close(fd):
    'close(fd)\n\nClose a file descriptor (for low level IO).'
    pass

def closerange(fd_low, fd_high):
    'closerange(fd_low, fd_high)\n\nCloses all file descriptors in [fd_low, fd_high), ignoring errors.'
    pass

def confstr(name):
    'confstr(name) -> string\n\nReturn a string-valued system configuration variable.'
    return ''

confstr_names = _mod___builtin__.dict()
def ctermid():
    'ctermid() -> string\n\nReturn the name of the controlling terminal for this process.'
    return ''

def dup(fd):
    'dup(fd) -> fd2\n\nReturn a duplicate of a file descriptor.'
    pass

def dup2(old_fd, new_fd):
    'dup2(old_fd, new_fd)\n\nDuplicate file descriptor.'
    pass

environ = _mod___builtin__.dict()
error = _mod_exceptions.OSError
def execv(path, args):
    'execv(path, args)\n\nExecute an executable path with arguments, replacing current process.\n\n    path: path of executable file\n    args: tuple or list of strings'
    pass

def execve(path, args, env):
    'execve(path, args, env)\n\nExecute a path with arguments and environment, replacing current process.\n\n    path: path of executable file\n    args: tuple or list of arguments\n    env: dictionary of strings mapping to strings'
    pass

def fchdir(fildes):
    'fchdir(fildes)\n\nChange to the directory of the given file descriptor.  fildes must be\nopened on a directory, not a file.'
    pass

def fchmod(fd, mode):
    'fchmod(fd, mode)\n\nChange the access permissions of the file given by file\ndescriptor fd.'
    pass

def fchown(fd, uid, gid):
    'fchown(fd, uid, gid)\n\nChange the owner and group id of the file given by file descriptor\nfd to the numeric uid and gid.'
    pass

def fdatasync(fildes):
    'fdatasync(fildes)\n\nforce write of file with filedescriptor to disk.\n does not force update of metadata.'
    pass

def fdopen(fd, mode='r', bufsize=None):
    "fdopen(fd [, mode='r' [, bufsize]]) -> file_object\n\nReturn an open file object connected to a file descriptor."
    pass

def fork():
    'fork() -> pid\n\nFork a child process.\nReturn 0 to child process and PID of child to parent process.'
    pass

def forkpty():
    'forkpty() -> (pid, master_fd)\n\nFork a new process with a new pseudo-terminal as controlling tty.\n\nLike fork(), return 0 as pid to child process, and PID of child to parent.\nTo both, return fd of newly opened pseudo-terminal.\n'
    return tuple()

def fpathconf(fd, name):
    'fpathconf(fd, name) -> integer\n\nReturn the configuration limit name for the file descriptor fd.\nIf there is no limit, return -1.'
    return 1

def fstat(fd):
    'fstat(fd) -> stat result\n\nLike stat(), but for an open file descriptor.'
    pass

def fstatvfs(fd):
    'fstatvfs(fd) -> statvfs result\n\nPerform an fstatvfs system call on the given fd.'
    pass

def fsync(fildes):
    'fsync(fildes)\n\nforce write of file with filedescriptor to disk.'
    pass

def ftruncate(fd, length):
    'ftruncate(fd, length)\n\nTruncate a file to a specified length.'
    pass

def getcwd():
    'getcwd() -> path\n\nReturn a string representing the current working directory.'
    pass

def getcwdu():
    'getcwdu() -> path\n\nReturn a unicode string representing the current working directory.'
    pass

def getegid():
    "getegid() -> egid\n\nReturn the current process's effective group id."
    pass

def geteuid():
    "geteuid() -> euid\n\nReturn the current process's effective user id."
    pass

def getgid():
    "getgid() -> gid\n\nReturn the current process's group id."
    pass

def getgroups():
    'getgroups() -> list of group IDs\n\nReturn list of supplemental group IDs for the process.'
    return list()

def getloadavg():
    'getloadavg() -> (float, float, float)\n\nReturn the number of processes in the system run queue averaged over\nthe last 1, 5, and 15 minutes or raises OSError if the load average\nwas unobtainable'
    return tuple()

def getlogin():
    'getlogin() -> string\n\nReturn the actual login name.'
    return ''

def getpgid(pid):
    'getpgid(pid) -> pgid\n\nCall the system call getpgid().'
    pass

def getpgrp():
    'getpgrp() -> pgrp\n\nReturn the current process group id.'
    pass

def getpid():
    'getpid() -> pid\n\nReturn the current process id'
    pass

def getppid():
    "getppid() -> ppid\n\nReturn the parent's process id."
    pass

def getresgid():
    "getresgid() -> (rgid, egid, sgid)\n\nGet tuple of the current process's real, effective, and saved group ids."
    return tuple()

def getresuid():
    "getresuid() -> (ruid, euid, suid)\n\nGet tuple of the current process's real, effective, and saved user ids."
    return tuple()

def getsid(pid):
    'getsid(pid) -> sid\n\nCall the system call getsid().'
    pass

def getuid():
    "getuid() -> uid\n\nReturn the current process's user id."
    pass

def initgroups(username, gid):
    'initgroups(username, gid) -> None\n\nCall the system initgroups() to initialize the group access list with all of\nthe groups of which the specified username is a member, plus the specified\ngroup id.'
    pass

def isatty(fd):
    "isatty(fd) -> bool\n\nReturn True if the file descriptor 'fd' is an open file descriptor\nconnected to the slave end of a terminal."
    return True

def kill(pid, sig):
    'kill(pid, sig)\n\nKill a process with a signal.'
    pass

def killpg(pgid, sig):
    'killpg(pgid, sig)\n\nKill a process group with a signal.'
    pass

def lchown(path, uid, gid):
    'lchown(path, uid, gid)\n\nChange the owner and group id of path to the numeric uid and gid.\nThis function will not follow symbolic links.'
    pass

def link(src, dst):
    'link(src, dst)\n\nCreate a hard link to a file.'
    pass

def listdir(path):
    "listdir(path) -> list_of_strings\n\nReturn a list containing the names of the entries in the directory.\n\n    path: path of directory to list\n\nThe list is in arbitrary order.  It does not include the special\nentries '.' and '..' even if they are present in the directory."
    return list()

def lseek(fd, pos, how):
    'lseek(fd, pos, how) -> newpos\n\nSet the current position of a file descriptor.\nReturn the new cursor position in bytes, starting from the beginning.'
    pass

def lstat(path):
    'lstat(path) -> stat result\n\nLike stat(path), but do not follow symbolic links.'
    pass

def major(device):
    'major(device) -> major number\nExtracts a device major number from a raw device number.'
    pass

def makedev(major, minor):
    'makedev(major, minor) -> device number\nComposes a raw device number from the major and minor device numbers.'
    pass

def minor(device):
    'minor(device) -> minor number\nExtracts a device minor number from a raw device number.'
    pass

def mkdir(path, mode=0777):
    'mkdir(path [, mode=0777])\n\nCreate a directory.'
    pass

def mkfifo(filename, mode=0666):
    'mkfifo(filename [, mode=0666])\n\nCreate a FIFO (a POSIX named pipe).'
    pass

def mknod(filename, mode=0600, device=None):
    'mknod(filename [, mode=0600, device])\n\nCreate a filesystem node (file, device special file or named pipe)\nnamed filename. mode specifies both the permissions to use and the\ntype of node to be created, being combined (bitwise OR) with one of\nS_IFREG, S_IFCHR, S_IFBLK, and S_IFIFO. For S_IFCHR and S_IFBLK,\ndevice defines the newly created device special file (probably using\nos.makedev()), otherwise it is ignored.'
    pass

def nice(inc):
    'nice(inc) -> new_priority\n\nDecrease the priority of process by inc and return the new priority.'
    pass

def open(filename, flag, mode=0777):
    'open(filename, flag [, mode=0777]) -> fd\n\nOpen a file (for low level IO).'
    pass

def openpty():
    "openpty() -> (master_fd, slave_fd)\n\nOpen a pseudo-terminal, returning open fd's for both master and slave end.\n"
    return tuple()

def pathconf(path, name):
    'pathconf(path, name) -> integer\n\nReturn the configuration limit name for the file or directory path.\nIf there is no limit, return -1.'
    return 1

pathconf_names = _mod___builtin__.dict()
def pipe():
    'pipe() -> (read_end, write_end)\n\nCreate a pipe.'
    return tuple()

def popen(command, mode='r', bufsize=None):
    "popen(command [, mode='r' [, bufsize]]) -> pipe\n\nOpen a pipe to/from a command returning a file object."
    pass

def putenv(key, value):
    'putenv(key, value)\n\nChange or add an environment variable.'
    pass

def read(fd, buffersize):
    'read(fd, buffersize) -> string\n\nRead a file descriptor.'
    return ''

def readlink(path):
    'readlink(path) -> path\n\nReturn a string representing the path to which the symbolic link points.'
    pass

def remove(path):
    'remove(path)\n\nRemove a file (same as unlink(path)).'
    pass

def rename(old, new):
    'rename(old, new)\n\nRename a file or directory.'
    pass

def rmdir(path):
    'rmdir(path)\n\nRemove a directory.'
    pass

def setegid(gid):
    "setegid(gid)\n\nSet the current process's effective group id."
    pass

def seteuid(uid):
    "seteuid(uid)\n\nSet the current process's effective user id."
    pass

def setgid(gid):
    "setgid(gid)\n\nSet the current process's group id."
    pass

def setgroups(list):
    'setgroups(list)\n\nSet the groups of the current process to list.'
    pass

def setpgid(pid, pgrp):
    'setpgid(pid, pgrp)\n\nCall the system call setpgid().'
    pass

def setpgrp():
    'setpgrp()\n\nMake this process the process group leader.'
    pass

def setregid(rgid, egid):
    "setregid(rgid, egid)\n\nSet the current process's real and effective group ids."
    pass

def setresgid(rgid, egid, sgid):
    "setresgid(rgid, egid, sgid)\n\nSet the current process's real, effective, and saved group ids."
    pass

def setresuid(ruid, euid, suid):
    "setresuid(ruid, euid, suid)\n\nSet the current process's real, effective, and saved user ids."
    pass

def setreuid(ruid, euid):
    "setreuid(ruid, euid)\n\nSet the current process's real and effective user ids."
    pass

def setsid():
    'setsid()\n\nCall the system call setsid().'
    pass

def setuid(uid):
    "setuid(uid)\n\nSet the current process's user id."
    pass

def stat(path):
    'stat(path) -> stat result\n\nPerform a stat system call on the given path.'
    pass

def stat_float_times(newval=None):
    'stat_float_times([newval]) -> oldval\n\nDetermine whether os.[lf]stat represents time stamps as float objects.\nIf newval is True, future calls to stat() return floats, if it is False,\nfuture calls return ints. \nIf newval is omitted, return the current setting.\n'
    pass

class stat_result(_mod___builtin__.object):
    'stat_result: Result from stat or lstat.\n\nThis object may be accessed either as a tuple of\n  (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)\nor via the attributes st_mode, st_ino, st_dev, st_nlink, st_uid, and so on.\n\nPosix/windows: If your platform supports st_blksize, st_blocks, st_rdev,\nor st_flags, they are available as attributes only.\n\nSee os.stat for more information.'
    def __add__(self):
        'x.__add__(y) <==> x+y'
        return stat_result()
    
    __class__ = stat_result
    def __contains__(self, value):
        'x.__contains__(y) <==> y in x'
        return False
    
    def __eq__(self):
        'x.__eq__(y) <==> x==y'
        return False
    
    def __ge__(self):
        'x.__ge__(y) <==> x>=y'
        return False
    
    def __getitem__(self, index):
        'x.__getitem__(y) <==> x[y]'
        pass
    
    def __getslice__(self):
        'x.__getslice__(i, j) <==> x[i:j]\n           \n           Use of negative indices is not supported.'
        return stat_result()
    
    def __gt__(self):
        'x.__gt__(y) <==> x>y'
        return False
    
    def __hash__(self):
        'x.__hash__() <==> hash(x)'
        return 0
    
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    def __le__(self):
        'x.__le__(y) <==> x<=y'
        return False
    
    def __len__(self):
        'x.__len__() <==> len(x)'
        return 0
    
    def __lt__(self):
        'x.__lt__(y) <==> x<y'
        return False
    
    def __mul__(self):
        'x.__mul__(n) <==> x*n'
        return stat_result()
    
    def __ne__(self):
        'x.__ne__(y) <==> x!=y'
        return False
    
    def __reduce__(self):
        return ''; return ()
    
    def __repr__(self):
        'x.__repr__() <==> repr(x)'
        return ''
    
    def __rmul__(self):
        'x.__rmul__(n) <==> n*x'
        return stat_result()
    
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    n_fields = 16
    n_sequence_fields = 10
    n_unnamed_fields = 3
    @property
    def st_atime(self):
        'time of last access'
        pass
    
    @property
    def st_blksize(self):
        'blocksize for filesystem I/O'
        pass
    
    @property
    def st_blocks(self):
        'number of blocks allocated'
        pass
    
    @property
    def st_ctime(self):
        'time of last change'
        pass
    
    @property
    def st_dev(self):
        'device'
        pass
    
    @property
    def st_gid(self):
        'group ID of owner'
        pass
    
    @property
    def st_ino(self):
        'inode'
        pass
    
    @property
    def st_mode(self):
        'protection bits'
        pass
    
    @property
    def st_mtime(self):
        'time of last modification'
        pass
    
    @property
    def st_nlink(self):
        'number of hard links'
        pass
    
    @property
    def st_rdev(self):
        'device type (if inode device)'
        pass
    
    @property
    def st_size(self):
        'total size, in bytes'
        pass
    
    @property
    def st_uid(self):
        'user ID of owner'
        pass
    

def statvfs(path):
    'statvfs(path) -> statvfs result\n\nPerform a statvfs system call on the given path.'
    pass

class statvfs_result(_mod___builtin__.object):
    'statvfs_result: Result from statvfs or fstatvfs.\n\nThis object may be accessed either as a tuple of\n  (bsize, frsize, blocks, bfree, bavail, files, ffree, favail, flag, namemax),\nor via the attributes f_bsize, f_frsize, f_blocks, f_bfree, and so on.\n\nSee os.statvfs for more information.'
    def __add__(self):
        'x.__add__(y) <==> x+y'
        return statvfs_result()
    
    __class__ = statvfs_result
    def __contains__(self, value):
        'x.__contains__(y) <==> y in x'
        return False
    
    def __eq__(self):
        'x.__eq__(y) <==> x==y'
        return False
    
    def __ge__(self):
        'x.__ge__(y) <==> x>=y'
        return False
    
    def __getitem__(self, index):
        'x.__getitem__(y) <==> x[y]'
        pass
    
    def __getslice__(self):
        'x.__getslice__(i, j) <==> x[i:j]\n           \n           Use of negative indices is not supported.'
        return statvfs_result()
    
    def __gt__(self):
        'x.__gt__(y) <==> x>y'
        return False
    
    def __hash__(self):
        'x.__hash__() <==> hash(x)'
        return 0
    
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    def __le__(self):
        'x.__le__(y) <==> x<=y'
        return False
    
    def __len__(self):
        'x.__len__() <==> len(x)'
        return 0
    
    def __lt__(self):
        'x.__lt__(y) <==> x<y'
        return False
    
    def __mul__(self):
        'x.__mul__(n) <==> x*n'
        return statvfs_result()
    
    def __ne__(self):
        'x.__ne__(y) <==> x!=y'
        return False
    
    def __reduce__(self):
        return ''; return ()
    
    def __repr__(self):
        'x.__repr__() <==> repr(x)'
        return ''
    
    def __rmul__(self):
        'x.__rmul__(n) <==> n*x'
        return statvfs_result()
    
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    @property
    def f_bavail(self):
        pass
    
    @property
    def f_bfree(self):
        pass
    
    @property
    def f_blocks(self):
        pass
    
    @property
    def f_bsize(self):
        pass
    
    @property
    def f_favail(self):
        pass
    
    @property
    def f_ffree(self):
        pass
    
    @property
    def f_files(self):
        pass
    
    @property
    def f_flag(self):
        pass
    
    @property
    def f_frsize(self):
        pass
    
    @property
    def f_namemax(self):
        pass
    
    n_fields = 10
    n_sequence_fields = 10
    n_unnamed_fields = 0

def strerror(code):
    'strerror(code) -> string\n\nTranslate an error code to a message string.'
    return ''

def symlink(src, dst):
    'symlink(src, dst)\n\nCreate a symbolic link pointing to src named dst.'
    pass

def sysconf(name):
    'sysconf(name) -> integer\n\nReturn an integer-valued system configuration variable.'
    return 1

sysconf_names = _mod___builtin__.dict()
def system(command):
    'system(command) -> exit_status\n\nExecute the command (a string) in a subshell.'
    pass

def tcgetpgrp(fd):
    'tcgetpgrp(fd) -> pgid\n\nReturn the process group associated with the terminal given by a fd.'
    pass

def tcsetpgrp(fd, pgid):
    'tcsetpgrp(fd, pgid)\n\nSet the process group associated with the terminal given by a fd.'
    pass

def tempnam(dir=None, prefix=None):
    'tempnam([dir[, prefix]]) -> string\n\nReturn a unique name for a temporary file.\nThe directory and a prefix may be specified as strings; they may be omitted\nor None if not needed.'
    return ''

def times():
    'times() -> (utime, stime, cutime, cstime, elapsed_time)\n\nReturn a tuple of floating point numbers indicating process times.'
    return tuple()

def tmpfile():
    'tmpfile() -> file object\n\nCreate a temporary file with no directory entries.'
    pass

def tmpnam():
    'tmpnam() -> string\n\nReturn a unique name for a temporary file.'
    return ''

def ttyname(fd):
    "ttyname(fd) -> string\n\nReturn the name of the terminal device connected to 'fd'."
    return ''

def umask(new_mask):
    'umask(new_mask) -> old_mask\n\nSet the current numeric umask and return the previous umask.'
    pass

def uname():
    'uname() -> (sysname, nodename, release, version, machine)\n\nReturn a tuple identifying the current operating system.'
    return tuple()

def unlink(path):
    'unlink(path)\n\nRemove a file (same as remove(path)).'
    pass

def unsetenv(key):
    'unsetenv(key)\n\nDelete an environment variable.'
    pass

def urandom(n):
    'urandom(n) -> str\n\nReturn n random bytes suitable for cryptographic use.'
    return ''

def utime(path, atime, mtime):
    'utime(path, (atime, mtime))\nutime(path, None)\n\nSet the access and modified time of the file to the given values.  If the\nsecond form is used, set the access and modified times to the current time.'
    pass

def wait():
    'wait() -> (pid, status)\n\nWait for completion of a child process.'
    return tuple()

def wait3(options):
    'wait3(options) -> (pid, status, rusage)\n\nWait for completion of a child process.'
    return tuple()

def wait4(pid, options):
    'wait4(pid, options) -> (pid, status, rusage)\n\nWait for completion of a given child process.'
    return tuple()

def waitpid(pid, options):
    'waitpid(pid, options) -> (pid, status)\n\nWait for completion of a given child process.'
    return tuple()

def write(fd, string):
    'write(fd, string) -> byteswritten\n\nWrite a string to a file descriptor.'
    pass

