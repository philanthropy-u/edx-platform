class PyCapsule(object):
    'Capsule objects let you wrap a C "void *" pointer in a Python\nobject.  They\'re a way of passing data through the Python interpreter\nwithout creating your own custom type.\n\nCapsules are used for communication between extension modules.\nThey provide a way for an extension module to export a C interface\nto other extension modules, so that extension modules can use the\nPython import mechanism to link to one another.\n'
    __class__ = PyCapsule
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    def __repr__(self):
        'x.__repr__() <==> repr(x)'
        return ''
    
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    

AF_APPLETALK = 5
AF_ASH = 18
AF_ATMPVC = 8
AF_ATMSVC = 20
AF_AX25 = 3
AF_BLUETOOTH = 31
AF_BRIDGE = 7
AF_DECnet = 12
AF_ECONET = 19
AF_INET = 2
AF_INET6 = 10
AF_IPX = 4
AF_IRDA = 23
AF_KEY = 15
AF_LLC = 26
AF_NETBEUI = 13
AF_NETLINK = 16
AF_NETROM = 6
AF_PACKET = 17
AF_PPPOX = 24
AF_ROSE = 11
AF_ROUTE = 16
AF_SECURITY = 14
AF_SNA = 22
AF_TIPC = 30
AF_UNIX = 1
AF_UNSPEC = 0
AF_WANPIPE = 25
AF_X25 = 9
AI_ADDRCONFIG = 32
AI_ALL = 16
AI_CANONNAME = 2
AI_NUMERICHOST = 4
AI_NUMERICSERV = 1024
AI_PASSIVE = 1
AI_V4MAPPED = 8
BDADDR_ANY = '00:00:00:00:00:00'
BDADDR_LOCAL = '00:00:00:FF:FF:FF'
BTPROTO_HCI = 1
BTPROTO_L2CAP = 0
BTPROTO_RFCOMM = 3
BTPROTO_SCO = 2
CAPI = PyCapsule()
EAI_ADDRFAMILY = -9
EAI_AGAIN = -3
EAI_BADFLAGS = -1
EAI_FAIL = -4
EAI_FAMILY = -6
EAI_MEMORY = -10
EAI_NODATA = -5
EAI_NONAME = -2
EAI_OVERFLOW = -12
EAI_SERVICE = -8
EAI_SOCKTYPE = -7
EAI_SYSTEM = -11
HCI_DATA_DIR = 1
HCI_FILTER = 2
HCI_TIME_STAMP = 3
INADDR_ALLHOSTS_GROUP = 3758096385
INADDR_ANY = 0
INADDR_BROADCAST = 4294967295
INADDR_LOOPBACK = 2130706433
INADDR_MAX_LOCAL_GROUP = 3758096639
INADDR_NONE = 4294967295
INADDR_UNSPEC_GROUP = 3758096384
IPPORT_RESERVED = 1024
IPPORT_USERRESERVED = 5000
IPPROTO_AH = 51
IPPROTO_DSTOPTS = 60
IPPROTO_EGP = 8
IPPROTO_ESP = 50
IPPROTO_FRAGMENT = 44
IPPROTO_GRE = 47
IPPROTO_HOPOPTS = 0
IPPROTO_ICMP = 1
IPPROTO_ICMPV6 = 58
IPPROTO_IDP = 22
IPPROTO_IGMP = 2
IPPROTO_IP = 0
IPPROTO_IPIP = 4
IPPROTO_IPV6 = 41
IPPROTO_NONE = 59
IPPROTO_PIM = 103
IPPROTO_PUP = 12
IPPROTO_RAW = 255
IPPROTO_ROUTING = 43
IPPROTO_RSVP = 46
IPPROTO_TCP = 6
IPPROTO_TP = 29
IPPROTO_UDP = 17
IPV6_CHECKSUM = 7
IPV6_DONTFRAG = 62
IPV6_DSTOPTS = 59
IPV6_HOPLIMIT = 52
IPV6_HOPOPTS = 54
IPV6_JOIN_GROUP = 20
IPV6_LEAVE_GROUP = 21
IPV6_MULTICAST_HOPS = 18
IPV6_MULTICAST_IF = 17
IPV6_MULTICAST_LOOP = 19
IPV6_NEXTHOP = 9
IPV6_PATHMTU = 61
IPV6_PKTINFO = 50
IPV6_RECVDSTOPTS = 58
IPV6_RECVHOPLIMIT = 51
IPV6_RECVHOPOPTS = 53
IPV6_RECVPATHMTU = 60
IPV6_RECVPKTINFO = 49
IPV6_RECVRTHDR = 56
IPV6_RECVTCLASS = 66
IPV6_RTHDR = 57
IPV6_RTHDRDSTOPTS = 55
IPV6_RTHDR_TYPE_0 = 0
IPV6_TCLASS = 67
IPV6_UNICAST_HOPS = 16
IPV6_V6ONLY = 26
IP_ADD_MEMBERSHIP = 35
IP_DEFAULT_MULTICAST_LOOP = 1
IP_DEFAULT_MULTICAST_TTL = 1
IP_DROP_MEMBERSHIP = 36
IP_HDRINCL = 3
IP_MAX_MEMBERSHIPS = 20
IP_MULTICAST_IF = 32
IP_MULTICAST_LOOP = 34
IP_MULTICAST_TTL = 33
IP_OPTIONS = 4
IP_RECVOPTS = 6
IP_RECVRETOPTS = 7
IP_RETOPTS = 7
IP_TOS = 1
IP_TTL = 2
MSG_CTRUNC = 8
MSG_DONTROUTE = 4
MSG_DONTWAIT = 64
MSG_EOR = 128
MSG_OOB = 1
MSG_PEEK = 2
MSG_TRUNC = 32
MSG_WAITALL = 256
NETLINK_DNRTMSG = 14
NETLINK_FIREWALL = 3
NETLINK_IP6_FW = 13
NETLINK_NFLOG = 5
NETLINK_ROUTE = 0
NETLINK_USERSOCK = 2
NETLINK_XFRM = 6
NI_DGRAM = 16
NI_MAXHOST = 1025
NI_MAXSERV = 32
NI_NAMEREQD = 8
NI_NOFQDN = 4
NI_NUMERICHOST = 1
NI_NUMERICSERV = 2
PACKET_BROADCAST = 1
PACKET_FASTROUTE = 6
PACKET_HOST = 0
PACKET_LOOPBACK = 5
PACKET_MULTICAST = 2
PACKET_OTHERHOST = 3
PACKET_OUTGOING = 4
PF_PACKET = 17
SHUT_RD = 0
SHUT_RDWR = 2
SHUT_WR = 1
SOCK_DGRAM = 2
SOCK_RAW = 3
SOCK_RDM = 4
SOCK_SEQPACKET = 5
SOCK_STREAM = 1
SOL_HCI = 0
SOL_IP = 0
SOL_SOCKET = 1
SOL_TCP = 6
SOL_TIPC = 271
SOL_UDP = 17
SOMAXCONN = 128
SO_ACCEPTCONN = 30
SO_BROADCAST = 6
SO_DEBUG = 1
SO_DONTROUTE = 5
SO_ERROR = 4
SO_KEEPALIVE = 9
SO_LINGER = 13
SO_OOBINLINE = 10
SO_RCVBUF = 8
SO_RCVLOWAT = 18
SO_RCVTIMEO = 20
SO_REUSEADDR = 2
SO_REUSEPORT = 15
SO_SNDBUF = 7
SO_SNDLOWAT = 19
SO_SNDTIMEO = 21
SO_TYPE = 3
SocketType = socket()
TCP_CORK = 3
TCP_DEFER_ACCEPT = 9
TCP_INFO = 11
TCP_KEEPCNT = 6
TCP_KEEPIDLE = 4
TCP_KEEPINTVL = 5
TCP_LINGER2 = 8
TCP_MAXSEG = 2
TCP_NODELAY = 1
TCP_QUICKACK = 12
TCP_SYNCNT = 7
TCP_WINDOW_CLAMP = 10
TIPC_ADDR_ID = 3
TIPC_ADDR_NAME = 2
TIPC_ADDR_NAMESEQ = 1
TIPC_CFG_SRV = 0
TIPC_CLUSTER_SCOPE = 2
TIPC_CONN_TIMEOUT = 130
TIPC_CRITICAL_IMPORTANCE = 3
TIPC_DEST_DROPPABLE = 129
TIPC_HIGH_IMPORTANCE = 2
TIPC_IMPORTANCE = 127
TIPC_LOW_IMPORTANCE = 0
TIPC_MEDIUM_IMPORTANCE = 1
TIPC_NODE_SCOPE = 3
TIPC_PUBLISHED = 1
TIPC_SRC_DROPPABLE = 128
TIPC_SUBSCR_TIMEOUT = 3
TIPC_SUB_CANCEL = 4
TIPC_SUB_PORTS = 1
TIPC_SUB_SERVICE = 2
TIPC_TOP_SRV = 1
TIPC_WAIT_FOREVER = -1
TIPC_WITHDRAWN = 2
TIPC_ZONE_SCOPE = 1
__doc__ = 'Implementation module for socket operations.\n\nSee the socket module for documentation.'
__name__ = '_socket'
__package__ = None
class error(IOError):
    __class__ = error
    __dict__ = {}
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    __module__ = 'socket'
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    @property
    def __weakref__(self):
        'list of weak references to the object (if defined)'
        pass
    

def fromfd(fd, family, type, proto=None):
    'fromfd(fd, family, type[, proto]) -> socket object\n\nCreate a socket object from a duplicate of the given\nfile descriptor.\nThe remaining arguments are the same as for socket().'
    pass

class gaierror(error):
    __class__ = gaierror
    __dict__ = {}
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    __module__ = 'socket'
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    

def getaddrinfo(host, port, family=None, socktype=None, proto=None, flags=None):
    'getaddrinfo(host, port [, family, socktype, proto, flags])\n    -> list of (family, socktype, proto, canonname, sockaddr)\n\nResolve host and port into addrinfo struct.'
    pass

def getdefaulttimeout():
    'getdefaulttimeout() -> timeout\n\nReturns the default timeout in seconds (float) for new socket objects.\nA value of None indicates that new socket objects have no timeout.\nWhen the socket module is first imported, the default is None.'
    pass

def gethostbyaddr(host):
    'gethostbyaddr(host) -> (name, aliaslist, addresslist)\n\nReturn the true host name, a list of aliases, and a list of IP addresses,\nfor a host.  The host argument is a string giving a host name or IP number.'
    return tuple()

def gethostbyname(host):
    "gethostbyname(host) -> address\n\nReturn the IP address (a string of the form '255.255.255.255') for a host."
    pass

def gethostbyname_ex(host):
    'gethostbyname_ex(host) -> (name, aliaslist, addresslist)\n\nReturn the true host name, a list of aliases, and a list of IP addresses,\nfor a host.  The host argument is a string giving a host name or IP number.'
    return tuple()

def gethostname():
    'gethostname() -> string\n\nReturn the current host name.'
    return ''

def getnameinfo(sockaddr, flags):
    'getnameinfo(sockaddr, flags) --> (host, port)\n\nGet host and port for a sockaddr.'
    return tuple()

def getprotobyname(name):
    'getprotobyname(name) -> integer\n\nReturn the protocol number for the named protocol.  (Rarely used.)'
    return 1

def getservbyname(servicename, protocolname=None):
    "getservbyname(servicename[, protocolname]) -> integer\n\nReturn a port number from a service name and protocol name.\nThe optional protocol name, if given, should be 'tcp' or 'udp',\notherwise any protocol will match."
    return 1

def getservbyport(port, protocolname=None):
    "getservbyport(port[, protocolname]) -> string\n\nReturn the service name from a port number and protocol name.\nThe optional protocol name, if given, should be 'tcp' or 'udp',\notherwise any protocol will match."
    return ''

has_ipv6 = True
class herror(error):
    __class__ = herror
    __dict__ = {}
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    __module__ = 'socket'
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    

def htonl(integer):
    'htonl(integer) -> integer\n\nConvert a 32-bit integer from host to network byte order.'
    return 1

def htons(integer):
    'htons(integer) -> integer\n\nConvert a 16-bit integer from host to network byte order.'
    return 1

def inet_aton(string):
    'inet_aton(string) -> packed 32-bit IP representation\n\nConvert an IP address in string format (123.45.67.89) to the 32-bit packed\nbinary format used in low-level network functions.'
    pass

def inet_ntoa(packed_ip):
    'inet_ntoa(packed_ip) -> ip_address_string\n\nConvert an IP address from 32-bit packed binary format to string format'
    pass

def inet_ntop(af, packed_ip):
    'inet_ntop(af, packed_ip) -> string formatted IP address\n\nConvert a packed IP address of the given family to string format.'
    return ''

def inet_pton(af, ip):
    'inet_pton(af, ip) -> packed IP address string\n\nConvert an IP address from string format to a packed string suitable\nfor use with low-level network functions.'
    pass

def ntohl(integer):
    'ntohl(integer) -> integer\n\nConvert a 32-bit integer from network to host byte order.'
    return 1

def ntohs(integer):
    'ntohs(integer) -> integer\n\nConvert a 16-bit integer from network to host byte order.'
    return 1

def setdefaulttimeout(timeout):
    'setdefaulttimeout(timeout)\n\nSet the default timeout in seconds (float) for new socket objects.\nA value of None indicates that new socket objects have no timeout.\nWhen the socket module is first imported, the default is None.'
    pass

class socket(object):
    "socket([family[, type[, proto]]]) -> socket object\n\nOpen a socket of the given type.  The family argument specifies the\naddress family; it defaults to AF_INET.  The type argument specifies\nwhether this is a stream (SOCK_STREAM, this is the default)\nor datagram (SOCK_DGRAM) socket.  The protocol argument defaults to 0,\nspecifying the default protocol.  Keyword arguments are accepted.\n\nA socket object represents one endpoint of a network connection.\n\nMethods of socket objects (keyword arguments not allowed):\n\naccept() -- accept a connection, returning new socket and client address\nbind(addr) -- bind the socket to a local address\nclose() -- close the socket\nconnect(addr) -- connect the socket to a remote address\nconnect_ex(addr) -- connect, return an error code instead of an exception\ndup() -- return a new socket object identical to the current one [*]\nfileno() -- return underlying file descriptor\ngetpeername() -- return remote address [*]\ngetsockname() -- return local address\ngetsockopt(level, optname[, buflen]) -- get socket options\ngettimeout() -- return timeout or None\nlisten(n) -- start listening for incoming connections\nmakefile([mode, [bufsize]]) -- return a file object for the socket [*]\nrecv(buflen[, flags]) -- receive data\nrecv_into(buffer[, nbytes[, flags]]) -- receive data (into a buffer)\nrecvfrom(buflen[, flags]) -- receive data and sender's address\nrecvfrom_into(buffer[, nbytes, [, flags])\n  -- receive data and sender's address (into a buffer)\nsendall(data[, flags]) -- send all data\nsend(data[, flags]) -- send data, may not send all of it\nsendto(data[, flags], addr) -- send data to a given address\nsetblocking(0 | 1) -- set or clear the blocking I/O flag\nsetsockopt(level, optname, value) -- set socket options\nsettimeout(None | float) -- set or clear the timeout\nshutdown(how) -- shut down traffic in one or both directions\n\n [*] not available on all platforms!"
    __class__ = socket
    def __getattribute__(self):
        "x.__getattribute__('name') <==> x.name"
        pass
    
    def __init__(self, family=None, type=None, proto=None):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    def __repr__(self):
        'x.__repr__() <==> repr(x)'
        return ''
    
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    def accept(self):
        'accept() -> (socket object, address info)\n\nWait for an incoming connection.  Return a new socket representing the\nconnection, and the address of the client.  For IP sockets, the address\ninfo is a pair (hostaddr, port).'
        return tuple()
    
    def bind(self, address):
        'bind(address)\n\nBind the socket to a local address.  For IP sockets, the address is a\npair (host, port); the host must refer to the local host. For raw packet\nsockets the address is a tuple (ifname, proto [,pkttype [,hatype]])'
        pass
    
    def close(self):
        'close()\n\nClose the socket.  It cannot be used after this call.'
        pass
    
    def connect(self, address):
        'connect(address)\n\nConnect the socket to a remote address.  For IP sockets, the address\nis a pair (host, port).'
        pass
    
    def connect_ex(self, address):
        'connect_ex(address) -> errno\n\nThis is like connect(address), but returns an error code (the errno value)\ninstead of raising an exception when an error occurs.'
        pass
    
    def dup(self):
        'dup() -> socket object\n\nReturn a new socket object connected to the same system resource.'
        pass
    
    @property
    def family(self):
        'the socket family'
        pass
    
    def fileno(self):
        'fileno() -> integer\n\nReturn the integer file descriptor of the socket.'
        return 1
    
    def getpeername(self):
        'getpeername() -> address info\n\nReturn the address of the remote endpoint.  For IP sockets, the address\ninfo is a pair (hostaddr, port).'
        pass
    
    def getsockname(self):
        'getsockname() -> address info\n\nReturn the address of the local endpoint.  For IP sockets, the address\ninfo is a pair (hostaddr, port).'
        pass
    
    def getsockopt(self, level, option, buffersize=None):
        'getsockopt(level, option[, buffersize]) -> value\n\nGet a socket option.  See the Unix manual for level and option.\nIf a nonzero buffersize argument is given, the return value is a\nstring of that length; otherwise it is an integer.'
        pass
    
    def gettimeout(self):
        'gettimeout() -> timeout\n\nReturns the timeout in seconds (float) associated with socket \noperations. A timeout of None indicates that timeouts on socket \noperations are disabled.'
        pass
    
    def listen(self, backlog):
        'listen(backlog)\n\nEnable a server to accept connections.  The backlog argument must be at\nleast 0 (if it is lower, it is set to 0); it specifies the number of\nunaccepted connections that the system will allow before refusing new\nconnections.'
        pass
    
    def makefile(self, mode=None, buffersize=None):
        'makefile([mode[, buffersize]]) -> file object\n\nReturn a regular file object corresponding to the socket.\nThe mode and buffersize arguments are as for the built-in open() function.'
        pass
    
    @property
    def proto(self):
        'the socket protocol'
        pass
    
    def recv(self, buffersize, flags=None):
        'recv(buffersize[, flags]) -> data\n\nReceive up to buffersize bytes from the socket.  For the optional flags\nargument, see the Unix manual.  When no data is available, block until\nat least one byte is available or until the remote end is closed.  When\nthe remote end is closed and all data is read, return the empty string.'
        pass
    
    def recv_into(self, buffer, nbytes=None, flags=None):
        'recv_into(buffer, [nbytes[, flags]]) -> nbytes_read\n\nA version of recv() that stores its data into a buffer rather than creating \na new string.  Receive up to buffersize bytes from the socket.  If buffersize \nis not specified (or 0), receive up to the size available in the given buffer.\n\nSee recv() for documentation about the flags.'
        pass
    
    def recvfrom(self, buffersize, flags=None):
        "recvfrom(buffersize[, flags]) -> (data, address info)\n\nLike recv(buffersize, flags) but also return the sender's address info."
        return tuple()
    
    def recvfrom_into(self, buffer, nbytes=None, flags=None):
        "recvfrom_into(buffer[, nbytes[, flags]]) -> (nbytes, address info)\n\nLike recv_into(buffer[, nbytes[, flags]]) but also return the sender's address info."
        return tuple()
    
    def send(self, data, flags=None):
        'send(data[, flags]) -> count\n\nSend a data string to the socket.  For the optional flags\nargument, see the Unix manual.  Return the number of bytes\nsent; this may be less than len(data) if the network is busy.'
        pass
    
    def sendall(self, data, flags=None):
        "sendall(data[, flags])\n\nSend a data string to the socket.  For the optional flags\nargument, see the Unix manual.  This calls send() repeatedly\nuntil all data is sent.  If an error occurs, it's impossible\nto tell how much data has been sent."
        pass
    
    def sendto(self, data, flags=None, address=None):
        'sendto(data[, flags], address) -> count\n\nLike send(data, flags) but allows specifying the destination address.\nFor IP sockets, the address is a pair (hostaddr, port).'
        pass
    
    def setblocking(self, flag):
        'setblocking(flag)\n\nSet the socket to blocking (flag is true) or non-blocking (false).\nsetblocking(True) is equivalent to settimeout(None);\nsetblocking(False) is equivalent to settimeout(0.0).'
        pass
    
    def setsockopt(self, level, option, value):
        'setsockopt(level, option, value)\n\nSet a socket option.  See the Unix manual for level and option.\nThe value argument can either be an integer or a string.'
        pass
    
    def settimeout(self, timeout):
        "settimeout(timeout)\n\nSet a timeout on socket operations.  'timeout' can be a float,\ngiving in seconds, or None.  Setting a timeout of None disables\nthe timeout feature and is equivalent to setblocking(1).\nSetting a timeout of zero is the same as setblocking(0)."
        pass
    
    def shutdown(self, flag):
        'shutdown(flag)\n\nShut down the reading side of the socket (flag == SHUT_RD), the writing side\nof the socket (flag == SHUT_WR), or both ends (flag == SHUT_RDWR).'
        pass
    
    @property
    def timeout(self):
        'the socket timeout'
        pass
    
    @property
    def type(self):
        'the socket type'
        pass
    

def socketpair(family=None, type=None, proto=None):
    'socketpair([family[, type[, proto]]]) -> (socket object, socket object)\n\nCreate a pair of socket objects from the sockets returned by the platform\nsocketpair() function.\nThe arguments are the same as for socket() except the default family is\nAF_UNIX if defined on the platform; otherwise, the default is AF_INET.'
    return tuple()

class timeout(error):
    __class__ = timeout
    __dict__ = {}
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    __module__ = 'socket'
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    

