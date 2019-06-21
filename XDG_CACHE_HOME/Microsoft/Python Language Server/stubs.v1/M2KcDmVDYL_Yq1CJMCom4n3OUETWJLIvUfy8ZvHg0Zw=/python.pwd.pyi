import __builtin__ as _mod___builtin__

__doc__ = "This module provides access to the Unix password database.\nIt is available on all Unix versions.\n\nPassword database entries are reported as 7-tuples containing the following\nitems from the password database (see `<pwd.h>'), in order:\npw_name, pw_passwd, pw_uid, pw_gid, pw_gecos, pw_dir, pw_shell.\nThe uid and gid items are integers, all others are strings. An\nexception is raised if the entry asked for cannot be found."
__name__ = 'pwd'
__package__ = None
def getpwall():
    'getpwall() -> list_of_entries\nReturn a list of all available password database entries, in arbitrary order.\nSee help(pwd) for more on password database entries.'
    return list()

def getpwnam():
    'getpwnam(name) -> (pw_name,pw_passwd,pw_uid,\n                    pw_gid,pw_gecos,pw_dir,pw_shell)\nReturn the password database entry for the given user name.\nSee help(pwd) for more on password database entries.'
    return tuple()

def getpwuid():
    'getpwuid(uid) -> (pw_name,pw_passwd,pw_uid,\n                  pw_gid,pw_gecos,pw_dir,pw_shell)\nReturn the password database entry for the given numeric user ID.\nSee help(pwd) for more on password database entries.'
    return tuple()

class struct_passwd(_mod___builtin__.object):
    'pwd.struct_passwd: Results from getpw*() routines.\n\nThis object may be accessed either as a tuple of\n  (pw_name,pw_passwd,pw_uid,pw_gid,pw_gecos,pw_dir,pw_shell)\nor via the object attributes as named in the above tuple.'
    def __add__(self):
        'x.__add__(y) <==> x+y'
        return struct_passwd()
    
    __class__ = struct_passwd
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
        return struct_passwd()
    
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
        return struct_passwd()
    
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
        return struct_passwd()
    
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    n_fields = 7
    n_sequence_fields = 7
    n_unnamed_fields = 0
    @property
    def pw_dir(self):
        'home directory'
        pass
    
    @property
    def pw_gecos(self):
        'real name'
        pass
    
    @property
    def pw_gid(self):
        'group id'
        pass
    
    @property
    def pw_name(self):
        'user name'
        pass
    
    @property
    def pw_passwd(self):
        'password'
        pass
    
    @property
    def pw_shell(self):
        'shell program'
        pass
    
    @property
    def pw_uid(self):
        'user id'
        pass
    

struct_pwent = struct_passwd()
