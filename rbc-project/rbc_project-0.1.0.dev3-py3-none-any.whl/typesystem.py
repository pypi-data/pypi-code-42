"""Provides Type structures.
"""
# Author: Pearu Peterson
# Created: February 2019


import re
import ctypes
import inspect
try:
    import numba as nb
    import numba.typing.ctypes_utils
except ImportError as msg:
    nb = None
    nb_NA_message = str(msg)


class TypeParseError(Exception):
    """Failure to parse type definition
    """


class TargetInfo(object):
    """Base class for determining various information about the target
    system.

    """

    def __init__(self, strict=False):
        """
        Parameters
        ----------
        strict: bool
          When True, require that atomic types are concrete. If not,
          raise an exception.
        """
        self.strict = strict
        self.custom_type_converters = []

    def sizeof(self, t):
        """Return the sizeof(t) value in the target system.

        Parameters
        ----------
        t : {str, ...}
            Specify types name. For a full support, one should
            implement the sizeof for the following type names: char,
            uchar, schar, byte, ubyte, short, ushort, int, uint, long,
            ulong, longlong, ulonglong, float, double, longdouble,
            complex, bool, size_t, ssize_t. wchar
        """
        raise NotImplementedError("%s.sizeof(%r)"
                                  % (type(self).__name__, t))

    def add_converter(self, converter):
        """Add custom type converter.

        Custom type converters are called on non-concrete atomic
        types.

        Parameters
        ----------
        converter : callable
          Specify a function with signature `converter(target_info,
          obj)` that returns `Type` instance corresponding to
          `obj`. If the conversion is unsuccesful, the `converter`
          returns `None` so that other converter functions could be
          tried.

        """
        self.custom_type_converters.append(converter)

    def custom_type(self, t):
        """Return custom type of an object.
        """
        for converter in self.custom_type_converters:
            r = converter(self, t)
            if r is not None:
                return r


class LocalTargetInfo(TargetInfo):
    """Uses ctypes to determine the type info in a local system.

    """
    def sizeof(self, t):
        if isinstance(t, str):
            if t == 'complex':
                return 2 * self.sizeof('float')
            ct = dict(
                bool=ctypes.c_bool,

                size_t=ctypes.c_size_t,
                ssize_t=ctypes.c_ssize_t,

                char=ctypes.c_char,
                uchar=ctypes.c_char,
                schar=ctypes.c_char,
                byte=ctypes.c_byte,
                ubyte=ctypes.c_ubyte,

                wchar=ctypes.c_wchar,

                short=ctypes.c_short,
                ushort=ctypes.c_ushort,

                int=ctypes.c_int,
                uint=ctypes.c_uint,

                long=ctypes.c_long,
                ulong=ctypes.c_ulong,

                longlong=ctypes.c_longlong,
                ulonglong=ctypes.c_ulonglong,

                float=ctypes.c_float,
                double=ctypes.c_double,
                longdouble=ctypes.c_longdouble,
            ).get(t)
            if ct is not None:
                return ctypes.sizeof(ct)
        return super(LocalTargetInfo, self).sizeof(t)


def _findparen(s):
    """Find the index of left parenthesis that matches with the one at the
    end of a string.

    Used internally.
    """
    j = s.find(')')
    assert j >= 0, repr((j, s))
    if j == len(s) - 1:
        i = s.find('(')
        if i < 0:
            raise TypeParseError('failed to find lparen index in `%s`' % s)
        return i
    i = s.rfind('(', 0, j)
    if i < 0:
        raise TypeParseError('failed to find lparen index in `%s`' % s)
    t = s[:i] + '_'*(j-i+1) + s[j+1:]
    assert len(t) == len(s), repr((t, s))
    return _findparen(t)


def _commasplit(s):
    """Split a comma-separated items taking into account parenthesis.

    Used internally.
    """
    lst = s.split(',')
    ac = ''
    p1, p2 = 0, 0
    rlst = []
    for i in lst:
        p1 += i.count('(') - i.count(')')
        p2 += i.count('{') - i.count('}')
        if p1 == p2 == 0:
            rlst.append((ac + ',' + i if ac else i).strip())
            ac = ''
        else:
            ac = ac + ',' + i if ac else i
    if p1 == p2 == 0:
        return rlst
    raise TypeParseError('failed to comma-split `%s`' % s)


_charn_match = re.compile(r'\A(char)(32|16|8)(_t|)\Z').match
_intn_match = re.compile(r'\A(signed\s*int|int|i)(\d+)(_t|)\Z').match
_uintn_match = re.compile(r'\A(unsigned\s*int|uint|u)(\d+)(_t|)\Z').match
_floatn_match = re.compile(r'\A(float|f)(16|32|64|128|256)(_t|)\Z').match
_complexn_match = re.compile(
    r'\A(complex|c)(16|32|64|128|256|512)(_t|)\Z').match

_bool_match = re.compile(r'\A(boolean|bool|_Bool|b)\Z').match
_string_match = re.compile(r'\A(string|str)\Z').match

_char_match = re.compile(r'\A(char)\Z').match
_schar_match = re.compile(r'\A(signed\s*char)\Z').match
_uchar_match = re.compile(r'\A(unsigned\s*char|uchar)\Z').match
_byte_match = re.compile(r'\A(signed\s*byte|byte)\Z').match
_ubyte_match = re.compile(r'\A(unsigned\s*byte|ubyte)\Z').match
_wchar_match = re.compile(r'\A(wchar)(_t|)\Z').match

_short_match = re.compile(
    r'\A(signed\s*short\s*int|signed\s*short|short\s*int|short)\Z').match
_ushort_match = re.compile(
    r'\A(unsigned\s*short\s*int|unsigned\s*short|ushort)\Z').match

_int_match = re.compile(r'\A(signed\s*int|signed|int|i)\Z').match
_uint_match = re.compile(r'\A(unsigned\s*int|unsigned|uint|u)\Z').match

_long_match = re.compile(
    r'\A(signed\s*long\s*int|signed\s*long|long\s*int|long|l)\Z').match
_ulong_match = re.compile(
    r'\A(unsigned\s*long\s*int|unsigned\s*long|ulong)\Z').match

_longlong_match = re.compile(
    r'\A(signed\s*long\s*long\s*int|signed\s*long\s*long|long\s*long'
    r'\s*int|long\s*long)\Z').match
_ulonglong_match = re.compile(
    r'\A(unsigned\s*long\s*long\s*int|unsigned\s*long\s*long)\Z'
).match

_size_t_match = re.compile(r'\A(std::|c_|)size_t\Z').match
_ssize_t_match = re.compile(r'\A(std::|c_|)ssize_t\Z').match

_float_match = re.compile(r'\A(float|f)\Z').match
_double_match = re.compile(r'\A(double|d)\Z').match
_longdouble_match = re.compile(r'\A(long\s*double)\Z').match

_complex_match = re.compile(r'\A(complex|c)\Z').match


# For `Type.fromstring('<typespec> <name>')` support:
_type_name_match = re.compile(r'\A(.*)\s(\w+)\Z').match
# bad names are the names of types that can have modifiers such as
# `signed`, `unsigned`, `long`, etc.:
_bad_names_match = re.compile(r'\A(char|byte|short|int|long|double)\Z').match


class Complex64(ctypes.Structure):
    _fields_ = [("real", ctypes.c_float), ("imag", ctypes.c_float)]

    @classmethod
    def from_param(cls, obj):
        if isinstance(obj, complex):
            return cls(obj.real, obj.imag)
        if isinstance(obj, (int, float)):
            return cls(obj.real, 0.0)
        raise NotImplementedError(repr(type(obj)))


class Complex128(ctypes.Structure):
    _fields_ = [("real", ctypes.c_double), ("imag", ctypes.c_double)]

    @classmethod
    def from_param(cls, obj):
        if isinstance(obj, complex):
            return cls(obj.real, obj.imag)
        if isinstance(obj, (int, float)):
            return cls(obj.real, 0.0)
        raise NotImplementedError(repr(type(obj)))

    def topython(self):
        return complex(self.real, self.imag)


# Initialize type maps
_ctypes_imap = {
    ctypes.c_void_p: 'void*', None: 'void', ctypes.c_bool: 'bool',
    ctypes.c_char_p: 'char%s*' % (ctypes.sizeof(ctypes.c_char()) * 8),
    ctypes.c_wchar_p: 'char%s*' % (ctypes.sizeof(ctypes.c_wchar()) * 8),
}
_ctypes_char_map = {}
_ctypes_int_map = {}
_ctypes_uint_map = {}
_ctypes_float_map = {}
_ctypes_complex_map = {}
for _k, _m, _lst in [
        ('char', _ctypes_char_map, ['c_char', 'c_wchar']),
        ('int', _ctypes_int_map,
         ['c_int8', 'c_int16', 'c_int32', 'c_int64', 'c_int',
          'c_long', 'c_longlong', 'c_byte', 'c_short', 'c_ssize_t']),
        ('uint', _ctypes_uint_map,
         ['c_uint8', 'c_uint16', 'c_uint32', 'c_uint64', 'c_uint',
          'c_ulong', 'c_ulonglong', 'c_ubyte', 'c_ushort', 'c_size_t']),
        ('float', _ctypes_float_map,
         ['c_float', 'c_double', 'c_longdouble']),
        ('complex', _ctypes_complex_map,
         [Complex64, Complex128])
]:
    for _n in _lst:
        if isinstance(_n, str):
            _t = getattr(ctypes, _n, None)
        else:
            _t = _n
        if _t is not None:
            _b = ctypes.sizeof(_t) * 8
            if _b not in _m:
                _m[_b] = _t
            _ctypes_imap[_t] = _k + str(_b)

if nb is not None:
    _numba_imap = {nb.void: 'void', nb.boolean: 'bool'}
    _numba_char_map = {}
    _numba_int_map = {}
    _numba_uint_map = {}
    _numba_float_map = {}
    _numba_complex_map = {}
    for _k, _m, _lst in [
            ('int', _numba_int_map,
             ['int8', 'int16', 'int32', 'int64', 'intc', 'int_', 'intp',
              'long_', 'longlong', 'short', 'char']),
            ('uint', _numba_uint_map,
             ['uint8', 'uint16', 'uint32', 'uint64', 'uintc', 'uint',
              'uintp', 'ulong', 'ulonglong', 'ushort']),
            ('float', _numba_float_map,
             ['float32', 'float64', 'float_', 'double']),
            ('complex', _numba_complex_map, ['complex64', 'complex128']),
    ]:
        for _n in _lst:
            _t = getattr(nb, _n, None)
            if _t is not None:
                _b = _t.bitwidth
                if _b not in _m:
                    _m[_b] = _t
                _numba_imap[_t] = _k + str(_b)

# python_imap values must be processed with Type.fromstring
_python_imap = {int: 'int64', float: 'float64', complex: 'complex128',
                str: 'string', bytes: 'char*'}

# Data for the mangling algorithm, see mangle/demangle methods.
#
_mangling_suffices = '_V'
_mangling_prefixes = 'PKaA'
_mangling_map = dict(
    void='v', bool='b',
    char8='c', char16='z', char32='w',
    int8='B', int16='s', int32='i', int64='l', int128='q',
    uint8='U', uint16='S', uint32='I', uint64='L', uint128='Q',
    float16='h', float32='f', float64='d', float128='x',
    complex32='H', complex64='F', complex128='D', complex256='X',
    string='t',
)
_mangling_imap = {}
for _k, _v in _mangling_map.items():
    assert _v not in _mangling_imap, repr((_k, _v))
    assert len(_v) == 1, repr((_k, _v))
    _mangling_imap[_v] = _k
# make sure that mangling keys will not conflict with mangling
# operators:
_i = set(_mangling_imap).intersection(_mangling_suffices+_mangling_prefixes)
assert not _i, repr(_i)


class Type(tuple):
    """Represents a type.

    There are five kinds of a types:

      void        - a "no type"
      atomic      e.g. `int32`
      pointer     e.g. `int32*`
      struct      e.g. `{int32, int32}`
      function    e.g. `int32(int32, int32)`

    Atomic types are types with names (Type contains a single
    string). All other types (except "no type") are certain
    constructions of atomic types.

    The name content of an atomic type is arbitrary but it cannot be
    empty. For instance, Type('a') and Type('a long name') are atomic
    types.

    Parsing types from a string is not fixed to any type system, the
    names of types can be arbitrary.  However, converting the Type
    instances to concrete types such as provided in numpy or numba,
    the following atomic types are defined (the first name corresponds
    to normalized name):

      no type:                    void, none
      bool:                       bool, boolean, _Bool, b
      8-bit char:                 char8, char
      16-bit char:                char16
      32-bit char:                char32, wchar
      8-bit signed integer:       int8, i8, byte, signed char
      16-bit signed integer:      int16, i16, int16_t
      32-bit signed integer:      int32, i32, int32_t
      64-bit signed integer:      int64, i64, int64_t
      128-bit signed integer:     int128, i128, int128_t
      8-bit unsigned integer:     uint8, u8, ubyte, unsigned char
      16-bit unsigned integer:    uint16, u16, uint16_t
      32-bit unsigned integer:    uint32, u32, uint32_t
      64-bit unsigned integer:    uint64, u64, uint64_t
      128-bit unsigned integer:   uint128, u128, uint64_t
      16-bit float:               float16, f16
      32-bit float:               float32, f32, float
      64-bit float:               float64, f64, double
      128-bit float:              float128, f128, long double
      32-bit complex:             complex32, c32, complex
      64-bit complex:             complex64, c64
      128-bit complex:            complex128, c128
      256-bit complex:            complex256, c256
      string:                     string, str

    with the following extensions:

      N-bit signed integer: int<N>, i<N>       for instance: int5, i31
      N-bit unsigned integer: uint<N>, u<N>
      N-bit float: float<N>
      N-bit complex: complex<N>

    Also byte, short, int, long, long long, signed int, size_t,
    ssize_t, etc are supported but their normalized names are system
    dependent.
    """

    _mangling = None

    def __new__(cls, *args, **params):
        obj = tuple.__new__(cls, args)
        if not obj._is_ok:
            raise ValueError(
                'attempt to create an invalid Type object from `%s`' % (args,))
        obj._params = params
        return obj

    def set_mangling(self, mangling):
        """Set mangling string of the type.
        """
        self._mangling = mangling

    @property
    def mangling(self):
        if self._mangling is None:
            self._mangling = self.mangle()
        return self._mangling

    @property
    def is_void(self):
        return len(self) == 0

    @property
    def is_atomic(self):
        return len(self) == 1 and isinstance(self[0], str)

    @property
    def is_int(self):
        return self.is_atomic and self[0].startswith('int')

    @property
    def is_uint(self):
        return self.is_atomic and self[0].startswith('uint')

    @property
    def is_float(self):
        return self.is_atomic and self[0].startswith('float')

    @property
    def is_complex(self):
        return self.is_atomic and self[0].startswith('complex')

    @property
    def is_string(self):
        return self.is_atomic and self[0] == 'string'

    @property
    def is_bool(self):
        return self.is_atomic and self[0] == 'bool'

    @property
    def is_char(self):
        return self.is_atomic and self[0].startswith('char')

    @property
    def is_pointer(self):
        return len(self) == 2 and isinstance(self[0], Type) \
            and isinstance(self[1], str) and self[1] == '*'

    @property
    def is_struct(self):
        return len(self) > 0 and all(isinstance(s, Type) for s in self)

    @property
    def is_function(self):
        return len(self) == 2 and isinstance(self[0], Type) and \
            isinstance(self[1], tuple) and not isinstance(self[1], Type)

    @property
    def is_complete(self):
        """Return True when the Type instance does not contain unknown types.
        """
        if self.is_atomic:
            return not self[0].startswith('<type of')
        elif self.is_pointer:
            return self[0].is_complete
        elif self.is_struct:
            for m in self:
                if not m.complete:
                    return False
        elif self.is_function:
            if not self[0].is_complete:
                return False
            for a in self[1]:
                if not a.is_complete:
                    return False
        elif self.is_void:
            pass
        else:
            raise NotImplementedError(repr(self))
        return True

    @property
    def _is_ok(self):
        return self.is_void or self.is_atomic or self.is_pointer \
            or self.is_struct or (self.is_function and len(self[1]) > 0)

    def __repr__(self):
        return '%s%s' % (type(self).__name__, tuple.__repr__(self))

    def __str__(self):
        if self._is_ok:
            return self.tostring()
        return tuple.__str__(self)

    def tostring(self, use_typename=False):
        """Return string representation of a type.
        """
        if self.is_void:
            return 'void'
        name = self._params.get('name')
        if name is not None:
            suffix = ' ' + name
        else:
            suffix = ''
        if use_typename:
            typename = self._params.get('typename')
            if typename is not None:
                return typename + suffix
        if self.is_atomic:
            return self[0] + suffix
        if self.is_pointer:
            return self[0].tostring(use_typename=use_typename) + '*' + suffix
        if self.is_struct:
            return '{' + ', '.join([t.tostring(use_typename=use_typename)
                                    for t in self]) + '}' + suffix
        if self.is_function:
            return (self[0].tostring(use_typename=use_typename)
                    + '(' + ', '.join(
                        a.tostring(use_typename=use_typename)
                        for a in self[1]) + ')' + suffix)
        raise NotImplementedError(repr(self))

    def toprototype(self):
        if self.is_void:
            return 'void'
        typename = self._params.get('typename')
        if typename is not None:
            return typename
        if self.is_atomic:
            s = self[0]
            if self.is_int or self.is_uint:
                return s + '_t'
            if self.is_float:
                bits = self.bits
                if bits == 32:
                    return 'float'
                elif bits == 64:
                    return 'double'
            return s
        if self.is_pointer:
            return self[0].toprototype() + '*'
        if self.is_struct:
            return '{' + ', '.join([t.toprototype() for t in self]) + '}'
        if self.is_function:
            return self[0].toprototype() + '(' + ', '.join(
                a.toprototype() for a in self[1]) + ')'
        raise NotImplementedError(repr(self))

    def tonumba(self, bool_is_int8=None):
        """Convert Type instance to numba type object.

        Parameters
        ----------
        bool_is_int8: {bool, None}

          If true, boolean data and values are mapped to LLVM `i8`,
          otherwise to `i1`. Note that numba boolean maps data to `i8`
          and value to `i1`. To get numba convention, specify
          `bool_is_int8` as `None`.

        """
        numba_type = self._params.get('tonumba')
        if numba_type is not None:
            return numba_type
        if self.is_void:
            return nb.void
        if self.is_int:
            return _numba_int_map.get(int(self[0][3:]))
        if self.is_uint:
            return _numba_uint_map.get(int(self[0][4:]))
        if self.is_float:
            return _numba_float_map.get(int(self[0][5:]))
        if self.is_complex:
            return _numba_complex_map.get(int(self[0][7:]))
        if self.is_bool:
            if bool_is_int8 is None:
                return nb.boolean
            return boolean8 if bool_is_int8 else boolean1
        if self.is_pointer:
            return nb.types.CPointer(
                self[0].tonumba(bool_is_int8=bool_is_int8))
        if self.is_struct:
            struct_name = self._params.get('name')
            if struct_name is None:
                struct_name = 'STRUCT'+self.mangling
            members = []
            for i, member in enumerate(self):
                name = member._params.get('name', '_%s' % (i+1))
                members.append((name,
                                member.tonumba(bool_is_int8=bool_is_int8)))
            return make_numba_struct(struct_name, members)
        if self.is_function:
            rtype = self[0].tonumba(bool_is_int8=bool_is_int8)
            atypes = [t.tonumba(bool_is_int8=bool_is_int8)
                      for t in self[1] if not t.is_void]
            return rtype(*atypes)
        if self.is_string:
            return nb.types.string
        if self.is_char:
            # in numba, char==int8
            return _numba_int_map.get(int(self[0][4:]))
        if self.is_atomic:
            return nb.types.Type(self[0])
        raise NotImplementedError(repr(self))

    def toctypes(self):
        """Convert Type instance to ctypes type object.
        """
        if self.is_void:
            return None
        if self.is_int:
            return _ctypes_int_map[int(self[0][3:])]
        if self.is_uint:
            return _ctypes_uint_map[int(self[0][4:])]
        if self.is_float:
            return _ctypes_float_map[int(self[0][5:])]
        if self.is_complex:
            return _ctypes_complex_map[int(self[0][7:])]
        if self.is_bool:
            return ctypes.c_bool
        if self.is_char:
            return _ctypes_char_map[int(self[0][4:])]
        if self.is_pointer:
            if self[0].is_void:
                return ctypes.c_void_p
            if self[0].is_char:
                return getattr(ctypes,
                               _ctypes_char_map.get(
                                   int(self[0][0][4:])).__name__ + '_p')
            return ctypes.POINTER(self[0].toctypes())
        if self.is_struct:
            fields = [('f%s' % i, t.toctypes()) for i, t in enumerate(self)]
            return type('struct%s' % (id(self)),
                        (ctypes.Structure, ),
                        dict(_fields_=fields))
        if self.is_function:
            rtype = self[0].toctypes()
            atypes = [t.toctypes() for t in self[1] if not t.is_void]
            return ctypes.CFUNCTYPE(rtype, *atypes)
        if self.is_string:
            return ctypes.c_wchar_p
        raise NotImplementedError(repr((self, self.is_string)))

    @classmethod
    def _fromstring(cls, s):
        s = s.strip()
        if s.endswith('*'):       # pointer
            return cls(cls._fromstring(s[:-1]), '*')
        if s.endswith('}'):       # struct
            if not s.startswith('{'):
                raise TypeParseError(
                    'mismatching curly parenthesis in `%s`' % (s))
            return cls(*map(cls._fromstring,
                            _commasplit(s[1:-1].strip())))
        if s.endswith(')'):       # function
            i = _findparen(s)
            if i < 0:
                raise TypeParseError('mismatching parenthesis in `%s`' % (s))
            rtype = cls._fromstring(s[:i])
            atypes = tuple(map(cls._fromstring,
                               _commasplit(s[i+1:-1].strip())))
            return cls(rtype, atypes)
        if s == 'void' or s == 'none' or not s:  # void
            return cls()
        m = _type_name_match(s)
        if m is not None:
            name = m.group(2)
            if not _bad_names_match(name):
                # `<typespec> <name>`
                t = cls._fromstring(m.group(1))
                t._params['name'] = name
                return t
        # atomic
        return cls(s)

    @classmethod
    def fromstring(cls, s, target_info=None):
        """Return new Type instance from a string.

        Parameters
        ----------
        s : str
        target_info : {TargetInfo, None}
          Specify TargetInfo instance that provides methods for
          determining the type information of a particular
          target. When not specified, then LocalTargetInfo instance
          will be created.
        """
        if target_info is None:
            target_info = LocalTargetInfo()
        try:
            return cls._fromstring(s)._normalize(
                target_info, target_info.strict)
        except TypeParseError as msg:
            raise ValueError('failed to parse `%s`: %s' % (s, msg))

    @classmethod
    def fromnumba(cls, t, target_info=None):
        """Return new Type instance from numba type object.
        """
        if nb is None:
            raise RuntimeError('importing numba failed: %s' % (nb_NA_message))
        n = _numba_imap.get(t)
        if n is not None:
            return cls.fromstring(n, target_info=target_info)
        if isinstance(t, nb.typing.templates.Signature):
            atypes = (cls.fromnumba(a, target_info=target_info)
                      for a in t.args)
            rtype = cls.fromnumba(t.return_type, target_info=target_info)
            return cls(rtype, tuple(atypes) or (Type(),))
        if isinstance(t, nb.types.misc.CPointer):
            return cls(cls.fromnumba(t.dtype, target_info=target_info), '*')
        raise NotImplementedError(repr(t))

    @classmethod
    def fromctypes(cls, t, target_info=None):
        """Return new Type instance from ctypes type object.
        """
        n = _ctypes_imap.get(t)
        if n is not None:
            return cls.fromstring(n, target_info=target_info)
        if issubclass(t, ctypes.Structure):
            return cls(*(cls.fromctypes(_t, target_info=target_info)
                         for _f, _t in t._fields_))
        if issubclass(t, ctypes._Pointer):
            return cls(cls.fromctypes(t._type_, target_info=target_info), '*')
        if issubclass(t, ctypes._CFuncPtr):
            return cls(cls.fromctypes(t._restype_, target_info=target_info),
                       tuple(map(cls.fromctypes, t._argtypes_)) or (Type(),))
        raise NotImplementedError(repr(t))

    @classmethod
    def fromcallable(cls, func, target_info=None):
        """Return new Type instance from a callable object.

        The callable object must use annotations for specifying the
        types of arguments and return value.
        """
        if func.__name__ == '<lambda>':
            # lambda function cannot carry annotations, hence:
            raise ValueError('constructing Type instance from '
                             'a lambda function is not supported')
        sig = inspect.signature(func)
        annot = sig.return_annotation
        if annot == sig.empty:
            rtype = cls()  # void
            # TODO: check that function does not return other than None
        else:
            rtype = cls.fromobject(annot, target_info=target_info)
        atypes = []
        for n, param in sig.parameters.items():
            annot = param.annotation
            if param.kind not in [inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                  inspect.Parameter.POSITIONAL_ONLY]:
                raise ValueError(
                    'callable argument kind must be positional,'
                    ' `%s` has kind %s' % (param, param.kind))
            if annot == sig.empty:
                atypes.append(cls('<type of %s>' % n))
            else:
                atypes.append(cls.fromobject(annot, target_info=target_info))
        return cls(rtype, tuple(atypes) or (Type(),))

    @classmethod
    def fromvalue(cls, obj, target_info=None):
        """Return Type instance that corresponds to given Python value.
        """
        n = _python_imap.get(type(obj))
        if n is not None:
            return cls.fromstring(n, target_info=target_info)
        raise NotImplementedError('%s.fromvalue(%r)'
                                  % (cls.__name__, obj))

    @classmethod
    def fromobject(cls, obj, target_info=None):
        """Return new Type instance from any object.

        Parameters
        ----------
        obj : object
        target_info : {TargetInfo, None}
          Specify TargetInfo instance that provides methods for
          determining the type information of a particular
          target. When not specified, then LocalTargetInfo instance
          will be created.
        """
        if isinstance(obj, cls):
            return obj
        if isinstance(obj, str):
            return cls.fromstring(obj, target_info=target_info)
        n = _python_imap.get(obj)
        if n is not None:
            return cls.fromstring(n, target_info=target_info)
        if hasattr(obj, '__module__'):
            if obj.__module__.startswith('numba'):
                return cls.fromnumba(obj, target_info=target_info)
            if obj.__module__.startswith('ctypes'):
                return cls.fromctypes(obj, target_info=target_info)
        if inspect.isclass(obj):
            if obj is int:
                return cls('int64')
            return cls.fromstring(obj.__name__,
                                  target_info=target_info)
        if callable(obj):
            return cls.fromcallable(obj, target_info=target_info)
        raise NotImplementedError(repr(type(obj)))

    def _normalize(self, target_info, strict):
        """Return new Type instance with atomic types normalized.
        """
        params = self._params
        if self.is_void:
            return self
        if self.is_atomic:
            s = self[0]
            m = _bool_match(s)
            if m is not None:
                return self.__class__('bool', **params)
            m = _string_match(s)
            if m is not None:
                return self.__class__('string', **params)
            for match, ntype in [
                    (_charn_match, 'char'),
                    (_intn_match, 'int'),
                    (_uintn_match, 'uint'),
                    (_floatn_match, 'float'),
                    (_complexn_match, 'complex'),
            ]:
                m = match(s)
                if m is not None:
                    bits = m.group(2)
                    return self.__class__(ntype + bits, **params)
            for match, otype, ntype in [
                    (_char_match, 'char', 'char'),
                    (_wchar_match, 'wchar', 'char'),

                    (_uchar_match, 'uchar', 'uint'),
                    (_schar_match, 'char', 'int'),

                    (_byte_match, 'byte', 'int'),
                    (_ubyte_match, 'ubyte', 'uint'),

                    (_short_match, 'short', 'int'),
                    (_ushort_match, 'ushort', 'uint'),

                    (_int_match, 'int', 'int'),
                    (_uint_match, 'uint', 'uint'),

                    (_long_match, 'long', 'int'),
                    (_ulong_match, 'ulong', 'uint'),

                    (_longlong_match, 'longlong', 'int'),
                    (_ulonglong_match, 'ulonglong', 'uint'),

                    (_size_t_match, 'size_t', 'uint'),
                    (_ssize_t_match, 'ssize_t', 'int'),

                    (_float_match, 'float', 'float'),
                    (_double_match, 'double', 'float'),
                    (_longdouble_match, 'longdouble', 'float'),
                    (_complex_match, 'complex', 'complex'),
            ]:
                if match(s) is not None:
                    bits = str(target_info.sizeof(otype) * 8)
                    return self.__class__(ntype + bits, **params)
            t = target_info.custom_type(s)
            if t is not None:
                return t
            if strict:
                raise ValueError('%s is not concrete' % (self))
            return self
        if self.is_pointer:
            return self.__class__(
                self[0]._normalize(target_info, strict), self[1], **params)
        if self.is_struct:
            return self.__class__(
                *(t._normalize(target_info, strict) for t in self), **params)
        if self.is_function:
            return self.__class__(
                self[0]._normalize(target_info, strict),
                tuple(t._normalize(target_info, strict) for t in self[1]),
                **params)
        raise NotImplementedError(repr(self))

    def mangle(self):
        """Return mangled type string.

        Mangled type string is a string representation of the type
        that can be used for extending the function name.
        """
        if self.is_void:
            return 'v'
        if self.is_pointer:
            return '_' + self[0].mangle() + 'P'
        if self.is_struct:
            return '_' + ''.join(m.mangle() for m in self) + 'K'
        if self.is_function:
            r = self[0].mangle()
            a = ''.join([a.mangle() for a in self[1]])
            return '_' + r + 'a' + a + 'A'
        if self.is_atomic:
            n = _mangling_map.get(self[0])
            if n is not None:
                return n
            n = self[0]
            return 'V' + str(len(n)) + 'V' + n
        raise NotImplementedError(repr(self))

    @classmethod
    def demangle(cls, s):
        block, rest = _demangle(s)
        assert not rest, repr(rest)
        assert len(block) == 1, repr(block)
        return block[0]

    @property
    def bits(self):
        if self.is_void:
            return 0
        if self.is_bool:
            return 1
        if self.is_int:
            return int(self[0][3:])
        if self.is_uint or self.is_char:
            return int(self[0][4:])
        if self.is_float:
            return int(self[0][5:])
        if self.is_complex:
            return int(self[0][6:])
        if self.is_struct:
            return sum([m.bits for m in self])
        return NotImplemented

    def match(self, other):
        """Return match penalty when other can be converted to self.
        Otherwise, return None.

        Parameters
        ----------
        other : {Type, tuple}
          Specify other signature. If other is a tuple of signatures,
          then it is interpreted as argument types of a function
          signature.

        Returns
        -------
        penalty : {int, None}
          Penalty of a match. For a perfect match, penalty is 0.
          If match is impossible, return None
        """
        if isinstance(other, Type):
            if self == other:
                return 0
            if other.is_void:
                return (0 if self.is_void else None)
            elif other.is_pointer:
                if not self.is_pointer:
                    return
                penalty = self[0].match(other)
                if penalty is None:
                    if self[0].is_void:
                        penalty = 1
                return penalty
            elif other.is_struct:
                if not self.is_struct:
                    return
                if len(self) != len(other):
                    return
                penalty = 0
                for a, b in zip(self, other):
                    p = a.match(b)
                    if p is None:
                        return
                    penalty = penalty + p
                return penalty
            elif other.is_function:
                if not self.is_function:
                    return
                if len(self[1]) != len(other[1]):
                    return
                penalty = self[0].match(other[0])
                if penalty is None:
                    return
                for a, b in zip(self[1], other[1]):
                    p = a.match(b)
                    if p is None:
                        return
                    penalty = penalty + p
                return penalty
            if (
                    (other.is_int and self.is_int)
                    or (other.is_float and self.is_float)
                    or (other.is_uint and self.is_uint)
                    or (other.is_char and self.is_char)
                    or (other.is_complex and self.is_complex)):
                if self.bits >= other.bits:
                    return 0
                return other.bits - self.bits
            if self.is_complex and (other.is_float
                                    or other.is_int or other.is_uint):
                return 1000
            if self.is_float and (other.is_int or other.is_uint):
                return 1000
            # TODO: lots of
            return None
            raise NotImplementedError(repr((self, other)))
        elif isinstance(other, tuple):
            if not self.is_function:
                return
            atypes = self[1]
            if len(atypes) != len(other):
                return
            penalty = 0
            for a, b in zip(atypes, other):
                p = a.match(b)
                if p is None:
                    return
                penalty = penalty + p
            return penalty
        raise NotImplementedError(repr(type(other)))

    def __call__(self, *atypes, **params):
        return self.__class__(self, atypes, **params)

    def pointer(self):
        return self.__class__(self, '*')


def _demangle(s):
    """Helper function to demangle the string of mangled Type.

    Used internally.

    Algorithm invented by Pearu Peterson, February 2019
    """
    if not s:
        return (Type(),), ''
    if s[0] == 'V':
        i = s.find('V', 1)
        assert i != -1, repr(s)
        ln = int(s[1:i])
        rest = s[i+ln+1:]
        typ = Type(s[i+1:i+ln+1])
    elif s[0] == '_':
        block, rest = _demangle(s[1:])
        kind, rest = rest[0], rest[1:]
        assert kind in '_'+_mangling_suffices+_mangling_prefixes, repr(kind)
        if kind == 'P':
            assert len(block) == 1, repr(block)
            typ = Type(block[0], '*')
        elif kind == 'K':
            typ = Type(*block)
        elif kind == 'a':
            assert len(block) == 1, repr(block)
            rtype = block[0]
            atypes, rest = _demangle('_' + rest)
            typ = Type(rtype, atypes)
        elif kind == 'A':
            return block, rest
        else:
            raise NotImplementedError(repr((kind, s)))
    else:
        rest = s[1:]
        t = _mangling_imap[s[0]]
        if t == 'void':
            typ = Type()
        else:
            typ = Type(t)
    result = [typ]
    if rest and rest[0] not in _mangling_prefixes:
        r, rest = _demangle(rest)
        result.extend(r)
    return tuple(result), rest


if nb is not None:
    class Boolean1(numba.types.Boolean):
        pass

    @numba.datamodel.register_default(Boolean1)
    class Boolean1Model(numba.datamodel.models.BooleanModel):

        def get_data_type(self):
            return self._bit_type

    class Boolean8(numba.types.Boolean):
        pass

    @numba.datamodel.register_default(Boolean8)
    class Boolean8Model(numba.datamodel.models.BooleanModel):

        def get_value_type(self):
            return self._byte_type

    boolean1 = Boolean1('boolean1')
    boolean8 = Boolean8('boolean8')

    @numba.targets.imputils.lower_cast(Boolean1, numba.types.Boolean)
    @numba.targets.imputils.lower_cast(Boolean8, numba.types.Boolean)
    def literal_booleanN_to_boolean(context, builder, fromty, toty, val):
        return builder.icmp_signed('!=', val, val.type(0))


def make_numba_struct(name, members, _cache={}):
    """Create numba struct type instance.
    """
    t = _cache.get(name)
    if t is None:
        def model__init__(self, dmm, fe_type):
            numba.datamodel.StructModel.__init__(self, dmm, fe_type, members)
        struct_model = type(name+'Model',
                            (numba.datamodel.StructModel,),
                            dict(__init__=model__init__))
        struct_type = type(name+'Type', (numba.types.Type,),
                           dict(members=[t for n, t in members]))
        numba.datamodel.registry.register_default(struct_type)(struct_model)
        _cache[name] = t = struct_type(name)
    return t
