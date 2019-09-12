import asyncio
from unittest import TestCase

from piccolo.extensions.user import BaseUser


class TestCreateUserTable(TestCase):
    def test_create_user_table(self):
        """
        Make sure the table can be created.
        """
        exception = None
        try:
            BaseUser.create().run_sync()
        except Exception as e:
            exception = e
        else:
            BaseUser.drop().run_sync()

        if exception:
            raise exception

        self.assertFalse(exception)


class TestHashPassword(TestCase):
    def test_hash_password(self):
        pass


class TestLogin(TestCase):
    def setUp(self):
        BaseUser.create().run_sync()

    def tearDown(self):
        BaseUser.drop().run_sync()

    def test_login(self):
        username = "bob"
        password = "Bob123$$$"
        email = "bob@bob.com"

        user = BaseUser(username=username, password=password, email=email)

        save_query = user.save()

        save_query.run_sync()

        authenticated = asyncio.run(BaseUser.login(username, password))
        self.assertTrue(authenticated is not None)

        authenticated = asyncio.run(BaseUser.login(username, "blablabla"))
        self.assertTrue(not authenticated)

    def test_update_password(self):
        username = "bob"
        password = "Bob123$$$"
        email = "bob@bob.com"

        user = BaseUser(username=username, password=password, email=email)
        user.save().run_sync()

        authenticated = BaseUser.login_sync(username, password)
        self.assertTrue(authenticated is not None)

        new_password = "XXX111"
        BaseUser.update_password_sync(username, new_password)
        authenticated = BaseUser.login_sync(username, new_password)
        self.assertTrue(authenticated is not None)
