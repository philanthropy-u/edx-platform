import __builtin__ as _mod___builtin__
import exceptions as _mod_exceptions

CLASSMETHOD_TYPES = _mod___builtin__.tuple()
CLASS_MEMBER_SUBSTITUTE = _mod___builtin__.dict()
EXACT_TOKEN_TYPES = _mod___builtin__.dict()
EXCLUDED_MEMBERS = _mod___builtin__.tuple()
IMPLICIT_CLASSMETHOD = _mod___builtin__.tuple()
INVALID_ARGNAMES = _mod___builtin__.set()
class InspectWarning(_mod_exceptions.UserWarning):
    __class__ = InspectWarning
    __dict__ = {}
    def __init__(self):
        'x.__init__(...) initializes x; see help(type(x)) for signature'
        pass
    
    __module__ = '__main__'
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    @property
    def __weakref__(self):
        'list of weak references to the object (if defined)'
        pass
    

LIES_ABOUT_MODULE = _mod___builtin__.frozenset()
MODULE_MEMBER_SUBSTITUTE = _mod___builtin__.dict()
class MemberInfo(_mod___builtin__.object):
    NO_VALUE = _mod___builtin__.object()
    __class__ = MemberInfo
    __dict__ = {}
    def __init__(self, name, value, literal, scope, module, alias, module_doc, scope_alias):
        pass
    
    __module__ = '__main__'
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    @property
    def __weakref__(self):
        'list of weak references to the object (if defined)'
        pass
    
    def _collect_bases(self, value_type, module, type_name):
        pass
    
    def _get_typename(self, cls, value_type, in_module):
        pass
    
    def _lines_with_members(self):
        pass
    
    def _lines_with_signature(self):
        pass
    
    def _str_from_literal(self, lit):
        pass
    
    def _str_from_typename(self, type_name):
        pass
    
    def _str_from_value(self, v):
        pass
    
    def as_str(self, indent):
        pass
    

PROPERTY_TYPES = _mod___builtin__.tuple()
SKIP_TYPENAME_FOR_TYPES = _mod___builtin__.tuple()
STATICMETHOD_TYPES = _mod___builtin__.tuple()
SYS_INFO_TYPES = _mod___builtin__.frozenset()
class ScrapeState(_mod___builtin__.object):
    __class__ = ScrapeState
    __dict__ = {}
    def __init__(self, module_name, module):
        pass
    
    __module__ = '__main__'
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    @property
    def __weakref__(self):
        'list of weak references to the object (if defined)'
        pass
    
    def _collect_members(self, mod, members, substitutes, outer_member):
        'Fills the members attribute with a dictionary containing\n        all members from the module.'
        pass
    
    def _mro_contains(self, mro, name, value):
        pass
    
    def _should_add_value(self, value):
        pass
    
    def _should_collect_members(self, member):
        pass
    
    def collect_second_level_members(self):
        pass
    
    def collect_top_level_members(self):
        pass
    
    def dump(self, out):
        pass
    
    def initial_import(self, search_path):
        pass
    
    def translate_members(self):
        pass
    

class Signature(_mod___builtin__.object):
    KNOWN_ARGSPECS = _mod___builtin__.dict()
    KNOWN_RESTYPES = _mod___builtin__.dict()
    _PAREN_TOKEN_MAP = _mod___builtin__.dict()
    __class__ = Signature
    __dict__ = {}
    def __init__(self, name, callable, scope, defaults, scope_alias, decorators, module_doc):
        pass
    
    __module__ = '__main__'
    def __str__(self):
        return ''
    
    @classmethod
    def __subclasshook__(cls, subclass):
        'Abstract classes can override this to customize issubclass().\n\nThis is invoked early on by abc.ABCMeta.__subclasscheck__().\nIt should return True, False or NotImplemented.  If it returns\nNotImplemented, the normal algorithm is used.  Otherwise, it\noverrides the normal algorithm (and the outcome is cached).\n'
        return False
    
    @property
    def __weakref__(self):
        'list of weak references to the object (if defined)'
        pass
    
    def _can_eval(self, s):
        pass
    
    def _get_first_function_call(self, expr):
        'Scans the string for the first closing parenthesis,\n        handling nesting, which is the best heuristic we have for\n        an example call at the start of the docstring.'
        pass
    
    def _init_argspec_fromargspec(self, defaults):
        pass
    
    def _init_argspec_fromdocstring(self, defaults, doc, override_name):
        pass
    
    def _init_argspec_fromknown(self, defaults, scope_alias):
        pass
    
    def _init_argspec_fromsignature(self, defaults):
        pass
    
    def _init_restype_fromdocstring(self):
        pass
    
    def _init_restype_fromknown(self, scope_alias):
        pass
    
    def _init_restype_fromsignature(self):
        pass
    
    def _make_unique_name(self, name, seen_names):
        pass
    
    def _parse_format_arg(self, name, args, defaults):
        pass
    
    def _parse_funcdef(self, expr, allow_name_mismatch, defaults, override_name):
        'Takes a call expression that was part of a docstring\n        and parses the AST as if it were a definition. If the parsed\n        AST matches the callable we are wrapping, returns the node.\n        '
        pass
    
    def _parse_take_expr(self, tokens, *stop_at):
        pass
    
    def _tokenize(self, expr):
        pass
    

VALUE_REPR_FIX = _mod___builtin__.dict()
__author__ = 'Microsoft Corporation <ptvshelp@microsoft.com>'
__builtins__ = {}
__doc__ = None
__file__ = '/home/danial/.vscode/extensions/ms-python.python-2019.5.18875/languageServer.0.2.96/scrape_module.py'
__name__ = '__main__'
__package__ = None
__version__ = '15.8'
__warningregistry__ = _mod___builtin__.dict()
def _triple_quote(s):
    pass

def add_builtin_objects(state):
    pass

def do_not_inspect(v):
    pass

outfile = _mod___builtin__.file()
print_function = _mod___builtin__.instance()
def safe_callable(v):
    pass

def safe_module_name(n):
    pass

state = ScrapeState()
