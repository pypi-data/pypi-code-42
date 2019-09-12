from .rpcbaseerrors import RPCError, AuthKeyError, BadRequestError, FloodError, ForbiddenError, InvalidDCError, ServerError, TimedOutError, UnauthorizedError


class AboutTooLongError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided bio is too long' + self._fmt_request(kwargs['request']))


class AccessTokenExpiredError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Bot token expired' + self._fmt_request(kwargs['request']))


class AccessTokenInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided token is not valid' + self._fmt_request(kwargs['request']))


class ActiveUserRequiredError(UnauthorizedError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The method is only available to already activated users' + self._fmt_request(kwargs['request']))


class AdminsTooMuchError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Too many admins' + self._fmt_request(kwargs['request']))


class AdminRankEmojiNotAllowedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Emoji are not allowed in admin titles or ranks' + self._fmt_request(kwargs['request']))


class AdminRankInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The given admin title or rank was invalid (possibly larger than 16 characters)' + self._fmt_request(kwargs['request']))


class ApiIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The api_id/api_hash combination is invalid' + self._fmt_request(kwargs['request']))


class ApiIdPublishedFloodError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("This API id was published somewhere, you can't use it now" + self._fmt_request(kwargs['request']))


class ArticleTitleEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The title of the article is empty' + self._fmt_request(kwargs['request']))


class AuthBytesInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided authorization is invalid' + self._fmt_request(kwargs['request']))


class AuthKeyDuplicatedError(AuthKeyError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The authorization key (session file) was used under two different IP addresses simultaneously, and can no longer be used. Use the same session exclusively, or use different sessions' + self._fmt_request(kwargs['request']))


class AuthKeyInvalidError(UnauthorizedError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The key is invalid' + self._fmt_request(kwargs['request']))


class AuthKeyPermEmptyError(UnauthorizedError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The method is unavailable for temporary authorization key, not bound to permanent' + self._fmt_request(kwargs['request']))


class AuthKeyUnregisteredError(UnauthorizedError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The key is not registered in the system' + self._fmt_request(kwargs['request']))


class AuthRestartError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Restart the authorization process' + self._fmt_request(kwargs['request']))


class BannedRightsInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('You cannot use that set of permissions in this request, i.e. restricting view_messages as a default' + self._fmt_request(kwargs['request']))


class BotsTooMuchError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('There are too many bots in this chat/channel' + self._fmt_request(kwargs['request']))


class BotChannelsNaError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("Bots can't edit admin privileges" + self._fmt_request(kwargs['request']))


class BotGroupsBlockedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("This bot can't be added to groups" + self._fmt_request(kwargs['request']))


class BotInlineDisabledError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("This bot can't be used in inline mode" + self._fmt_request(kwargs['request']))


class BotInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('This is not a valid bot' + self._fmt_request(kwargs['request']))


class BotMethodInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The API access for bot users is restricted. The method you tried to invoke cannot be executed as a bot' + self._fmt_request(kwargs['request']))


class BotMissingError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('This method can only be run by a bot' + self._fmt_request(kwargs['request']))


class BotPaymentsDisabledError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('This method can only be run by a bot' + self._fmt_request(kwargs['request']))


class BotPollsDisabledError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('You cannot create polls under a bot account' + self._fmt_request(kwargs['request']))


class BroadcastIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The channel is invalid' + self._fmt_request(kwargs['request']))


class ButtonDataInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided button data is invalid' + self._fmt_request(kwargs['request']))


class ButtonTypeInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The type of one of the buttons you provided is invalid' + self._fmt_request(kwargs['request']))


class ButtonUrlInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Button URL invalid' + self._fmt_request(kwargs['request']))


class CallAlreadyAcceptedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The call was already accepted' + self._fmt_request(kwargs['request']))


class CallAlreadyDeclinedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The call was already declined' + self._fmt_request(kwargs['request']))


class CallOccupyFailedError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The call failed because the user is already making another call' + self._fmt_request(kwargs['request']))


class CallPeerInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided call peer object is invalid' + self._fmt_request(kwargs['request']))


class CallProtocolFlagsInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Call protocol flags invalid' + self._fmt_request(kwargs['request']))


class CdnMethodInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('This method cannot be invoked on a CDN server. Refer to https://core.telegram.org/cdn#schema for available methods' + self._fmt_request(kwargs['request']))


class ChannelsAdminPublicTooMuchError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("You're admin of too many public channels, make some channels private to change the username of this channel" + self._fmt_request(kwargs['request']))


class ChannelsTooMuchError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('You have joined too many channels/supergroups' + self._fmt_request(kwargs['request']))


class ChannelInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Invalid channel object. Make sure to pass the right types, for instance making sure that the request is designed for channels or otherwise look for a different one more suited' + self._fmt_request(kwargs['request']))


class ChannelPrivateError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The channel specified is private and you lack permission to access it. Another reason may be that you were banned from it' + self._fmt_request(kwargs['request']))


class ChannelPublicGroupNaError(ForbiddenError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('channel/supergroup not available' + self._fmt_request(kwargs['request']))


class ChatAboutNotModifiedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('About text has not changed' + self._fmt_request(kwargs['request']))


class ChatAboutTooLongError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Chat about too long' + self._fmt_request(kwargs['request']))


class ChatAdminInviteRequiredError(ForbiddenError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('You do not have the rights to do this' + self._fmt_request(kwargs['request']))


class ChatAdminRequiredError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Chat admin privileges are required to do that in the specified chat (for example, to send a message in a channel which is not yours), or invalid permissions used for the channel or group' + self._fmt_request(kwargs['request']))


class ChatForbiddenError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('You cannot write in this chat' + self._fmt_request(kwargs['request']))


class ChatIdEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided chat ID is empty' + self._fmt_request(kwargs['request']))


class ChatIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Invalid object ID for a chat. Make sure to pass the right types, for instance making sure that the request is designed for chats (not channels/megagroups) or otherwise look for a different one more suited\\nAn example working with a megagroup and AddChatUserRequest, it will fail because megagroups are channels. Use InviteToChannelRequest instead' + self._fmt_request(kwargs['request']))


class ChatInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The chat is invalid for this request' + self._fmt_request(kwargs['request']))


class ChatLinkExistsError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The chat is linked to a channel and cannot be used in that request' + self._fmt_request(kwargs['request']))


class ChatNotModifiedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("The chat or channel wasn't modified (title, invites, username, admins, etc. are the same)" + self._fmt_request(kwargs['request']))


class ChatRestrictedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The chat is restricted and cannot be used in that request' + self._fmt_request(kwargs['request']))


class ChatSendGifsForbiddenError(ForbiddenError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("You can't send gifs in this chat" + self._fmt_request(kwargs['request']))


class ChatSendInlineForbiddenError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('You cannot send inline results in this chat' + self._fmt_request(kwargs['request']))


class ChatSendMediaForbiddenError(ForbiddenError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("You can't send media in this chat" + self._fmt_request(kwargs['request']))


class ChatSendStickersForbiddenError(ForbiddenError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("You can't send stickers in this chat" + self._fmt_request(kwargs['request']))


class ChatTitleEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('No chat title provided' + self._fmt_request(kwargs['request']))


class ChatWriteForbiddenError(ForbiddenError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("You can't write in this chat" + self._fmt_request(kwargs['request']))


class CodeEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided code is empty' + self._fmt_request(kwargs['request']))


class CodeHashInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Code hash invalid' + self._fmt_request(kwargs['request']))


class CodeInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Code invalid (i.e. from email)' + self._fmt_request(kwargs['request']))


class ConnectionApiIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided API id is invalid' + self._fmt_request(kwargs['request']))


class ConnectionDeviceModelEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Device model empty' + self._fmt_request(kwargs['request']))


class ConnectionLangPackInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The specified language pack is not valid. This is meant to be used by official applications only so far, leave it empty' + self._fmt_request(kwargs['request']))


class ConnectionLayerInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The very first request must always be InvokeWithLayerRequest' + self._fmt_request(kwargs['request']))


class ConnectionNotInitedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Connection not initialized' + self._fmt_request(kwargs['request']))


class ConnectionSystemEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Connection system empty' + self._fmt_request(kwargs['request']))


class ContactIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided contact ID is invalid' + self._fmt_request(kwargs['request']))


class DataInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Encrypted data invalid' + self._fmt_request(kwargs['request']))


class DataJsonInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided JSON data is invalid' + self._fmt_request(kwargs['request']))


class DateEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Date empty' + self._fmt_request(kwargs['request']))


class DcIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('This occurs when an authorization is tried to be exported for the same data center one is currently connected to' + self._fmt_request(kwargs['request']))


class DhGAInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('g_a invalid' + self._fmt_request(kwargs['request']))


class EmailHashExpiredError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The email hash expired and cannot be used to verify it' + self._fmt_request(kwargs['request']))


class EmailInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The given email is invalid' + self._fmt_request(kwargs['request']))


class EmailUnconfirmedError(BadRequestError):
    def __init__(self, **kwargs):
        self.code_length = int(kwargs.get('capture', 0))
        super(Exception, self).__init__('Email unconfirmed, the length of the code must be {code_length}'.format(code_length=self.code_length) + self._fmt_request(kwargs['request']))


class EmoticonEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The emoticon field cannot be empty' + self._fmt_request(kwargs['request']))


class EncryptedMessageInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Encrypted message invalid' + self._fmt_request(kwargs['request']))


class EncryptionAlreadyAcceptedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Secret chat already accepted' + self._fmt_request(kwargs['request']))


class EncryptionAlreadyDeclinedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The secret chat was already declined' + self._fmt_request(kwargs['request']))


class EncryptionDeclinedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The secret chat was declined' + self._fmt_request(kwargs['request']))


class EncryptionIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided secret chat ID is invalid' + self._fmt_request(kwargs['request']))


class EncryptionOccupyFailedError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('TDLib developer claimed it is not an error while accepting secret chats and 500 is used instead of 420' + self._fmt_request(kwargs['request']))


class EntitiesTooLongError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('It is no longer possible to send such long data inside entity tags (for example inline text URLs)' + self._fmt_request(kwargs['request']))


class EntityMentionUserInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("You can't use this entity" + self._fmt_request(kwargs['request']))


class ErrorTextEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided error message is empty' + self._fmt_request(kwargs['request']))


class ExportCardInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Provided card is invalid' + self._fmt_request(kwargs['request']))


class ExternalUrlInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('External URL invalid' + self._fmt_request(kwargs['request']))


class FieldNameEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The field with the name FIELD_NAME is missing' + self._fmt_request(kwargs['request']))


class FieldNameInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The field with the name FIELD_NAME is invalid' + self._fmt_request(kwargs['request']))


class FileIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided file id is invalid' + self._fmt_request(kwargs['request']))


class FileMigrateError(InvalidDCError):
    def __init__(self, **kwargs):
        self.new_dc = int(kwargs.get('capture', 0))
        super(Exception, self).__init__('The file to be accessed is currently stored in DC {new_dc}'.format(new_dc=self.new_dc) + self._fmt_request(kwargs['request']))


class FilePartsInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The number of file parts is invalid' + self._fmt_request(kwargs['request']))


class FilePart0MissingError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('File part 0 missing' + self._fmt_request(kwargs['request']))


class FilePartEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided file part is empty' + self._fmt_request(kwargs['request']))


class FilePartInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The file part number is invalid' + self._fmt_request(kwargs['request']))


class FilePartLengthInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The length of a file part is invalid' + self._fmt_request(kwargs['request']))


class FilePartSizeInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided file part size is invalid' + self._fmt_request(kwargs['request']))


class FilePartMissingError(BadRequestError):
    def __init__(self, **kwargs):
        self.which = int(kwargs.get('capture', 0))
        super(Exception, self).__init__('Part {which} of the file is missing from storage'.format(which=self.which) + self._fmt_request(kwargs['request']))


class FilerefUpgradeNeededError(AuthKeyError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The file reference needs to be refreshed before being used again' + self._fmt_request(kwargs['request']))


class FirstNameInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The first name is invalid' + self._fmt_request(kwargs['request']))


class FloodTestPhoneWaitError(FloodError):
    def __init__(self, **kwargs):
        self.seconds = int(kwargs.get('capture', 0))
        super(Exception, self).__init__('A wait of {seconds} seconds is required in the test servers'.format(seconds=self.seconds) + self._fmt_request(kwargs['request']))


class FloodWaitError(FloodError):
    def __init__(self, **kwargs):
        self.seconds = int(kwargs.get('capture', 0))
        super(Exception, self).__init__('A wait of {seconds} seconds is required'.format(seconds=self.seconds) + self._fmt_request(kwargs['request']))


class FolderIdEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The folder you tried to delete was already empty' + self._fmt_request(kwargs['request']))


class FolderIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The folder you tried to use was not valid' + self._fmt_request(kwargs['request']))


class FreshResetAuthorisationForbiddenError(AuthKeyError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The current session is too new and cannot be used to reset other authorisations yet' + self._fmt_request(kwargs['request']))


class GifIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided GIF ID is invalid' + self._fmt_request(kwargs['request']))


class GroupedMediaInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Invalid grouped media' + self._fmt_request(kwargs['request']))


class HashInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided hash is invalid' + self._fmt_request(kwargs['request']))


class HistoryGetFailedError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Fetching of history failed' + self._fmt_request(kwargs['request']))


class ImageProcessFailedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Failure while processing image' + self._fmt_request(kwargs['request']))


class InlineResultExpiredError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The inline query expired' + self._fmt_request(kwargs['request']))


class InputConstructorInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided constructor is invalid' + self._fmt_request(kwargs['request']))


class InputFetchErrorError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('An error occurred while deserializing TL parameters' + self._fmt_request(kwargs['request']))


class InputFetchFailError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Failed deserializing TL payload' + self._fmt_request(kwargs['request']))


class InputLayerInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided layer is invalid' + self._fmt_request(kwargs['request']))


class InputMethodInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The invoked method does not exist anymore or has never existed' + self._fmt_request(kwargs['request']))


class InputRequestTooLongError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The input request was too long. This may be a bug in the library as it can occur when serializing more bytes than it should (like appending the vector constructor code at the end of a message)' + self._fmt_request(kwargs['request']))


class InputUserDeactivatedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The specified user was deleted' + self._fmt_request(kwargs['request']))


class InterdcCallErrorError(BadRequestError):
    def __init__(self, **kwargs):
        self.dc = int(kwargs.get('capture', 0))
        super(Exception, self).__init__('An error occurred while communicating with DC {dc}'.format(dc=self.dc) + self._fmt_request(kwargs['request']))


class InterdcCallRichErrorError(BadRequestError):
    def __init__(self, **kwargs):
        self.dc = int(kwargs.get('capture', 0))
        super(Exception, self).__init__('A rich error occurred while communicating with DC {dc}'.format(dc=self.dc) + self._fmt_request(kwargs['request']))


class InviteHashEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The invite hash is empty' + self._fmt_request(kwargs['request']))


class InviteHashExpiredError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The chat the user tried to join has expired and is not valid anymore' + self._fmt_request(kwargs['request']))


class InviteHashInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The invite hash is invalid' + self._fmt_request(kwargs['request']))


class LangPackInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided language pack is invalid' + self._fmt_request(kwargs['request']))


class LastnameInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The last name is invalid' + self._fmt_request(kwargs['request']))


class LimitInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('An invalid limit was provided. See https://core.telegram.org/api/files#downloading-files' + self._fmt_request(kwargs['request']))


class LinkNotModifiedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The channel is already linked to this group' + self._fmt_request(kwargs['request']))


class LocationInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The location given for a file was invalid. See https://core.telegram.org/api/files#downloading-files' + self._fmt_request(kwargs['request']))


class MaxIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided max ID is invalid' + self._fmt_request(kwargs['request']))


class MaxQtsInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided QTS were invalid' + self._fmt_request(kwargs['request']))


class Md5ChecksumInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The MD5 check-sums do not match' + self._fmt_request(kwargs['request']))


class MediaCaptionTooLongError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The caption is too long' + self._fmt_request(kwargs['request']))


class MediaEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided media object is invalid' + self._fmt_request(kwargs['request']))


class MediaInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Media invalid' + self._fmt_request(kwargs['request']))


class MediaNewInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The new media to edit the message with is invalid (such as stickers or voice notes)' + self._fmt_request(kwargs['request']))


class MediaPrevInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The old media cannot be edited with anything else (such as stickers or voice notes)' + self._fmt_request(kwargs['request']))


class MegagroupIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The group is invalid' + self._fmt_request(kwargs['request']))


class MegagroupPrehistoryHiddenError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("You can't set this discussion group because it's history is hidden" + self._fmt_request(kwargs['request']))


class MemberNoLocationError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("An internal failure occurred while fetching user info (couldn't find location)" + self._fmt_request(kwargs['request']))


class MemberOccupyPrimaryLocFailedError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Occupation of primary member location failed' + self._fmt_request(kwargs['request']))


class MessageAuthorRequiredError(ForbiddenError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Message author required' + self._fmt_request(kwargs['request']))


class MessageDeleteForbiddenError(ForbiddenError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("You can't delete one of the messages you tried to delete, most likely because it is a service message." + self._fmt_request(kwargs['request']))


class MessageEditTimeExpiredError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("You can't edit this message anymore, too much time has passed since its creation." + self._fmt_request(kwargs['request']))


class MessageEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Empty or invalid UTF-8 message was sent' + self._fmt_request(kwargs['request']))


class MessageIdsEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('No message ids were provided' + self._fmt_request(kwargs['request']))


class MessageIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("The specified message ID is invalid or you can't do that operation on such message" + self._fmt_request(kwargs['request']))


class MessageNotModifiedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Content of the message was not modified' + self._fmt_request(kwargs['request']))


class MessageTooLongError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Message was too long. Current maximum length is 4096 UTF-8 characters' + self._fmt_request(kwargs['request']))


class MsgWaitFailedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('A waiting call returned an error' + self._fmt_request(kwargs['request']))


class MtSendQueueTooLongError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('' + self._fmt_request(kwargs['request']))


class NeedChatInvalidError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided chat is invalid' + self._fmt_request(kwargs['request']))


class NeedMemberInvalidError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided member is invalid or does not exist (for example a thumb size)' + self._fmt_request(kwargs['request']))


class NetworkMigrateError(InvalidDCError):
    def __init__(self, **kwargs):
        self.new_dc = int(kwargs.get('capture', 0))
        super(Exception, self).__init__('The source IP address is associated with DC {new_dc}'.format(new_dc=self.new_dc) + self._fmt_request(kwargs['request']))


class NewSaltInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The new salt is invalid' + self._fmt_request(kwargs['request']))


class NewSettingsInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The new settings are invalid' + self._fmt_request(kwargs['request']))


class OffsetInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The given offset was invalid, it must be divisible by 1KB. See https://core.telegram.org/api/files#downloading-files' + self._fmt_request(kwargs['request']))


class OffsetPeerIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided offset peer is invalid' + self._fmt_request(kwargs['request']))


class OptionsTooMuchError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('You defined too many options for the poll' + self._fmt_request(kwargs['request']))


class PackShortNameInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Invalid sticker pack name. It must begin with a letter, can\'t contain consecutive underscores and must end in "_by_<bot username>".' + self._fmt_request(kwargs['request']))


class PackShortNameOccupiedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('A stickerpack with this name already exists' + self._fmt_request(kwargs['request']))


class ParticipantsTooFewError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Not enough participants' + self._fmt_request(kwargs['request']))


class ParticipantCallFailedError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Failure while making call' + self._fmt_request(kwargs['request']))


class ParticipantVersionOutdatedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The other participant does not use an up to date telegram client with support for calls' + self._fmt_request(kwargs['request']))


class PasswordEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided password is empty' + self._fmt_request(kwargs['request']))


class PasswordHashInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The password (and thus its hash value) you entered is invalid' + self._fmt_request(kwargs['request']))


class PasswordRequiredError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The account must have 2-factor authentication enabled (a password) before this method can be used' + self._fmt_request(kwargs['request']))


class PaymentProviderInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The payment provider was not recognised or its token was invalid' + self._fmt_request(kwargs['request']))


class PeerFloodError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Too many requests' + self._fmt_request(kwargs['request']))


class PeerIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('An invalid Peer was used. Make sure to pass the right peer type' + self._fmt_request(kwargs['request']))


class PeerIdNotSupportedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided peer ID is not supported' + self._fmt_request(kwargs['request']))


class PersistentTimestampEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Persistent timestamp empty' + self._fmt_request(kwargs['request']))


class PersistentTimestampInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Persistent timestamp invalid' + self._fmt_request(kwargs['request']))


class PersistentTimestampOutdatedError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Persistent timestamp outdated' + self._fmt_request(kwargs['request']))


class PhoneCodeEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The phone code is missing' + self._fmt_request(kwargs['request']))


class PhoneCodeExpiredError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The confirmation code has expired' + self._fmt_request(kwargs['request']))


class PhoneCodeHashEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The phone code hash is missing' + self._fmt_request(kwargs['request']))


class PhoneCodeInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The phone code entered was invalid' + self._fmt_request(kwargs['request']))


class PhoneMigrateError(InvalidDCError):
    def __init__(self, **kwargs):
        self.new_dc = int(kwargs.get('capture', 0))
        super(Exception, self).__init__('The phone number a user is trying to use for authorization is associated with DC {new_dc}'.format(new_dc=self.new_dc) + self._fmt_request(kwargs['request']))


class PhoneNumberAppSignupForbiddenError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('' + self._fmt_request(kwargs['request']))


class PhoneNumberBannedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The used phone number has been banned from Telegram and cannot be used anymore. Maybe check https://www.telegram.org/faq_spam' + self._fmt_request(kwargs['request']))


class PhoneNumberFloodError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('You asked for the code too many times.' + self._fmt_request(kwargs['request']))


class PhoneNumberInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The phone number is invalid' + self._fmt_request(kwargs['request']))


class PhoneNumberOccupiedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The phone number is already in use' + self._fmt_request(kwargs['request']))


class PhoneNumberUnoccupiedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The phone number is not yet being used' + self._fmt_request(kwargs['request']))


class PhonePasswordFloodError(AuthKeyError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('You have tried logging in too many times' + self._fmt_request(kwargs['request']))


class PhonePasswordProtectedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('This phone is password protected' + self._fmt_request(kwargs['request']))


class PhotoContentUrlEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The content from the URL used as a photo appears to be empty or has caused another HTTP error' + self._fmt_request(kwargs['request']))


class PhotoCropSizeSmallError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Photo is too small' + self._fmt_request(kwargs['request']))


class PhotoExtInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The extension of the photo is invalid' + self._fmt_request(kwargs['request']))


class PhotoInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Photo invalid' + self._fmt_request(kwargs['request']))


class PhotoInvalidDimensionsError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The photo dimensions are invalid (hint: `pip install pillow` for `send_file` to resize images)' + self._fmt_request(kwargs['request']))


class PhotoSaveFileInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The photo you tried to send cannot be saved by Telegram. A reason may be that it exceeds 10MB. Try resizing it locally' + self._fmt_request(kwargs['request']))


class PhotoThumbUrlEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The URL used as a thumbnail appears to be empty or has caused another HTTP error' + self._fmt_request(kwargs['request']))


class PinRestrictedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("You can't pin messages in private chats with other people" + self._fmt_request(kwargs['request']))


class PollOptionDuplicateError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('A duplicate option was sent in the same poll' + self._fmt_request(kwargs['request']))


class PollUnsupportedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('This layer does not support polls in the issued method' + self._fmt_request(kwargs['request']))


class PrivacyKeyInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The privacy key is invalid' + self._fmt_request(kwargs['request']))


class PtsChangeEmptyError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('No PTS change' + self._fmt_request(kwargs['request']))


class QueryIdEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The query ID is empty' + self._fmt_request(kwargs['request']))


class QueryIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The query ID is invalid' + self._fmt_request(kwargs['request']))


class QueryTooShortError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The query string is too short' + self._fmt_request(kwargs['request']))


class RandomIdDuplicateError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('You provided a random ID that was already used' + self._fmt_request(kwargs['request']))


class RandomIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('A provided random ID is invalid' + self._fmt_request(kwargs['request']))


class RandomLengthInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Random length invalid' + self._fmt_request(kwargs['request']))


class RangesInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Invalid range provided' + self._fmt_request(kwargs['request']))


class ReactionInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Invalid reaction provided (only emoji are allowed)' + self._fmt_request(kwargs['request']))


class RegIdGenerateFailedError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Failure while generating registration ID' + self._fmt_request(kwargs['request']))


class ReplyMarkupInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided reply markup is invalid' + self._fmt_request(kwargs['request']))


class ReplyMarkupTooLongError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The data embedded in the reply markup buttons was too much' + self._fmt_request(kwargs['request']))


class ResultIdDuplicateError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Duplicated IDs on the sent results. Make sure to use unique IDs.' + self._fmt_request(kwargs['request']))


class ResultTypeInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Result type invalid' + self._fmt_request(kwargs['request']))


class ResultsTooMuchError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('You sent too many results. See https://core.telegram.org/bots/api#answerinlinequery for the current limit.' + self._fmt_request(kwargs['request']))


class RightForbiddenError(ForbiddenError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Either your admin rights do not allow you to do this or you passed the wrong rights combination (some rights only apply to channels and vice versa)' + self._fmt_request(kwargs['request']))


class RpcCallFailError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Telegram is having internal issues, please try again later.' + self._fmt_request(kwargs['request']))


class RpcMcgetFailError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Telegram is having internal issues, please try again later.' + self._fmt_request(kwargs['request']))


class RsaDecryptFailedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Internal RSA decryption failed' + self._fmt_request(kwargs['request']))


class ScheduleDateTooLateError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The date you tried to schedule is too far in the future (several years long)' + self._fmt_request(kwargs['request']))


class ScheduleTooMuchError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('You cannot schedule more messages in this chat (last known limit of 100 per chat)' + self._fmt_request(kwargs['request']))


class SearchQueryEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The search query is empty' + self._fmt_request(kwargs['request']))


class SecondsInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Slow mode only supports certain values (e.g. 0, 10s, 30s, 1m, 5m, 15m and 1h)' + self._fmt_request(kwargs['request']))


class SendMessageMediaInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The message media was invalid or not specified' + self._fmt_request(kwargs['request']))


class SendMessageTypeInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The message type is invalid' + self._fmt_request(kwargs['request']))


class SessionExpiredError(UnauthorizedError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The authorization has expired' + self._fmt_request(kwargs['request']))


class SessionPasswordNeededError(UnauthorizedError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Two-steps verification is enabled and a password is required' + self._fmt_request(kwargs['request']))


class SessionRevokedError(UnauthorizedError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The authorization has been invalidated, because of the user terminating all sessions' + self._fmt_request(kwargs['request']))


class Sha256HashInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided SHA256 hash is invalid' + self._fmt_request(kwargs['request']))


class ShortnameOccupyFailedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('An error occurred when trying to register the short-name used for the sticker pack. Try a different name' + self._fmt_request(kwargs['request']))


class StartParamEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The start parameter is empty' + self._fmt_request(kwargs['request']))


class StartParamInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Start parameter invalid' + self._fmt_request(kwargs['request']))


class StickersetInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided sticker set is invalid' + self._fmt_request(kwargs['request']))


class StickersEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('No sticker provided' + self._fmt_request(kwargs['request']))


class StickerEmojiInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Sticker emoji invalid' + self._fmt_request(kwargs['request']))


class StickerFileInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Sticker file invalid' + self._fmt_request(kwargs['request']))


class StickerIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided sticker ID is invalid' + self._fmt_request(kwargs['request']))


class StickerInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided sticker is invalid' + self._fmt_request(kwargs['request']))


class StickerPngDimensionsError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Sticker png dimensions invalid' + self._fmt_request(kwargs['request']))


class StorageCheckFailedError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Server storage check failed' + self._fmt_request(kwargs['request']))


class StoreInvalidScalarTypeError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('' + self._fmt_request(kwargs['request']))


class TakeoutInitDelayError(FloodError):
    def __init__(self, **kwargs):
        self.seconds = int(kwargs.get('capture', 0))
        super(Exception, self).__init__('A wait of {seconds} seconds is required before being able to initiate the takeout'.format(seconds=self.seconds) + self._fmt_request(kwargs['request']))


class TakeoutInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The takeout session has been invalidated by another data export session' + self._fmt_request(kwargs['request']))


class TakeoutRequiredError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('You must initialize a takeout request first' + self._fmt_request(kwargs['request']))


class TempAuthKeyEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('No temporary auth key provided' + self._fmt_request(kwargs['request']))


class TimeoutError(TimedOutError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('A timeout occurred while fetching data from the bot' + self._fmt_request(kwargs['request']))


class TmpPasswordDisabledError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The temporary password is disabled' + self._fmt_request(kwargs['request']))


class TokenInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided token is invalid' + self._fmt_request(kwargs['request']))


class TtlDaysInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided TTL is invalid' + self._fmt_request(kwargs['request']))


class TypesEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The types field is empty' + self._fmt_request(kwargs['request']))


class TypeConstructorInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The type constructor is invalid' + self._fmt_request(kwargs['request']))


class UnknownMethodError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The method you tried to call cannot be called on non-CDN DCs' + self._fmt_request(kwargs['request']))


class UntilDateInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('That date cannot be specified in this request (try using None)' + self._fmt_request(kwargs['request']))


class UrlInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("The URL used was invalid (e.g. when answering a callback with an URL that's not t.me/yourbot or your game's URL)" + self._fmt_request(kwargs['request']))


class UsernameInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Nobody is using this username, or the username is unacceptable. If the latter, it must match r"[a-zA-Z][\\w\\d]{3,30}[a-zA-Z\\d]"' + self._fmt_request(kwargs['request']))


class UsernameNotModifiedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The username is not different from the current username' + self._fmt_request(kwargs['request']))


class UsernameNotOccupiedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The username is not in use by anyone else yet' + self._fmt_request(kwargs['request']))


class UsernameOccupiedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The username is already taken' + self._fmt_request(kwargs['request']))


class UsersTooFewError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Not enough users (to create a chat, for example)' + self._fmt_request(kwargs['request']))


class UsersTooMuchError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The maximum number of users has been exceeded (to create a chat, for example)' + self._fmt_request(kwargs['request']))


class UserAdminInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("Either you're not an admin or you tried to ban an admin that you didn't promote" + self._fmt_request(kwargs['request']))


class UserAlreadyParticipantError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The authenticated user is already a participant of the chat' + self._fmt_request(kwargs['request']))


class UserBannedInChannelError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("You're banned from sending messages in supergroups/channels" + self._fmt_request(kwargs['request']))


class UserBlockedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('User blocked' + self._fmt_request(kwargs['request']))


class UserBotError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Bots can only be admins in channels.' + self._fmt_request(kwargs['request']))


class UserBotInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('This method can only be called by a bot' + self._fmt_request(kwargs['request']))


class UserBotRequiredError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('This method can only be called by a bot' + self._fmt_request(kwargs['request']))


class UserChannelsTooMuchError(ForbiddenError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('One of the users you tried to add is already in too many channels/supergroups' + self._fmt_request(kwargs['request']))


class UserCreatorError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("You can't leave this channel, because you're its creator" + self._fmt_request(kwargs['request']))


class UserDeactivatedError(UnauthorizedError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The user has been deleted/deactivated' + self._fmt_request(kwargs['request']))


class UserDeactivatedBanError(UnauthorizedError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The user has been deleted/deactivated' + self._fmt_request(kwargs['request']))


class UserIdInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Invalid object ID for a user. Make sure to pass the right types, for instance making sure that the request is designed for users or otherwise look for a different one more suited' + self._fmt_request(kwargs['request']))


class UserInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The given user was invalid' + self._fmt_request(kwargs['request']))


class UserIsBlockedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('User is blocked' + self._fmt_request(kwargs['request']))


class UserIsBotError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("Bots can't send messages to other bots" + self._fmt_request(kwargs['request']))


class UserKickedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('This user was kicked from this supergroup/channel' + self._fmt_request(kwargs['request']))


class UserMigrateError(InvalidDCError):
    def __init__(self, **kwargs):
        self.new_dc = int(kwargs.get('capture', 0))
        super(Exception, self).__init__('The user whose identity is being used to execute queries is associated with DC {new_dc}'.format(new_dc=self.new_dc) + self._fmt_request(kwargs['request']))


class UserNotMutualContactError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The provided user is not a mutual contact' + self._fmt_request(kwargs['request']))


class UserNotParticipantError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The target user is not a member of the specified megagroup or channel' + self._fmt_request(kwargs['request']))


class UserPrivacyRestrictedError(ForbiddenError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("The user's privacy settings do not allow you to do this" + self._fmt_request(kwargs['request']))


class UserRestrictedError(ForbiddenError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__("You're spamreported, you can't create channels or chats." + self._fmt_request(kwargs['request']))


class VideoContentTypeInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The video content type is not supported with the given parameters (i.e. supports_streaming)' + self._fmt_request(kwargs['request']))


class WallpaperFileInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The given file cannot be used as a wallpaper' + self._fmt_request(kwargs['request']))


class WallpaperInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('The input wallpaper was not valid' + self._fmt_request(kwargs['request']))


class WcConvertUrlInvalidError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('WC convert URL invalid' + self._fmt_request(kwargs['request']))


class WebpageCurlFailedError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Failure while fetching the webpage with cURL' + self._fmt_request(kwargs['request']))


class WebpageMediaEmptyError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Webpage media empty' + self._fmt_request(kwargs['request']))


class WorkerBusyTooLongRetryError(ServerError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('Telegram workers are too busy to respond immediately' + self._fmt_request(kwargs['request']))


class YouBlockedUserError(BadRequestError):
    def __init__(self, **kwargs):
        super(Exception, self).__init__('You blocked this user' + self._fmt_request(kwargs['request']))


rpc_errors_dict = {
    'ABOUT_TOO_LONG': AboutTooLongError,
    'ACCESS_TOKEN_EXPIRED': AccessTokenExpiredError,
    'ACCESS_TOKEN_INVALID': AccessTokenInvalidError,
    'ACTIVE_USER_REQUIRED': ActiveUserRequiredError,
    'ADMINS_TOO_MUCH': AdminsTooMuchError,
    'ADMIN_RANK_EMOJI_NOT_ALLOWED': AdminRankEmojiNotAllowedError,
    'ADMIN_RANK_INVALID': AdminRankInvalidError,
    'API_ID_INVALID': ApiIdInvalidError,
    'API_ID_PUBLISHED_FLOOD': ApiIdPublishedFloodError,
    'ARTICLE_TITLE_EMPTY': ArticleTitleEmptyError,
    'AUTH_BYTES_INVALID': AuthBytesInvalidError,
    'AUTH_KEY_DUPLICATED': AuthKeyDuplicatedError,
    'AUTH_KEY_INVALID': AuthKeyInvalidError,
    'AUTH_KEY_PERM_EMPTY': AuthKeyPermEmptyError,
    'AUTH_KEY_UNREGISTERED': AuthKeyUnregisteredError,
    'AUTH_RESTART': AuthRestartError,
    'BANNED_RIGHTS_INVALID': BannedRightsInvalidError,
    'BOTS_TOO_MUCH': BotsTooMuchError,
    'BOT_CHANNELS_NA': BotChannelsNaError,
    'BOT_GROUPS_BLOCKED': BotGroupsBlockedError,
    'BOT_INLINE_DISABLED': BotInlineDisabledError,
    'BOT_INVALID': BotInvalidError,
    'BOT_METHOD_INVALID': BotMethodInvalidError,
    'BOT_MISSING': BotMissingError,
    'BOT_PAYMENTS_DISABLED': BotPaymentsDisabledError,
    'BOT_POLLS_DISABLED': BotPollsDisabledError,
    'BROADCAST_ID_INVALID': BroadcastIdInvalidError,
    'BUTTON_DATA_INVALID': ButtonDataInvalidError,
    'BUTTON_TYPE_INVALID': ButtonTypeInvalidError,
    'BUTTON_URL_INVALID': ButtonUrlInvalidError,
    'CALL_ALREADY_ACCEPTED': CallAlreadyAcceptedError,
    'CALL_ALREADY_DECLINED': CallAlreadyDeclinedError,
    'CALL_OCCUPY_FAILED': CallOccupyFailedError,
    'CALL_PEER_INVALID': CallPeerInvalidError,
    'CALL_PROTOCOL_FLAGS_INVALID': CallProtocolFlagsInvalidError,
    'CDN_METHOD_INVALID': CdnMethodInvalidError,
    'CHANNELS_ADMIN_PUBLIC_TOO_MUCH': ChannelsAdminPublicTooMuchError,
    'CHANNELS_TOO_MUCH': ChannelsTooMuchError,
    'CHANNEL_INVALID': ChannelInvalidError,
    'CHANNEL_PRIVATE': ChannelPrivateError,
    'CHANNEL_PUBLIC_GROUP_NA': ChannelPublicGroupNaError,
    'CHAT_ABOUT_NOT_MODIFIED': ChatAboutNotModifiedError,
    'CHAT_ABOUT_TOO_LONG': ChatAboutTooLongError,
    'CHAT_ADMIN_INVITE_REQUIRED': ChatAdminInviteRequiredError,
    'CHAT_ADMIN_REQUIRED': ChatAdminRequiredError,
    'CHAT_FORBIDDEN': ChatForbiddenError,
    'CHAT_ID_EMPTY': ChatIdEmptyError,
    'CHAT_ID_INVALID': ChatIdInvalidError,
    'CHAT_INVALID': ChatInvalidError,
    'CHAT_LINK_EXISTS': ChatLinkExistsError,
    'CHAT_NOT_MODIFIED': ChatNotModifiedError,
    'CHAT_RESTRICTED': ChatRestrictedError,
    'CHAT_SEND_GIFS_FORBIDDEN': ChatSendGifsForbiddenError,
    'CHAT_SEND_INLINE_FORBIDDEN': ChatSendInlineForbiddenError,
    'CHAT_SEND_MEDIA_FORBIDDEN': ChatSendMediaForbiddenError,
    'CHAT_SEND_STICKERS_FORBIDDEN': ChatSendStickersForbiddenError,
    'CHAT_TITLE_EMPTY': ChatTitleEmptyError,
    'CHAT_WRITE_FORBIDDEN': ChatWriteForbiddenError,
    'CODE_EMPTY': CodeEmptyError,
    'CODE_HASH_INVALID': CodeHashInvalidError,
    'CODE_INVALID': CodeInvalidError,
    'CONNECTION_API_ID_INVALID': ConnectionApiIdInvalidError,
    'CONNECTION_DEVICE_MODEL_EMPTY': ConnectionDeviceModelEmptyError,
    'CONNECTION_LANG_PACK_INVALID': ConnectionLangPackInvalidError,
    'CONNECTION_LAYER_INVALID': ConnectionLayerInvalidError,
    'CONNECTION_NOT_INITED': ConnectionNotInitedError,
    'CONNECTION_SYSTEM_EMPTY': ConnectionSystemEmptyError,
    'CONTACT_ID_INVALID': ContactIdInvalidError,
    'DATA_INVALID': DataInvalidError,
    'DATA_JSON_INVALID': DataJsonInvalidError,
    'DATE_EMPTY': DateEmptyError,
    'DC_ID_INVALID': DcIdInvalidError,
    'DH_G_A_INVALID': DhGAInvalidError,
    'EMAIL_HASH_EXPIRED': EmailHashExpiredError,
    'EMAIL_INVALID': EmailInvalidError,
    'EMOTICON_EMPTY': EmoticonEmptyError,
    'ENCRYPTED_MESSAGE_INVALID': EncryptedMessageInvalidError,
    'ENCRYPTION_ALREADY_ACCEPTED': EncryptionAlreadyAcceptedError,
    'ENCRYPTION_ALREADY_DECLINED': EncryptionAlreadyDeclinedError,
    'ENCRYPTION_DECLINED': EncryptionDeclinedError,
    'ENCRYPTION_ID_INVALID': EncryptionIdInvalidError,
    'ENCRYPTION_OCCUPY_FAILED': EncryptionOccupyFailedError,
    'ENTITIES_TOO_LONG': EntitiesTooLongError,
    'ENTITY_MENTION_USER_INVALID': EntityMentionUserInvalidError,
    'ERROR_TEXT_EMPTY': ErrorTextEmptyError,
    'EXPORT_CARD_INVALID': ExportCardInvalidError,
    'EXTERNAL_URL_INVALID': ExternalUrlInvalidError,
    'FIELD_NAME_EMPTY': FieldNameEmptyError,
    'FIELD_NAME_INVALID': FieldNameInvalidError,
    'FILE_ID_INVALID': FileIdInvalidError,
    'FILE_PARTS_INVALID': FilePartsInvalidError,
    'FILE_PART_0_MISSING': FilePart0MissingError,
    'FILE_PART_EMPTY': FilePartEmptyError,
    'FILE_PART_INVALID': FilePartInvalidError,
    'FILE_PART_LENGTH_INVALID': FilePartLengthInvalidError,
    'FILE_PART_SIZE_INVALID': FilePartSizeInvalidError,
    'FILEREF_UPGRADE_NEEDED': FilerefUpgradeNeededError,
    'FIRSTNAME_INVALID': FirstNameInvalidError,
    'FOLDER_ID_EMPTY': FolderIdEmptyError,
    'FOLDER_ID_INVALID': FolderIdInvalidError,
    'FRESH_RESET_AUTHORISATION_FORBIDDEN': FreshResetAuthorisationForbiddenError,
    'GIF_ID_INVALID': GifIdInvalidError,
    'GROUPED_MEDIA_INVALID': GroupedMediaInvalidError,
    'HASH_INVALID': HashInvalidError,
    'HISTORY_GET_FAILED': HistoryGetFailedError,
    'IMAGE_PROCESS_FAILED': ImageProcessFailedError,
    'INLINE_RESULT_EXPIRED': InlineResultExpiredError,
    'INPUT_CONSTRUCTOR_INVALID': InputConstructorInvalidError,
    'INPUT_FETCH_ERROR': InputFetchErrorError,
    'INPUT_FETCH_FAIL': InputFetchFailError,
    'INPUT_LAYER_INVALID': InputLayerInvalidError,
    'INPUT_METHOD_INVALID': InputMethodInvalidError,
    'INPUT_REQUEST_TOO_LONG': InputRequestTooLongError,
    'INPUT_USER_DEACTIVATED': InputUserDeactivatedError,
    'INVITE_HASH_EMPTY': InviteHashEmptyError,
    'INVITE_HASH_EXPIRED': InviteHashExpiredError,
    'INVITE_HASH_INVALID': InviteHashInvalidError,
    'LANG_PACK_INVALID': LangPackInvalidError,
    'LASTNAME_INVALID': LastnameInvalidError,
    'LIMIT_INVALID': LimitInvalidError,
    'LINK_NOT_MODIFIED': LinkNotModifiedError,
    'LOCATION_INVALID': LocationInvalidError,
    'MAX_ID_INVALID': MaxIdInvalidError,
    'MAX_QTS_INVALID': MaxQtsInvalidError,
    'MD5_CHECKSUM_INVALID': Md5ChecksumInvalidError,
    'MEDIA_CAPTION_TOO_LONG': MediaCaptionTooLongError,
    'MEDIA_EMPTY': MediaEmptyError,
    'MEDIA_INVALID': MediaInvalidError,
    'MEDIA_NEW_INVALID': MediaNewInvalidError,
    'MEDIA_PREV_INVALID': MediaPrevInvalidError,
    'MEGAGROUP_ID_INVALID': MegagroupIdInvalidError,
    'MEGAGROUP_PREHISTORY_HIDDEN': MegagroupPrehistoryHiddenError,
    'MEMBER_NO_LOCATION': MemberNoLocationError,
    'MEMBER_OCCUPY_PRIMARY_LOC_FAILED': MemberOccupyPrimaryLocFailedError,
    'MESSAGE_AUTHOR_REQUIRED': MessageAuthorRequiredError,
    'MESSAGE_DELETE_FORBIDDEN': MessageDeleteForbiddenError,
    'MESSAGE_EDIT_TIME_EXPIRED': MessageEditTimeExpiredError,
    'MESSAGE_EMPTY': MessageEmptyError,
    'MESSAGE_IDS_EMPTY': MessageIdsEmptyError,
    'MESSAGE_ID_INVALID': MessageIdInvalidError,
    'MESSAGE_NOT_MODIFIED': MessageNotModifiedError,
    'MESSAGE_TOO_LONG': MessageTooLongError,
    'MSG_WAIT_FAILED': MsgWaitFailedError,
    'MT_SEND_QUEUE_TOO_LONG': MtSendQueueTooLongError,
    'NEED_CHAT_INVALID': NeedChatInvalidError,
    'NEED_MEMBER_INVALID': NeedMemberInvalidError,
    'NEW_SALT_INVALID': NewSaltInvalidError,
    'NEW_SETTINGS_INVALID': NewSettingsInvalidError,
    'OFFSET_INVALID': OffsetInvalidError,
    'OFFSET_PEER_ID_INVALID': OffsetPeerIdInvalidError,
    'OPTIONS_TOO_MUCH': OptionsTooMuchError,
    'PACK_SHORT_NAME_INVALID': PackShortNameInvalidError,
    'PACK_SHORT_NAME_OCCUPIED': PackShortNameOccupiedError,
    'PARTICIPANTS_TOO_FEW': ParticipantsTooFewError,
    'PARTICIPANT_CALL_FAILED': ParticipantCallFailedError,
    'PARTICIPANT_VERSION_OUTDATED': ParticipantVersionOutdatedError,
    'PASSWORD_EMPTY': PasswordEmptyError,
    'PASSWORD_HASH_INVALID': PasswordHashInvalidError,
    'PASSWORD_REQUIRED': PasswordRequiredError,
    'PAYMENT_PROVIDER_INVALID': PaymentProviderInvalidError,
    'PEER_FLOOD': PeerFloodError,
    'PEER_ID_INVALID': PeerIdInvalidError,
    'PEER_ID_NOT_SUPPORTED': PeerIdNotSupportedError,
    'PERSISTENT_TIMESTAMP_EMPTY': PersistentTimestampEmptyError,
    'PERSISTENT_TIMESTAMP_INVALID': PersistentTimestampInvalidError,
    'PERSISTENT_TIMESTAMP_OUTDATED': PersistentTimestampOutdatedError,
    'PHONE_CODE_EMPTY': PhoneCodeEmptyError,
    'PHONE_CODE_EXPIRED': PhoneCodeExpiredError,
    'PHONE_CODE_HASH_EMPTY': PhoneCodeHashEmptyError,
    'PHONE_CODE_INVALID': PhoneCodeInvalidError,
    'PHONE_NUMBER_APP_SIGNUP_FORBIDDEN': PhoneNumberAppSignupForbiddenError,
    'PHONE_NUMBER_BANNED': PhoneNumberBannedError,
    'PHONE_NUMBER_FLOOD': PhoneNumberFloodError,
    'PHONE_NUMBER_INVALID': PhoneNumberInvalidError,
    'PHONE_NUMBER_OCCUPIED': PhoneNumberOccupiedError,
    'PHONE_NUMBER_UNOCCUPIED': PhoneNumberUnoccupiedError,
    'PHONE_PASSWORD_FLOOD': PhonePasswordFloodError,
    'PHONE_PASSWORD_PROTECTED': PhonePasswordProtectedError,
    'PHOTO_CONTENT_URL_EMPTY': PhotoContentUrlEmptyError,
    'PHOTO_CROP_SIZE_SMALL': PhotoCropSizeSmallError,
    'PHOTO_EXT_INVALID': PhotoExtInvalidError,
    'PHOTO_INVALID': PhotoInvalidError,
    'PHOTO_INVALID_DIMENSIONS': PhotoInvalidDimensionsError,
    'PHOTO_SAVE_FILE_INVALID': PhotoSaveFileInvalidError,
    'PHOTO_THUMB_URL_EMPTY': PhotoThumbUrlEmptyError,
    'PIN_RESTRICTED': PinRestrictedError,
    'POLL_OPTION_DUPLICATE': PollOptionDuplicateError,
    'POLL_UNSUPPORTED': PollUnsupportedError,
    'PRIVACY_KEY_INVALID': PrivacyKeyInvalidError,
    'PTS_CHANGE_EMPTY': PtsChangeEmptyError,
    'QUERY_ID_EMPTY': QueryIdEmptyError,
    'QUERY_ID_INVALID': QueryIdInvalidError,
    'QUERY_TOO_SHORT': QueryTooShortError,
    'RANDOM_ID_DUPLICATE': RandomIdDuplicateError,
    'RANDOM_ID_INVALID': RandomIdInvalidError,
    'RANDOM_LENGTH_INVALID': RandomLengthInvalidError,
    'RANGES_INVALID': RangesInvalidError,
    'REACTION_INVALID': ReactionInvalidError,
    'REG_ID_GENERATE_FAILED': RegIdGenerateFailedError,
    'REPLY_MARKUP_INVALID': ReplyMarkupInvalidError,
    'REPLY_MARKUP_TOO_LONG': ReplyMarkupTooLongError,
    'RESULT_ID_DUPLICATE': ResultIdDuplicateError,
    'RESULT_TYPE_INVALID': ResultTypeInvalidError,
    'RESULTS_TOO_MUCH': ResultsTooMuchError,
    'RIGHT_FORBIDDEN': RightForbiddenError,
    'RPC_CALL_FAIL': RpcCallFailError,
    'RPC_MCGET_FAIL': RpcMcgetFailError,
    'RSA_DECRYPT_FAILED': RsaDecryptFailedError,
    'SCHEDULE_DATE_TOO_LATE': ScheduleDateTooLateError,
    'SCHEDULE_TOO_MUCH': ScheduleTooMuchError,
    'SEARCH_QUERY_EMPTY': SearchQueryEmptyError,
    'SECONDS_INVALID': SecondsInvalidError,
    'SEND_MESSAGE_MEDIA_INVALID': SendMessageMediaInvalidError,
    'SEND_MESSAGE_TYPE_INVALID': SendMessageTypeInvalidError,
    'SESSION_EXPIRED': SessionExpiredError,
    'SESSION_PASSWORD_NEEDED': SessionPasswordNeededError,
    'SESSION_REVOKED': SessionRevokedError,
    'SHA256_HASH_INVALID': Sha256HashInvalidError,
    'SHORTNAME_OCCUPY_FAILED': ShortnameOccupyFailedError,
    'START_PARAM_EMPTY': StartParamEmptyError,
    'START_PARAM_INVALID': StartParamInvalidError,
    'STICKERSET_INVALID': StickersetInvalidError,
    'STICKERS_EMPTY': StickersEmptyError,
    'STICKER_EMOJI_INVALID': StickerEmojiInvalidError,
    'STICKER_FILE_INVALID': StickerFileInvalidError,
    'STICKER_ID_INVALID': StickerIdInvalidError,
    'STICKER_INVALID': StickerInvalidError,
    'STICKER_PNG_DIMENSIONS': StickerPngDimensionsError,
    'STORAGE_CHECK_FAILED': StorageCheckFailedError,
    'STORE_INVALID_SCALAR_TYPE': StoreInvalidScalarTypeError,
    'TAKEOUT_INVALID': TakeoutInvalidError,
    'TAKEOUT_REQUIRED': TakeoutRequiredError,
    'TEMP_AUTH_KEY_EMPTY': TempAuthKeyEmptyError,
    'Timeout': TimeoutError,
    'TMP_PASSWORD_DISABLED': TmpPasswordDisabledError,
    'TOKEN_INVALID': TokenInvalidError,
    'TTL_DAYS_INVALID': TtlDaysInvalidError,
    'TYPES_EMPTY': TypesEmptyError,
    'TYPE_CONSTRUCTOR_INVALID': TypeConstructorInvalidError,
    'UNKNOWN_METHOD': UnknownMethodError,
    'UNTIL_DATE_INVALID': UntilDateInvalidError,
    'URL_INVALID': UrlInvalidError,
    'USERNAME_INVALID': UsernameInvalidError,
    'USERNAME_NOT_MODIFIED': UsernameNotModifiedError,
    'USERNAME_NOT_OCCUPIED': UsernameNotOccupiedError,
    'USERNAME_OCCUPIED': UsernameOccupiedError,
    'USERS_TOO_FEW': UsersTooFewError,
    'USERS_TOO_MUCH': UsersTooMuchError,
    'USER_ADMIN_INVALID': UserAdminInvalidError,
    'USER_ALREADY_PARTICIPANT': UserAlreadyParticipantError,
    'USER_BANNED_IN_CHANNEL': UserBannedInChannelError,
    'USER_BLOCKED': UserBlockedError,
    'USER_BOT': UserBotError,
    'USER_BOT_INVALID': UserBotInvalidError,
    'USER_BOT_REQUIRED': UserBotRequiredError,
    'USER_CHANNELS_TOO_MUCH': UserChannelsTooMuchError,
    'USER_CREATOR': UserCreatorError,
    'USER_DEACTIVATED': UserDeactivatedError,
    'USER_DEACTIVATED_BAN': UserDeactivatedBanError,
    'USER_ID_INVALID': UserIdInvalidError,
    'USER_INVALID': UserInvalidError,
    'USER_IS_BLOCKED': UserIsBlockedError,
    'USER_IS_BOT': UserIsBotError,
    'USER_KICKED': UserKickedError,
    'USER_NOT_MUTUAL_CONTACT': UserNotMutualContactError,
    'USER_NOT_PARTICIPANT': UserNotParticipantError,
    'USER_PRIVACY_RESTRICTED': UserPrivacyRestrictedError,
    'USER_RESTRICTED': UserRestrictedError,
    'VIDEO_CONTENT_TYPE_INVALID': VideoContentTypeInvalidError,
    'WALLPAPER_FILE_INVALID': WallpaperFileInvalidError,
    'WALLPAPER_INVALID': WallpaperInvalidError,
    'WC_CONVERT_URL_INVALID': WcConvertUrlInvalidError,
    'WEBPAGE_CURL_FAILED': WebpageCurlFailedError,
    'WEBPAGE_MEDIA_EMPTY': WebpageMediaEmptyError,
    'WORKER_BUSY_TOO_LONG_RETRY': WorkerBusyTooLongRetryError,
    'YOU_BLOCKED_USER': YouBlockedUserError,
}

rpc_errors_re = (
    ('EMAIL_UNCONFIRMED_(\\d+)', EmailUnconfirmedError),
    ('FILE_MIGRATE_(\\d+)', FileMigrateError),
    ('FILE_PART_(\\d+)_MISSING', FilePartMissingError),
    ('FLOOD_TEST_PHONE_WAIT_(\\d+)', FloodTestPhoneWaitError),
    ('FLOOD_WAIT_(\\d+)', FloodWaitError),
    ('INTERDC_(\\d+)_CALL_ERROR', InterdcCallErrorError),
    ('INTERDC_(\\d+)_CALL_RICH_ERROR', InterdcCallRichErrorError),
    ('NETWORK_MIGRATE_(\\d+)', NetworkMigrateError),
    ('PHONE_MIGRATE_(\\d+)', PhoneMigrateError),
    ('TAKEOUT_INIT_DELAY_(\\d+)', TakeoutInitDelayError),
    ('USER_MIGRATE_(\\d+)', UserMigrateError),
)
