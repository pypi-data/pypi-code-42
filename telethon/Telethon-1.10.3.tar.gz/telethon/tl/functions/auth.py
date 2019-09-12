"""File generated by TLObjects' generator. All changes will be ERASED"""
from ...tl.tlobject import TLObject
from ...tl.tlobject import TLRequest
from typing import Optional, List, Union, TYPE_CHECKING
import os
import struct
from datetime import datetime
if TYPE_CHECKING:
    from ...tl.types import TypeCodeSettings, TypeInputCheckPasswordSRP



class BindTempAuthKeyRequest(TLRequest):
    CONSTRUCTOR_ID = 0xcdd42a05
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, perm_auth_key_id: int, nonce: int, expires_at: Optional[datetime], encrypted_message: bytes):
        """
        :returns Bool: This type has no constructors.
        """
        self.perm_auth_key_id = perm_auth_key_id
        self.nonce = nonce
        self.expires_at = expires_at
        self.encrypted_message = encrypted_message

    def to_dict(self):
        return {
            '_': 'BindTempAuthKeyRequest',
            'perm_auth_key_id': self.perm_auth_key_id,
            'nonce': self.nonce,
            'expires_at': self.expires_at,
            'encrypted_message': self.encrypted_message
        }

    def __bytes__(self):
        return b''.join((
            b'\x05*\xd4\xcd',
            struct.pack('<q', self.perm_auth_key_id),
            struct.pack('<q', self.nonce),
            self.serialize_datetime(self.expires_at),
            self.serialize_bytes(self.encrypted_message),
        ))

    @classmethod
    def from_reader(cls, reader):
        _perm_auth_key_id = reader.read_long()
        _nonce = reader.read_long()
        _expires_at = reader.tgread_date()
        _encrypted_message = reader.tgread_bytes()
        return cls(perm_auth_key_id=_perm_auth_key_id, nonce=_nonce, expires_at=_expires_at, encrypted_message=_encrypted_message)


class CancelCodeRequest(TLRequest):
    CONSTRUCTOR_ID = 0x1f040578
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, phone_number: str, phone_code_hash: str):
        """
        :returns Bool: This type has no constructors.
        """
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash

    def to_dict(self):
        return {
            '_': 'CancelCodeRequest',
            'phone_number': self.phone_number,
            'phone_code_hash': self.phone_code_hash
        }

    def __bytes__(self):
        return b''.join((
            b'x\x05\x04\x1f',
            self.serialize_bytes(self.phone_number),
            self.serialize_bytes(self.phone_code_hash),
        ))

    @classmethod
    def from_reader(cls, reader):
        _phone_number = reader.tgread_string()
        _phone_code_hash = reader.tgread_string()
        return cls(phone_number=_phone_number, phone_code_hash=_phone_code_hash)


class CheckPasswordRequest(TLRequest):
    CONSTRUCTOR_ID = 0xd18b4d16
    SUBCLASS_OF_ID = 0xb9e04e39

    def __init__(self, password: 'TypeInputCheckPasswordSRP'):
        """
        :returns auth.Authorization: Instance of either Authorization, AuthorizationSignUpRequired.
        """
        self.password = password

    def to_dict(self):
        return {
            '_': 'CheckPasswordRequest',
            'password': self.password.to_dict() if isinstance(self.password, TLObject) else self.password
        }

    def __bytes__(self):
        return b''.join((
            b'\x16M\x8b\xd1',
            bytes(self.password),
        ))

    @classmethod
    def from_reader(cls, reader):
        _password = reader.tgread_object()
        return cls(password=_password)


class DropTempAuthKeysRequest(TLRequest):
    CONSTRUCTOR_ID = 0x8e48a188
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, except_auth_keys: List[int]):
        """
        :returns Bool: This type has no constructors.
        """
        self.except_auth_keys = except_auth_keys

    def to_dict(self):
        return {
            '_': 'DropTempAuthKeysRequest',
            'except_auth_keys': [] if self.except_auth_keys is None else self.except_auth_keys[:]
        }

    def __bytes__(self):
        return b''.join((
            b'\x88\xa1H\x8e',
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.except_auth_keys)),b''.join(struct.pack('<q', x) for x in self.except_auth_keys),
        ))

    @classmethod
    def from_reader(cls, reader):
        reader.read_int()
        _except_auth_keys = []
        for _ in range(reader.read_int()):
            _x = reader.read_long()
            _except_auth_keys.append(_x)

        return cls(except_auth_keys=_except_auth_keys)


class ExportAuthorizationRequest(TLRequest):
    CONSTRUCTOR_ID = 0xe5bfffcd
    SUBCLASS_OF_ID = 0x5fd1ec51

    def __init__(self, dc_id: int):
        """
        :returns auth.ExportedAuthorization: Instance of ExportedAuthorization.
        """
        self.dc_id = dc_id

    def to_dict(self):
        return {
            '_': 'ExportAuthorizationRequest',
            'dc_id': self.dc_id
        }

    def __bytes__(self):
        return b''.join((
            b'\xcd\xff\xbf\xe5',
            struct.pack('<i', self.dc_id),
        ))

    @classmethod
    def from_reader(cls, reader):
        _dc_id = reader.read_int()
        return cls(dc_id=_dc_id)


class ImportAuthorizationRequest(TLRequest):
    CONSTRUCTOR_ID = 0xe3ef9613
    SUBCLASS_OF_ID = 0xb9e04e39

    # noinspection PyShadowingBuiltins
    def __init__(self, id: int, bytes: bytes):
        """
        :returns auth.Authorization: Instance of either Authorization, AuthorizationSignUpRequired.
        """
        self.id = id
        self.bytes = bytes

    def to_dict(self):
        return {
            '_': 'ImportAuthorizationRequest',
            'id': self.id,
            'bytes': self.bytes
        }

    def __bytes__(self):
        return b''.join((
            b'\x13\x96\xef\xe3',
            struct.pack('<i', self.id),
            self.serialize_bytes(self.bytes),
        ))

    @classmethod
    def from_reader(cls, reader):
        _id = reader.read_int()
        _bytes = reader.tgread_bytes()
        return cls(id=_id, bytes=_bytes)


class ImportBotAuthorizationRequest(TLRequest):
    CONSTRUCTOR_ID = 0x67a3ff2c
    SUBCLASS_OF_ID = 0xb9e04e39

    def __init__(self, flags: int, api_id: int, api_hash: str, bot_auth_token: str):
        """
        :returns auth.Authorization: Instance of either Authorization, AuthorizationSignUpRequired.
        """
        self.flags = flags
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_auth_token = bot_auth_token

    def to_dict(self):
        return {
            '_': 'ImportBotAuthorizationRequest',
            'flags': self.flags,
            'api_id': self.api_id,
            'api_hash': self.api_hash,
            'bot_auth_token': self.bot_auth_token
        }

    def __bytes__(self):
        return b''.join((
            b',\xff\xa3g',
            struct.pack('<i', self.flags),
            struct.pack('<i', self.api_id),
            self.serialize_bytes(self.api_hash),
            self.serialize_bytes(self.bot_auth_token),
        ))

    @classmethod
    def from_reader(cls, reader):
        _flags = reader.read_int()
        _api_id = reader.read_int()
        _api_hash = reader.tgread_string()
        _bot_auth_token = reader.tgread_string()
        return cls(flags=_flags, api_id=_api_id, api_hash=_api_hash, bot_auth_token=_bot_auth_token)


class LogOutRequest(TLRequest):
    CONSTRUCTOR_ID = 0x5717da40
    SUBCLASS_OF_ID = 0xf5b399ac

    def to_dict(self):
        return {
            '_': 'LogOutRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'@\xda\x17W',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class RecoverPasswordRequest(TLRequest):
    CONSTRUCTOR_ID = 0x4ea56e92
    SUBCLASS_OF_ID = 0xb9e04e39

    def __init__(self, code: str):
        """
        :returns auth.Authorization: Instance of either Authorization, AuthorizationSignUpRequired.
        """
        self.code = code

    def to_dict(self):
        return {
            '_': 'RecoverPasswordRequest',
            'code': self.code
        }

    def __bytes__(self):
        return b''.join((
            b'\x92n\xa5N',
            self.serialize_bytes(self.code),
        ))

    @classmethod
    def from_reader(cls, reader):
        _code = reader.tgread_string()
        return cls(code=_code)


class RequestPasswordRecoveryRequest(TLRequest):
    CONSTRUCTOR_ID = 0xd897bc66
    SUBCLASS_OF_ID = 0xfa72d43a

    def to_dict(self):
        return {
            '_': 'RequestPasswordRecoveryRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'f\xbc\x97\xd8',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class ResendCodeRequest(TLRequest):
    CONSTRUCTOR_ID = 0x3ef1a9bf
    SUBCLASS_OF_ID = 0x6ce87081

    def __init__(self, phone_number: str, phone_code_hash: str):
        """
        :returns auth.SentCode: Instance of SentCode.
        """
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash

    def to_dict(self):
        return {
            '_': 'ResendCodeRequest',
            'phone_number': self.phone_number,
            'phone_code_hash': self.phone_code_hash
        }

    def __bytes__(self):
        return b''.join((
            b'\xbf\xa9\xf1>',
            self.serialize_bytes(self.phone_number),
            self.serialize_bytes(self.phone_code_hash),
        ))

    @classmethod
    def from_reader(cls, reader):
        _phone_number = reader.tgread_string()
        _phone_code_hash = reader.tgread_string()
        return cls(phone_number=_phone_number, phone_code_hash=_phone_code_hash)


class ResetAuthorizationsRequest(TLRequest):
    CONSTRUCTOR_ID = 0x9fab0d1a
    SUBCLASS_OF_ID = 0xf5b399ac

    def to_dict(self):
        return {
            '_': 'ResetAuthorizationsRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'\x1a\r\xab\x9f',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class SendCodeRequest(TLRequest):
    CONSTRUCTOR_ID = 0xa677244f
    SUBCLASS_OF_ID = 0x6ce87081

    def __init__(self, phone_number: str, api_id: int, api_hash: str, settings: 'TypeCodeSettings'):
        """
        :returns auth.SentCode: Instance of SentCode.
        """
        self.phone_number = phone_number
        self.api_id = api_id
        self.api_hash = api_hash
        self.settings = settings

    def to_dict(self):
        return {
            '_': 'SendCodeRequest',
            'phone_number': self.phone_number,
            'api_id': self.api_id,
            'api_hash': self.api_hash,
            'settings': self.settings.to_dict() if isinstance(self.settings, TLObject) else self.settings
        }

    def __bytes__(self):
        return b''.join((
            b'O$w\xa6',
            self.serialize_bytes(self.phone_number),
            struct.pack('<i', self.api_id),
            self.serialize_bytes(self.api_hash),
            bytes(self.settings),
        ))

    @classmethod
    def from_reader(cls, reader):
        _phone_number = reader.tgread_string()
        _api_id = reader.read_int()
        _api_hash = reader.tgread_string()
        _settings = reader.tgread_object()
        return cls(phone_number=_phone_number, api_id=_api_id, api_hash=_api_hash, settings=_settings)


class SignInRequest(TLRequest):
    CONSTRUCTOR_ID = 0xbcd51581
    SUBCLASS_OF_ID = 0xb9e04e39

    def __init__(self, phone_number: str, phone_code_hash: str, phone_code: str):
        """
        :returns auth.Authorization: Instance of either Authorization, AuthorizationSignUpRequired.
        """
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash
        self.phone_code = phone_code

    def to_dict(self):
        return {
            '_': 'SignInRequest',
            'phone_number': self.phone_number,
            'phone_code_hash': self.phone_code_hash,
            'phone_code': self.phone_code
        }

    def __bytes__(self):
        return b''.join((
            b'\x81\x15\xd5\xbc',
            self.serialize_bytes(self.phone_number),
            self.serialize_bytes(self.phone_code_hash),
            self.serialize_bytes(self.phone_code),
        ))

    @classmethod
    def from_reader(cls, reader):
        _phone_number = reader.tgread_string()
        _phone_code_hash = reader.tgread_string()
        _phone_code = reader.tgread_string()
        return cls(phone_number=_phone_number, phone_code_hash=_phone_code_hash, phone_code=_phone_code)


class SignUpRequest(TLRequest):
    CONSTRUCTOR_ID = 0x80eee427
    SUBCLASS_OF_ID = 0xb9e04e39

    def __init__(self, phone_number: str, phone_code_hash: str, first_name: str, last_name: str):
        """
        :returns auth.Authorization: Instance of either Authorization, AuthorizationSignUpRequired.
        """
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        return {
            '_': 'SignUpRequest',
            'phone_number': self.phone_number,
            'phone_code_hash': self.phone_code_hash,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

    def __bytes__(self):
        return b''.join((
            b"'\xe4\xee\x80",
            self.serialize_bytes(self.phone_number),
            self.serialize_bytes(self.phone_code_hash),
            self.serialize_bytes(self.first_name),
            self.serialize_bytes(self.last_name),
        ))

    @classmethod
    def from_reader(cls, reader):
        _phone_number = reader.tgread_string()
        _phone_code_hash = reader.tgread_string()
        _first_name = reader.tgread_string()
        _last_name = reader.tgread_string()
        return cls(phone_number=_phone_number, phone_code_hash=_phone_code_hash, first_name=_first_name, last_name=_last_name)

