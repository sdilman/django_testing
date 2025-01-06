from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.not_author = User.objects.create(username='Не автор')
        cls.note = Note.objects.create(
            title='Test News Title',
            text='Test News Text',
            slug='slug-test-0123456789',
            author=cls.author
        )

    def test_home_availability_for_anonymous_user(self):
        names = ('notes:home', 'users:login', 'users:logout', 'users:signup')
        for name in names:
            with self.subTest(name=name):
                self.assertEqual(
                    self.client.get(reverse(name)).status_code, HTTPStatus.OK
                )

    def test_pages_availability_for_auth_user(self):
        names = ('notes:list', 'notes:add', 'notes:success')
        self.client.force_login(self.not_author)
        for name in names:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_author(self):
        names = ('notes:detail', 'notes:edit', 'notes:delete')
        self.client.force_login(self.author)
        for name in names:
            with self.subTest(name=name):
                response = self.client.get(
                    reverse(name, args=(self.note.slug,))
                )
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_non_authorized(self):
        names = ('notes:detail', 'notes:edit', 'notes:delete')
        user_results = (
            (self.author, HTTPStatus.OK),
            (self.not_author, HTTPStatus.NOT_FOUND)
        )
        for user, result in user_results:
            self.client.force_login(user)
            for name in names:
                with self.subTest(name=name, user=user):
                    response = self.client.get(
                        reverse(name, args=(self.note.slug,))
                    )
                    self.assertEqual(response.status_code, result)

    def test_redirects(self):
        page_data = (
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:add', None),
            ('notes:success', None),
            ('notes:list', None),
        )
        for name, args in page_data:
            login_url = reverse('users:login')
            with self.subTest(name=name):
                url = reverse(name, args=args)
                # if args is not None:
                #     url = reverse(name, args=args)
                # else:
                #     url = reverse(name)
                expected_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, expected_url)
