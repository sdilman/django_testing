from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.tests.test_base import (
    URL_HOME, URL_LOGIN, URL_LOGOUT, URL_SIGNUP,
    URL_NOTES_LIST, URL_SUCCESS, URL_DETAIL, URL_DELETE, URL_EDIT, URL_ADD,
    URL_LOGIN_REDIRECT_ADD, URL_LOGIN_REDIRECT_EDIT,
    URL_LOGIN_REDIRECT_SUCCESS,
    URL_LOGIN_REDIRECT_NOTES_LIST, URL_LOGIN_REDIRECT_DELETE,
    URL_LOGIN_REDIRECT_DETAIL
)
from notes.tests.test_base import TestBase


User = get_user_model()


class TestRoutes(TestBase):

    def test_status_code(self):
        cases = (
            (URL_HOME, self.client, HTTPStatus.OK),
            (URL_LOGIN, self.client, HTTPStatus.OK),
            (URL_LOGOUT, self.client, HTTPStatus.OK),
            (URL_SIGNUP, self.client, HTTPStatus.OK),
            (URL_NOTES_LIST, self.not_author_client, HTTPStatus.OK),
            (URL_ADD, self.not_author_client, HTTPStatus.OK),
            (URL_SUCCESS, self.not_author_client, HTTPStatus.OK),
            (URL_DETAIL, self.author_client, HTTPStatus.OK),
            (URL_DELETE, self.author_client, HTTPStatus.OK),
            (URL_EDIT, self.author_client, HTTPStatus.OK),
            (URL_DETAIL, self.not_author_client, HTTPStatus.NOT_FOUND),
            (URL_DELETE, self.not_author_client, HTTPStatus.NOT_FOUND),
            (URL_EDIT, self.not_author_client, HTTPStatus.NOT_FOUND),
        )
        for url, client, result in cases:
            with self.subTest(url=url, client=client, result=result):
                self.assertEqual(client.get(url).status_code, result)

    def test_redirects(self):
        urls = (
            (URL_DETAIL, URL_LOGIN_REDIRECT_DETAIL),
            (URL_EDIT, URL_LOGIN_REDIRECT_EDIT),
            (URL_DELETE, URL_LOGIN_REDIRECT_DELETE),
            (URL_ADD, URL_LOGIN_REDIRECT_ADD),
            (URL_SUCCESS, URL_LOGIN_REDIRECT_SUCCESS),
            (URL_NOTES_LIST, URL_LOGIN_REDIRECT_NOTES_LIST)
        )
        for url_call, url_redirect in urls:
            with self.subTest(url=url_call):
                response = self.client.get(url_call)
                self.assertRedirects(response, url_redirect)
