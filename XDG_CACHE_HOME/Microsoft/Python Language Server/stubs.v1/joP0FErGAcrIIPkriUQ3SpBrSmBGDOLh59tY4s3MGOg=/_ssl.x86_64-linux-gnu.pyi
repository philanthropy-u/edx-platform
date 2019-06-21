class tuple(object):
    "tuple() -> empty tuple\ntuple(iterable) -> tuple initialized from iterable's items\n\nIf the argument is a tuple, the return value is the same object."
    def __add__(self):
        'x.__add__(y) <==> x+y'
        return tuple()
    
    __class__ = tuple
    def __contains__(self, value):
        'x.__contains__(y) <==> y in x'
        return False
    
    def __eq__(self):
        'x.__eq__(y) <==> x==y'
        return False
    
    def __ge__(self):
        'x.__ge__(y) <==> x>=y'
        return False
    
    def __getattribute__(self):
        "x.__getattribute__('name') <==> x.name"
        pass
    
    def __getitem__(self, index):
        'x.__getitem__(y) <==> x[y]'
        pass
    
    def __getnewargs__(self):
        return ()
    
    def __getslice__(self):
        'x.__getslice__(i, j) <==> x[i:j]\n           \n           Use of negative indices is not supported.'
        return tuple()
    
    def __gt__(self):
        'x.__gt__(y) <==> x>y'
        return False
    
    def __hash__(self):
        'x.__hash__() <==> hash(x)'
        return 0
    
    def __init__(self, iterable):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    def __iter__(self):
        'x.__iter__() <==> iter(x)'
        return tuple()
    
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
        return tuple()
    
    def __ne__(self):
        'x.__ne__(y) <==> x!=y'
        return False
    
    def __repr__(self):
        'x.__repr__() <==> repr(x)'
        return ''
    
    def __rmul__(self):
        'x.__rmul__(n) <==> n*x'
        return tuple()
    
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    def count(self):
        'T.count(value) -> integer -- return number of occurrences of value'
        return 1
    
    def index(self):
        'T.index(value, [start, [stop]]) -> integer -- return first index of value.\nRaises ValueError if the value is not present.'
        return 1
    

class tuple(object):
    "tuple() -> empty tuple\ntuple(iterable) -> tuple initialized from iterable's items\n\nIf the argument is a tuple, the return value is the same object."
    def __add__(self):
        'x.__add__(y) <==> x+y'
        return tuple()
    
    __class__ = tuple
    def __contains__(self, value):
        'x.__contains__(y) <==> y in x'
        return False
    
    def __eq__(self):
        'x.__eq__(y) <==> x==y'
        return False
    
    def __ge__(self):
        'x.__ge__(y) <==> x>=y'
        return False
    
    def __getattribute__(self):
        "x.__getattribute__('name') <==> x.name"
        pass
    
    def __getitem__(self, index):
        'x.__getitem__(y) <==> x[y]'
        pass
    
    def __getnewargs__(self):
        return ()
    
    def __getslice__(self):
        'x.__getslice__(i, j) <==> x[i:j]\n           \n           Use of negative indices is not supported.'
        return tuple()
    
    def __gt__(self):
        'x.__gt__(y) <==> x>y'
        return False
    
    def __hash__(self):
        'x.__hash__() <==> hash(x)'
        return 0
    
    def __init__(self, iterable):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    def __iter__(self):
        'x.__iter__() <==> iter(x)'
        return tuple()
    
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
        return tuple()
    
    def __ne__(self):
        'x.__ne__(y) <==> x!=y'
        return False
    
    def __repr__(self):
        'x.__repr__() <==> repr(x)'
        return ''
    
    def __rmul__(self):
        'x.__rmul__(n) <==> n*x'
        return tuple()
    
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    def count(self):
        'T.count(value) -> integer -- return number of occurrences of value'
        return 1
    
    def index(self):
        'T.index(value, [start, [stop]]) -> integer -- return first index of value.\nRaises ValueError if the value is not present.'
        return 1
    

class dict(object):
    "dict() -> new empty dictionary\ndict(mapping) -> new dictionary initialized from a mapping object's\n    (key, value) pairs\ndict(iterable) -> new dictionary initialized as if via:\n    d = {}\n    for k, v in iterable:\n        d[k] = v\ndict(**kwargs) -> new dictionary initialized with the name=value pairs\n    in the keyword argument list.  For example:  dict(one=1, two=2)"
    __class__ = dict
    def __cmp__(self):
        'x.__cmp__(y) <==> cmp(x,y)'
        pass
    
    def __contains__(self, value):
        'D.__contains__(k) -> True if D has a key k, else False'
        return False
    
    def __delitem__(self):
        'x.__delitem__(y) <==> del x[y]'
        return None
    
    def __eq__(self):
        'x.__eq__(y) <==> x==y'
        return False
    
    def __ge__(self):
        'x.__ge__(y) <==> x>=y'
        return False
    
    def __getattribute__(self):
        "x.__getattribute__('name') <==> x.name"
        pass
    
    def __getitem__(self, index):
        'x.__getitem__(y) <==> x[y]'
        pass
    
    def __gt__(self):
        'x.__gt__(y) <==> x>y'
        return False
    
    __hash__ = None
    def __init__(self, iterable):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    def __iter__(self):
        'x.__iter__() <==> iter(x)'
        return dict()
    
    def __le__(self):
        'x.__le__(y) <==> x<=y'
        return False
    
    def __len__(self):
        'x.__len__() <==> len(x)'
        return 0
    
    def __lt__(self):
        'x.__lt__(y) <==> x<y'
        return False
    
    def __ne__(self):
        'x.__ne__(y) <==> x!=y'
        return False
    
    def __repr__(self):
        'x.__repr__() <==> repr(x)'
        return ''
    
    def __setitem__(self, index, value):
        'x.__setitem__(i, y) <==> x[i]=y'
        return None
    
    def __sizeof__(self):
        'D.__sizeof__() -> size of D in memory, in bytes'
        return 0
    
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    def clear(self):
        'D.clear() -> None.  Remove all items from D.'
        pass
    
    def copy(self):
        'D.copy() -> a shallow copy of D'
        pass
    
    @classmethod
    def fromkeys(cls):
        'dict.fromkeys(S[,v]) -> New dict with keys from S and values equal to v.\nv defaults to None.'
        pass
    
    def get(self):
        'D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.'
        pass
    
    def has_key(self):
        'D.has_key(k) -> True if D has a key k, else False'
        pass
    
    def items(self):
        "D.items() -> list of D's (key, value) pairs, as 2-tuples"
        return list()
    
    def iteritems(self):
        'D.iteritems() -> an iterator over the (key, value) items of D'
        pass
    
    def iterkeys(self):
        'D.iterkeys() -> an iterator over the keys of D'
        pass
    
    def itervalues(self):
        'D.itervalues() -> an iterator over the values of D'
        pass
    
    def keys(self):
        "D.keys() -> list of D's keys"
        return list()
    
    def pop(self):
        'D.pop(k[,d]) -> v, remove specified key and return the corresponding value.\nIf key is not found, d is returned if given, otherwise KeyError is raised'
        pass
    
    def popitem(self):
        'D.popitem() -> (k, v), remove and return some (key, value) pair as a\n2-tuple; but raise KeyError if D is empty.'
        return tuple()
    
    def setdefault(self):
        'D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D'
        pass
    
    def update(self):
        'D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.\nIf E present and has a .keys() method, does:     for k in E: D[k] = E[k]\nIf E present and lacks .keys() method, does:     for (k, v) in E: D[k] = v\nIn either case, this is followed by: for k in F: D[k] = F[k]'
        pass
    
    def values(self):
        "D.values() -> list of D's values"
        return list()
    
    def viewitems(self):
        "D.viewitems() -> a set-like object providing a view on D's items"
        pass
    
    def viewkeys(self):
        "D.viewkeys() -> a set-like object providing a view on D's keys"
        pass
    
    def viewvalues(self):
        "D.viewvalues() -> an object providing a view on D's values"
        pass
    

class dict(object):
    "dict() -> new empty dictionary\ndict(mapping) -> new dictionary initialized from a mapping object's\n    (key, value) pairs\ndict(iterable) -> new dictionary initialized as if via:\n    d = {}\n    for k, v in iterable:\n        d[k] = v\ndict(**kwargs) -> new dictionary initialized with the name=value pairs\n    in the keyword argument list.  For example:  dict(one=1, two=2)"
    __class__ = dict
    def __cmp__(self):
        'x.__cmp__(y) <==> cmp(x,y)'
        pass
    
    def __contains__(self, value):
        'D.__contains__(k) -> True if D has a key k, else False'
        return False
    
    def __delitem__(self):
        'x.__delitem__(y) <==> del x[y]'
        return None
    
    def __eq__(self):
        'x.__eq__(y) <==> x==y'
        return False
    
    def __ge__(self):
        'x.__ge__(y) <==> x>=y'
        return False
    
    def __getattribute__(self):
        "x.__getattribute__('name') <==> x.name"
        pass
    
    def __getitem__(self, index):
        'x.__getitem__(y) <==> x[y]'
        pass
    
    def __gt__(self):
        'x.__gt__(y) <==> x>y'
        return False
    
    __hash__ = None
    def __init__(self, iterable):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    def __iter__(self):
        'x.__iter__() <==> iter(x)'
        return dict()
    
    def __le__(self):
        'x.__le__(y) <==> x<=y'
        return False
    
    def __len__(self):
        'x.__len__() <==> len(x)'
        return 0
    
    def __lt__(self):
        'x.__lt__(y) <==> x<y'
        return False
    
    def __ne__(self):
        'x.__ne__(y) <==> x!=y'
        return False
    
    def __repr__(self):
        'x.__repr__() <==> repr(x)'
        return ''
    
    def __setitem__(self, index, value):
        'x.__setitem__(i, y) <==> x[i]=y'
        return None
    
    def __sizeof__(self):
        'D.__sizeof__() -> size of D in memory, in bytes'
        return 0
    
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    def clear(self):
        'D.clear() -> None.  Remove all items from D.'
        pass
    
    def copy(self):
        'D.copy() -> a shallow copy of D'
        pass
    
    @classmethod
    def fromkeys(cls):
        'dict.fromkeys(S[,v]) -> New dict with keys from S and values equal to v.\nv defaults to None.'
        pass
    
    def get(self):
        'D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.'
        pass
    
    def has_key(self):
        'D.has_key(k) -> True if D has a key k, else False'
        pass
    
    def items(self):
        "D.items() -> list of D's (key, value) pairs, as 2-tuples"
        return list()
    
    def iteritems(self):
        'D.iteritems() -> an iterator over the (key, value) items of D'
        pass
    
    def iterkeys(self):
        'D.iterkeys() -> an iterator over the keys of D'
        pass
    
    def itervalues(self):
        'D.itervalues() -> an iterator over the values of D'
        pass
    
    def keys(self):
        "D.keys() -> list of D's keys"
        return list()
    
    def pop(self):
        'D.pop(k[,d]) -> v, remove specified key and return the corresponding value.\nIf key is not found, d is returned if given, otherwise KeyError is raised'
        pass
    
    def popitem(self):
        'D.popitem() -> (k, v), remove and return some (key, value) pair as a\n2-tuple; but raise KeyError if D is empty.'
        return tuple()
    
    def setdefault(self):
        'D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D'
        pass
    
    def update(self):
        'D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.\nIf E present and has a .keys() method, does:     for k in E: D[k] = E[k]\nIf E present and lacks .keys() method, does:     for (k, v) in E: D[k] = v\nIn either case, this is followed by: for k in F: D[k] = F[k]'
        pass
    
    def values(self):
        "D.values() -> list of D's values"
        return list()
    
    def viewitems(self):
        "D.viewitems() -> a set-like object providing a view on D's items"
        pass
    
    def viewkeys(self):
        "D.viewkeys() -> a set-like object providing a view on D's keys"
        pass
    
    def viewvalues(self):
        "D.viewvalues() -> an object providing a view on D's values"
        pass
    

class dict(object):
    "dict() -> new empty dictionary\ndict(mapping) -> new dictionary initialized from a mapping object's\n    (key, value) pairs\ndict(iterable) -> new dictionary initialized as if via:\n    d = {}\n    for k, v in iterable:\n        d[k] = v\ndict(**kwargs) -> new dictionary initialized with the name=value pairs\n    in the keyword argument list.  For example:  dict(one=1, two=2)"
    __class__ = dict
    def __cmp__(self):
        'x.__cmp__(y) <==> cmp(x,y)'
        pass
    
    def __contains__(self, value):
        'D.__contains__(k) -> True if D has a key k, else False'
        return False
    
    def __delitem__(self):
        'x.__delitem__(y) <==> del x[y]'
        return None
    
    def __eq__(self):
        'x.__eq__(y) <==> x==y'
        return False
    
    def __ge__(self):
        'x.__ge__(y) <==> x>=y'
        return False
    
    def __getattribute__(self):
        "x.__getattribute__('name') <==> x.name"
        pass
    
    def __getitem__(self, index):
        'x.__getitem__(y) <==> x[y]'
        pass
    
    def __gt__(self):
        'x.__gt__(y) <==> x>y'
        return False
    
    __hash__ = None
    def __init__(self, iterable):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    def __iter__(self):
        'x.__iter__() <==> iter(x)'
        return dict()
    
    def __le__(self):
        'x.__le__(y) <==> x<=y'
        return False
    
    def __len__(self):
        'x.__len__() <==> len(x)'
        return 0
    
    def __lt__(self):
        'x.__lt__(y) <==> x<y'
        return False
    
    def __ne__(self):
        'x.__ne__(y) <==> x!=y'
        return False
    
    def __repr__(self):
        'x.__repr__() <==> repr(x)'
        return ''
    
    def __setitem__(self, index, value):
        'x.__setitem__(i, y) <==> x[i]=y'
        return None
    
    def __sizeof__(self):
        'D.__sizeof__() -> size of D in memory, in bytes'
        return 0
    
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    def clear(self):
        'D.clear() -> None.  Remove all items from D.'
        pass
    
    def copy(self):
        'D.copy() -> a shallow copy of D'
        pass
    
    @classmethod
    def fromkeys(cls):
        'dict.fromkeys(S[,v]) -> New dict with keys from S and values equal to v.\nv defaults to None.'
        pass
    
    def get(self):
        'D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.'
        pass
    
    def has_key(self):
        'D.has_key(k) -> True if D has a key k, else False'
        pass
    
    def items(self):
        "D.items() -> list of D's (key, value) pairs, as 2-tuples"
        return list()
    
    def iteritems(self):
        'D.iteritems() -> an iterator over the (key, value) items of D'
        pass
    
    def iterkeys(self):
        'D.iterkeys() -> an iterator over the keys of D'
        pass
    
    def itervalues(self):
        'D.itervalues() -> an iterator over the values of D'
        pass
    
    def keys(self):
        "D.keys() -> list of D's keys"
        return list()
    
    def pop(self):
        'D.pop(k[,d]) -> v, remove specified key and return the corresponding value.\nIf key is not found, d is returned if given, otherwise KeyError is raised'
        pass
    
    def popitem(self):
        'D.popitem() -> (k, v), remove and return some (key, value) pair as a\n2-tuple; but raise KeyError if D is empty.'
        return tuple()
    
    def setdefault(self):
        'D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D'
        pass
    
    def update(self):
        'D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.\nIf E present and has a .keys() method, does:     for k in E: D[k] = E[k]\nIf E present and lacks .keys() method, does:     for (k, v) in E: D[k] = v\nIn either case, this is followed by: for k in F: D[k] = F[k]'
        pass
    
    def values(self):
        "D.values() -> list of D's values"
        return list()
    
    def viewitems(self):
        "D.viewitems() -> a set-like object providing a view on D's items"
        pass
    
    def viewkeys(self):
        "D.viewkeys() -> a set-like object providing a view on D's keys"
        pass
    
    def viewvalues(self):
        "D.viewvalues() -> an object providing a view on D's values"
        pass
    

ALERT_DESCRIPTION_ACCESS_DENIED = 49
ALERT_DESCRIPTION_BAD_CERTIFICATE = 42
ALERT_DESCRIPTION_BAD_CERTIFICATE_HASH_VALUE = 114
ALERT_DESCRIPTION_BAD_CERTIFICATE_STATUS_RESPONSE = 113
ALERT_DESCRIPTION_BAD_RECORD_MAC = 20
ALERT_DESCRIPTION_CERTIFICATE_EXPIRED = 45
ALERT_DESCRIPTION_CERTIFICATE_REVOKED = 44
ALERT_DESCRIPTION_CERTIFICATE_UNKNOWN = 46
ALERT_DESCRIPTION_CERTIFICATE_UNOBTAINABLE = 111
ALERT_DESCRIPTION_CLOSE_NOTIFY = 0
ALERT_DESCRIPTION_DECODE_ERROR = 50
ALERT_DESCRIPTION_DECOMPRESSION_FAILURE = 30
ALERT_DESCRIPTION_DECRYPT_ERROR = 51
ALERT_DESCRIPTION_HANDSHAKE_FAILURE = 40
ALERT_DESCRIPTION_ILLEGAL_PARAMETER = 47
ALERT_DESCRIPTION_INSUFFICIENT_SECURITY = 71
ALERT_DESCRIPTION_INTERNAL_ERROR = 80
ALERT_DESCRIPTION_NO_RENEGOTIATION = 100
ALERT_DESCRIPTION_PROTOCOL_VERSION = 70
ALERT_DESCRIPTION_RECORD_OVERFLOW = 22
ALERT_DESCRIPTION_UNEXPECTED_MESSAGE = 10
ALERT_DESCRIPTION_UNKNOWN_CA = 48
ALERT_DESCRIPTION_UNKNOWN_PSK_IDENTITY = 115
ALERT_DESCRIPTION_UNRECOGNIZED_NAME = 112
ALERT_DESCRIPTION_UNSUPPORTED_CERTIFICATE = 43
ALERT_DESCRIPTION_UNSUPPORTED_EXTENSION = 110
ALERT_DESCRIPTION_USER_CANCELLED = 90
CERT_NONE = 0
CERT_OPTIONAL = 1
CERT_REQUIRED = 2
HAS_ALPN = True
HAS_ECDH = True
HAS_NPN = True
HAS_SNI = True
HAS_TLS_UNIQUE = True
HAS_TLSv1_3 = False
OPENSSL_VERSION = 'OpenSSL 1.1.0g  2 Nov 2017'
OPENSSL_VERSION_INFO = tuple()
OPENSSL_VERSION_NUMBER = 269484159L
OP_ALL = 2147483732
OP_CIPHER_SERVER_PREFERENCE = 4194304
OP_NO_COMPRESSION = 131072
OP_NO_SSLv2 = 0
OP_NO_SSLv3 = 33554432
OP_NO_TLSv1 = 67108864
OP_NO_TLSv1_1 = 268435456
OP_NO_TLSv1_2 = 134217728
OP_NO_TLSv1_3 = 0
OP_SINGLE_DH_USE = 0
OP_SINGLE_ECDH_USE = 0
PROTOCOL_SSLv23 = 2
PROTOCOL_TLS = 2
PROTOCOL_TLSv1 = 3
PROTOCOL_TLSv1_1 = 4
PROTOCOL_TLSv1_2 = 5
def RAND_add(string, entropy):
    'RAND_add(string, entropy)\n\nMix string into the OpenSSL PRNG state.  entropy (a float) is a lower\nbound on the entropy contained in string.  See RFC 1750.'
    pass

def RAND_status():
    'RAND_status() -> 0 or 1\n\nReturns 1 if the OpenSSL PRNG has been seeded with enough data and 0 if not.\nIt is necessary to seed the PRNG with RAND_add() on some platforms before\nusing the ssl() function.'
    pass

class SSLEOFError(SSLError):
    'SSL/TLS connection terminated abruptly.'
    __class__ = SSLEOFError
    __dict__ = {}
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    __module__ = 'ssl'
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    

class SSLError(error):
    'An error occurred in the SSL implementation.'
    __class__ = SSLError
    __dict__ = {}
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    __module__ = 'ssl'
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    

class SSLSyscallError(SSLError):
    'System error when attempting SSL operation.'
    __class__ = SSLSyscallError
    __dict__ = {}
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    __module__ = 'ssl'
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    

class SSLWantReadError(SSLError):
    'Non-blocking SSL socket needs to read more data\nbefore the requested operation can be completed.'
    __class__ = SSLWantReadError
    __dict__ = {}
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    __module__ = 'ssl'
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    

class SSLWantWriteError(SSLError):
    'Non-blocking SSL socket needs to write more data\nbefore the requested operation can be completed.'
    __class__ = SSLWantWriteError
    __dict__ = {}
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    __module__ = 'ssl'
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    

class SSLZeroReturnError(SSLError):
    'SSL/TLS session closed cleanly.'
    __class__ = SSLZeroReturnError
    __dict__ = {}
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    __module__ = 'ssl'
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    

SSL_ERROR_EOF = 8
SSL_ERROR_INVALID_ERROR_CODE = 10
SSL_ERROR_SSL = 1
SSL_ERROR_SYSCALL = 5
SSL_ERROR_WANT_CONNECT = 7
SSL_ERROR_WANT_READ = 2
SSL_ERROR_WANT_WRITE = 3
SSL_ERROR_WANT_X509_LOOKUP = 4
SSL_ERROR_ZERO_RETURN = 6
VERIFY_CRL_CHECK_CHAIN = 12
VERIFY_CRL_CHECK_LEAF = 4
VERIFY_DEFAULT = 0
VERIFY_X509_STRICT = 32
VERIFY_X509_TRUSTED_FIRST = 32768
_OPENSSL_API_VERSION = tuple()
class _SSLContext(object):
    __class__ = _SSLContext
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    def _set_alpn_protocols(self):
        pass
    
    def _set_npn_protocols(self):
        pass
    
    def _wrap_socket(self):
        pass
    
    def cert_store_stats(self):
        "cert_store_stats() -> {'crl': int, 'x509_ca': int, 'x509': int}\n\nReturns quantities of loaded X.509 certificates. X.509 certificates with a\nCA extension and certificate revocation lists inside the context's cert\nstore.\nNOTE: Certificates in a capath directory aren't loaded unless they have\nbeen used at least once."
        pass
    
    @property
    def check_hostname(self):
        pass
    
    def get_ca_certs(self, binary_form=False):
        "get_ca_certs(binary_form=False) -> list of loaded certificate\n\nReturns a list of dicts with information of loaded CA certs. If the\noptional argument is True, returns a DER-encoded copy of the CA certificate.\nNOTE: Certificates in a capath directory aren't loaded unless they have\nbeen used at least once."
        return list()
    
    def load_cert_chain(self):
        pass
    
    def load_dh_params(self):
        pass
    
    def load_verify_locations(self):
        pass
    
    @property
    def options(self):
        pass
    
    def session_stats(self):
        pass
    
    def set_ciphers(self):
        pass
    
    def set_default_verify_paths(self):
        pass
    
    def set_ecdh_curve(self):
        pass
    
    def set_servername_callback(self, method):
        'set_servername_callback(method)\n\nThis sets a callback that will be called when a server name is provided by\nthe SSL/TLS client in the SNI extension.\n\nIf the argument is None then the callback is disabled. The method is called\nwith the SSLSocket, the server name as a string, and the SSLContext object.\nSee RFC 6066 for details of the SNI extension.'
        pass
    
    @property
    def verify_flags(self):
        pass
    
    @property
    def verify_mode(self):
        pass
    

class _SSLSocket(object):
    __class__ = _SSLSocket
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    def cipher(self):
        pass
    
    def compression(self):
        pass
    
    @property
    def context(self):
        '_setter_context(ctx)\nThis changes the context associated with the SSLSocket. This is typically\nused from within a callback function set by the set_servername_callback\non the SSLContext to change the certificate information associated with the\nSSLSocket before the cryptographic exchange handshake messages\n'
        pass
    
    def do_handshake(self):
        pass
    
    def peer_certificate(self, der=False):
        "peer_certificate([der=False]) -> certificate\n\nReturns the certificate for the peer.  If no certificate was provided,\nreturns None.  If a certificate was provided, but not validated, returns\nan empty dictionary.  Otherwise returns a dict containing information\nabout the peer certificate.\n\nIf the optional argument is True, returns a DER-encoded copy of the\npeer certificate, or None if no certificate was provided.  This will\nreturn the certificate even if it wasn't validated."
        pass
    
    def pending(self):
        'pending() -> count\n\nReturns the number of already decrypted bytes available for read,\npending on the connection.\n'
        pass
    
    def read(self, len=None):
        'read([len]) -> string\n\nRead up to len bytes from the SSL socket.'
        return ''
    
    def selected_alpn_protocol(self):
        pass
    
    def selected_npn_protocol(self):
        pass
    
    def shutdown(self, s):
        'shutdown(s) -> socket\n\nDoes the SSL shutdown handshake with the remote end, and returns\nthe underlying socket object.'
        pass
    
    def tls_unique_cb(self):
        "tls_unique_cb() -> bytes\n\nReturns the 'tls-unique' channel binding data, as defined by RFC 5929.\n\nIf the TLS handshake is not yet complete, None is returned"
        pass
    
    def version(self):
        pass
    
    def write(self, s):
        'write(s) -> len\n\nWrites the string s into the SSL object.  Returns the number\nof bytes written.'
        pass
    

__doc__ = 'Implementation module for SSL socket operations.  See the socket module\nfor documentation.'
__file__ = '/usr/lib/python2.7/lib-dynload/_ssl.x86_64-linux-gnu.so'
__name__ = '_ssl'
__package__ = None
def _test_decode_cert():
    pass

err_codes_to_names = dict()
err_names_to_codes = dict()
def get_default_verify_paths():
    "get_default_verify_paths() -> tuple\n\nReturn search paths and environment vars that are used by SSLContext's\nset_default_verify_paths() to load default CAs. The values are\n'cert_file_env', 'cert_file', 'cert_dir_env', 'cert_dir'."
    pass

lib_codes_to_names = dict()
def nid2obj(nid):
    'nid2obj(nid) -> (nid, shortname, longname, oid)\n\nLookup NID, short name, long name and OID of an ASN1_OBJECT by NID.'
    return tuple()

def txt2obj(txt, name=False):
    'txt2obj(txt, name=False) -> (nid, shortname, longname, oid)\n\nLookup NID, short name, long name and OID of an ASN1_OBJECT. By default\nobjects are looked up by OID. With name=True short and long name are also\nmatched.'
    return tuple()

