"""File generated by TLObjects' generator. All changes will be ERASED"""
from ...tl.tlobject import TLObject
from typing import Optional, List, Union, TYPE_CHECKING
import os
import struct
from datetime import datetime
if TYPE_CHECKING:
    from ...tl.types import TypeUser
    from ...tl.types.help import TypeTermsOfService
    from ...tl.types.auth import TypeCodeType, TypeSentCodeType



class Authorization(TLObject):
    CONSTRUCTOR_ID = 0xcd050916
    SUBCLASS_OF_ID = 0xb9e04e39

    def __init__(self, user: 'TypeUser', tmp_sessions: Optional[int]=None):
        """
        Constructor for auth.Authorization: Instance of either Authorization, AuthorizationSignUpRequired.
        """
        self.user = user
        self.tmp_sessions = tmp_sessions

    def to_dict(self):
        return {
            '_': 'Authorization',
            'user': self.user.to_dict() if isinstance(self.user, TLObject) else self.user,
            'tmp_sessions': self.tmp_sessions
        }

    def __bytes__(self):
        return b''.join((
            b'\x16\t\x05\xcd',
            struct.pack('<I', (0 if self.tmp_sessions is None or self.tmp_sessions is False else 1)),
            b'' if self.tmp_sessions is None or self.tmp_sessions is False else (struct.pack('<i', self.tmp_sessions)),
            bytes(self.user),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        if flags & 1:
            _tmp_sessions = reader.read_int()
        else:
            _tmp_sessions = None
        _user = reader.tgread_object()
        return cls(user=_user, tmp_sessions=_tmp_sessions)


class AuthorizationSignUpRequired(TLObject):
    CONSTRUCTOR_ID = 0x44747e9a
    SUBCLASS_OF_ID = 0xb9e04e39

    def __init__(self, terms_of_service: Optional['TypeTermsOfService']=None):
        """
        Constructor for auth.Authorization: Instance of either Authorization, AuthorizationSignUpRequired.
        """
        self.terms_of_service = terms_of_service

    def to_dict(self):
        return {
            '_': 'AuthorizationSignUpRequired',
            'terms_of_service': self.terms_of_service.to_dict() if isinstance(self.terms_of_service, TLObject) else self.terms_of_service
        }

    def __bytes__(self):
        return b''.join((
            b'\x9a~tD',
            struct.pack('<I', (0 if self.terms_of_service is None or self.terms_of_service is False else 1)),
            b'' if self.terms_of_service is None or self.terms_of_service is False else (bytes(self.terms_of_service)),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        if flags & 1:
            _terms_of_service = reader.tgread_object()
        else:
            _terms_of_service = None
        return cls(terms_of_service=_terms_of_service)


class CodeTypeCall(TLObject):
    CONSTRUCTOR_ID = 0x741cd3e3
    SUBCLASS_OF_ID = 0xb3f3e401

    def to_dict(self):
        return {
            '_': 'CodeTypeCall'
        }

    def __bytes__(self):
        return b''.join((
            b'\xe3\xd3\x1ct',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class CodeTypeFlashCall(TLObject):
    CONSTRUCTOR_ID = 0x226ccefb
    SUBCLASS_OF_ID = 0xb3f3e401

    def to_dict(self):
        return {
            '_': 'CodeTypeFlashCall'
        }

    def __bytes__(self):
        return b''.join((
            b'\xfb\xcel"',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class CodeTypeSms(TLObject):
    CONSTRUCTOR_ID = 0x72a3158c
    SUBCLASS_OF_ID = 0xb3f3e401

    def to_dict(self):
        return {
            '_': 'CodeTypeSms'
        }

    def __bytes__(self):
        return b''.join((
            b'\x8c\x15\xa3r',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class ExportedAuthorization(TLObject):
    CONSTRUCTOR_ID = 0xdf969c2d
    SUBCLASS_OF_ID = 0x5fd1ec51

    # noinspection PyShadowingBuiltins
    def __init__(self, id: int, bytes: bytes):
        """
        Constructor for auth.ExportedAuthorization: Instance of ExportedAuthorization.
        """
        self.id = id
        self.bytes = bytes

    def to_dict(self):
        return {
            '_': 'ExportedAuthorization',
            'id': self.id,
            'bytes': self.bytes
        }

    def __bytes__(self):
        return b''.join((
            b'-\x9c\x96\xdf',
            struct.pack('<i', self.id),
            self.serialize_bytes(self.bytes),
        ))

    @classmethod
    def from_reader(cls, reader):
        _id = reader.read_int()
        _bytes = reader.tgread_bytes()
        return cls(id=_id, bytes=_bytes)


class PasswordRecovery(TLObject):
    CONSTRUCTOR_ID = 0x137948a5
    SUBCLASS_OF_ID = 0xfa72d43a

    def __init__(self, email_pattern: str):
        """
        Constructor for auth.PasswordRecovery: Instance of PasswordRecovery.
        """
        self.email_pattern = email_pattern

    def to_dict(self):
        return {
            '_': 'PasswordRecovery',
            'email_pattern': self.email_pattern
        }

    def __bytes__(self):
        return b''.join((
            b'\xa5Hy\x13',
            self.serialize_bytes(self.email_pattern),
        ))

    @classmethod
    def from_reader(cls, reader):
        _email_pattern = reader.tgread_string()
        return cls(email_pattern=_email_pattern)


class SentCode(TLObject):
    CONSTRUCTOR_ID = 0x5e002502
    SUBCLASS_OF_ID = 0x6ce87081

    # noinspection PyShadowingBuiltins
    def __init__(self, type: 'TypeSentCodeType', phone_code_hash: str, next_type: Optional['TypeCodeType']=None, timeout: Optional[int]=None):
        """
        Constructor for auth.SentCode: Instance of SentCode.
        """
        self.type = type
        self.phone_code_hash = phone_code_hash
        self.next_type = next_type
        self.timeout = timeout

    def to_dict(self):
        return {
            '_': 'SentCode',
            'type': self.type.to_dict() if isinstance(self.type, TLObject) else self.type,
            'phone_code_hash': self.phone_code_hash,
            'next_type': self.next_type.to_dict() if isinstance(self.next_type, TLObject) else self.next_type,
            'timeout': self.timeout
        }

    def __bytes__(self):
        return b''.join((
            b'\x02%\x00^',
            struct.pack('<I', (0 if self.next_type is None or self.next_type is False else 2) | (0 if self.timeout is None or self.timeout is False else 4)),
            bytes(self.type),
            self.serialize_bytes(self.phone_code_hash),
            b'' if self.next_type is None or self.next_type is False else (bytes(self.next_type)),
            b'' if self.timeout is None or self.timeout is False else (struct.pack('<i', self.timeout)),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        _type = reader.tgread_object()
        _phone_code_hash = reader.tgread_string()
        if flags & 2:
            _next_type = reader.tgread_object()
        else:
            _next_type = None
        if flags & 4:
            _timeout = reader.read_int()
        else:
            _timeout = None
        return cls(type=_type, phone_code_hash=_phone_code_hash, next_type=_next_type, timeout=_timeout)


class SentCodeTypeApp(TLObject):
    CONSTRUCTOR_ID = 0x3dbb5986
    SUBCLASS_OF_ID = 0xff5b158e

    def __init__(self, length: int):
        """
        Constructor for auth.SentCodeType: Instance of either SentCodeTypeApp, SentCodeTypeSms, SentCodeTypeCall, SentCodeTypeFlashCall.
        """
        self.length = length

    def to_dict(self):
        return {
            '_': 'SentCodeTypeApp',
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'\x86Y\xbb=',
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _length = reader.read_int()
        return cls(length=_length)


class SentCodeTypeCall(TLObject):
    CONSTRUCTOR_ID = 0x5353e5a7
    SUBCLASS_OF_ID = 0xff5b158e

    def __init__(self, length: int):
        """
        Constructor for auth.SentCodeType: Instance of either SentCodeTypeApp, SentCodeTypeSms, SentCodeTypeCall, SentCodeTypeFlashCall.
        """
        self.length = length

    def to_dict(self):
        return {
            '_': 'SentCodeTypeCall',
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'\xa7\xe5SS',
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _length = reader.read_int()
        return cls(length=_length)


class SentCodeTypeFlashCall(TLObject):
    CONSTRUCTOR_ID = 0xab03c6d9
    SUBCLASS_OF_ID = 0xff5b158e

    def __init__(self, pattern: str):
        """
        Constructor for auth.SentCodeType: Instance of either SentCodeTypeApp, SentCodeTypeSms, SentCodeTypeCall, SentCodeTypeFlashCall.
        """
        self.pattern = pattern

    def to_dict(self):
        return {
            '_': 'SentCodeTypeFlashCall',
            'pattern': self.pattern
        }

    def __bytes__(self):
        return b''.join((
            b'\xd9\xc6\x03\xab',
            self.serialize_bytes(self.pattern),
        ))

    @classmethod
    def from_reader(cls, reader):
        _pattern = reader.tgread_string()
        return cls(pattern=_pattern)


class SentCodeTypeSms(TLObject):
    CONSTRUCTOR_ID = 0xc000bba2
    SUBCLASS_OF_ID = 0xff5b158e

    def __init__(self, length: int):
        """
        Constructor for auth.SentCodeType: Instance of either SentCodeTypeApp, SentCodeTypeSms, SentCodeTypeCall, SentCodeTypeFlashCall.
        """
        self.length = length

    def to_dict(self):
        return {
            '_': 'SentCodeTypeSms',
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'\xa2\xbb\x00\xc0',
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _length = reader.read_int()
        return cls(length=_length)

