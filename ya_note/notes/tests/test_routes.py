from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note
from notes.tests.settings import (
    URL_HOME, URL_LOGIN, URL_LOGOUT, URL_SIGNUP,
    URL_NOTES_LIST, URL_SUCCESS, URL_DETAIL, URL_DELETE, URL_EDIT, URL_ADD,
    URL_LOGIN_REDIRECT_ADD, URL_LOGIN_REDIRECT_EDIT, URL_LOGIN_REDIRECT_SUCCESS,
    URL_LOGIN_REDIRECT_NOTES_LIST, URL_LOGIN_REDIRECT_DELETE, URL_LOGIN_REDIRECT_DETAIL
)

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.not_author = User.objects.create(username='Не автор')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)
        cls.note = Note.objects.create(
            title='Test News Title',
            text='Test News Text',
            slug='slug-test-0123456789',
            author=cls.author
        )

    def test_status_code(self):
        ...

    def test_redirect(self):
        ...


    def test_home_availability_for_anonymous_user(self):
        for url in (URL_HOME, URL_LOGIN, URL_LOGOUT, URL_SIGNUP):
            with self.subTest(url=url):
                self.assertEqual(
                    self.client.get(url).status_code, HTTPStatus.OK
                )

    def test_pages_availability_for_auth_user(self):
        for url in (URL_NOTES_LIST, URL_ADD, URL_SUCCESS):
            with self.subTest(url=url):
                response = self.not_author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_author_and_non_author(self):
        urls = URL_DETAIL, URL_DELETE, URL_EDIT
        user_results = (
            (self.author_client, HTTPStatus.OK),
            (self.not_author_client, HTTPStatus.NOT_FOUND)
        )
        for client, result in user_results:
            for url in urls:
                with self.subTest(url=url, client=client):
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
