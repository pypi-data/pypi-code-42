import codecs
import json
import logging
import time
from collections import namedtuple
from functools import wraps

from minty import Base
from pyramid.httpexceptions import HTTPForbidden, HTTPUnauthorized
from redis import StrictRedis


class SessionRetrieverError(Exception):
    """Base for session retrieval related exceptions."""

    pass


class SessionNotFoundError(SessionRetrieverError, ValueError):
    """Session can't be found in Redis."""

    pass


class SessionDataNotFoundError(SessionRetrieverError, ValueError):
    """Session data can't be found in Redis."""

    pass


class SessionRetriever(Base):
    """HTTP session retriever.

    retrieves a session stored by the Perl application from the Redis store
    """

    __slots__ = ["redis", "decoder"]

    def __init__(self, redis: StrictRedis):
        """Initialize a HTTP session retriever.

        :param redis: Redis connection object to retrieve session data
        :type redis: StrictRedis
        """
        self.redis = redis

    def retrieve(self, session_id: str) -> dict:
        """Retrieve a session from Redis.

        :param session_id: session id to retrieve
        :type session_id: str
        :raises SessionNotFoundError: if the session cannot be found
        :raises SessionDataNotFoundError: if the session is found, but contains
                                          no data
        :return: the session data
        :rtype: dict
        """
        now = time.time()
        with self.statsd.get_timer("retrieve").time("total_time"):
            with self.statsd.get_timer("retrieve").time(
                "redis.get_expires.time"
            ):
                expiration = self.redis.get(f"expires:{session_id}")

            if expiration is None:
                self.logger.info(f"Session '{session_id}' not found")
                self.statsd.get_counter("retrieve").increment(
                    "redis.get_session.not_found.count"
                )
                raise SessionNotFoundError(session_id)

            if float(expiration) < now:
                self.logger.info(f"Session '{session_id}' has expired")
                self.statsd.get_counter("retrieve").increment(
                    "redis.get_session.not_found.count"
                )
                raise SessionNotFoundError(session_id)

            with self.statsd.get_timer("retrieve").time(
                "redis.get_session.time"
            ):
                session_data_raw = self.redis.get(f"json:session:{session_id}")

            if session_data_raw is None:
                self.logger.info(f"Session '{session_id}' not found")
                self.statsd.get_counter("retrieve").increment(
                    "redis.get_session.not_found.count"
                )
                raise SessionDataNotFoundError(session_id)

            session_data_decoded = codecs.decode(session_data_raw, "base64")
            session_data = json.loads(session_data_decoded)

            self.statsd.get_counter("retrieve").increment(
                "redis.get_session.count"
            )
            self.logger.info(f"Session '{session_id}' retrieved")

            return session_data


def redis_from_config(config: dict) -> StrictRedis:
    """Create a Redis cleint from variables in the config parameter.

    :param config: config variables
    :type config: dict
    :return: configured redis client
    :rtype: StrictRedis
    """
    redis_conf = config["redis"]["session"]

    redis = StrictRedis(**redis_conf)
    return redis


def session_manager_factory(infra_factory):
    """Create a configured SessionRetriever class.

    :param infra_factory: infrastructure factory class
    :type infra_factory: InfrastructureFactory
    :return: configured SessionRetriever class to retrieve session information
        from session store
    :rtype: SessionRetriever
    """
    infra_factory.register_infrastructure(
        name="redis", infrastructure=redis_from_config
    )
    redis = infra_factory.get_infrastructure(
        context=None, infrastructure_name="redis"
    )
    return SessionRetriever(redis)


UserInfo = namedtuple("UserInfo", "user_uuid permissions")


def protected_route(permission="gebruiker", *args):
    """Check session and inject `UserInfo` in wrapped view .

    zaaksysteem_session cookie is checked for validity and `UserInfo` is
    injected in the view.

    :param view: view function
    :type view: pyramid view
    :raises HTTPUnauthorized: session not valid or non-existant
    :return: view with `UserInfo` injected
    :rtype: wrapped view
    """
    permission_list = [permission, *args]

    def protected_view_wrapper(view):
        @wraps(view)
        def view_wrapper(request):
            logger = logging.getLogger(view.__name__)
            try:
                session_data = request.retrieve_session()
            except (SessionRetrieverError, KeyError) as e:
                logger.info(f"Invalid session: '{e}'")
                raise HTTPUnauthorized(
                    content_type="application/json",
                    json_body={"error": "Unauthorized"},
                )

            user_info = handle_session_data(
                session_data=session_data, logger=logger
            )

            # User permissions will be set on login, based on a table of roles
            # and access rights.
            #
            # This generally means someone with "admin" rights will also have
            # the other permissions set, for instance.
            for perm in permission_list:
                if user_info.permissions.get(perm, False) is True:
                    return view(request=request, user_info=user_info)

            raise HTTPForbidden(
                json={"error": "You do not have permission to access this."}
            )

        return view_wrapper

    return protected_view_wrapper


def handle_session_data(session_data: dict, logger) -> UserInfo:
    """Handle session data for different types of users.

    Current users: zaaksyteem user & pip_user

    :param session_data: session
    :type session_data: dict
    :param logger: logger
    :type logger: Logger
    :raises HTTPUnauthorized: if user is not Authorized
    :return: user_info object
    :rtype: UserInfo
    """
    try:
        user_info_raw = session_data.get("__user", False)
        if user_info_raw:
            user_info_decoded = json.loads(user_info_raw)
            user_info = UserInfo(
                user_uuid=user_info_decoded["subject_uuid"],
                permissions=user_info_decoded["permissions"],
            )
            return user_info

        user_info_pip = session_data.get("pip", False)
        if user_info_pip:
            user_info = UserInfo(
                user_uuid=user_info_pip["user_uuid"],
                permissions={"pip_user": True},
            )
            return user_info
    except KeyError as e:
        logger.info(f"Unauthorized: error in session data: '{e}'")
        raise HTTPUnauthorized(
            content_type="application/json",
            json_body={"error": "Unauthorized"},
        )
    except TypeError as e:
        logger.info(f"Unauthorized: error in session data: '{e}'")
        raise HTTPUnauthorized(
            content_type="application/json",
            json_body={"error": "Unauthorized"},
        )

    raise HTTPUnauthorized(
        content_type="application/json", json_body={"error": "Unauthorized"}
    )
