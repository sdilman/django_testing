from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


NOTE_SLUG = 'slug-test-0123456789'
URL_HOME = reverse('notes:home')
URL_NOTES_LIST = reverse('notes:list')
URL_ADD = reverse('notes:add')
URL_EDIT = reverse('notes:edit', args=(NOTE_SLUG,))
URL_DELETE = reverse('notes:delete', args=(NOTE_SLUG,))
URL_DETAIL = reverse('notes:detail', args=(NOTE_SLUG,))
URL_LOGIN = reverse('users:login')
URL_LOGOUT = reverse('users:logout')
URL_SIGNUP = reverse('users:signup')
URL_SUCCESS = reverse('notes:success')
URL_LOGIN_REDIRECT_ADD = f'{URL_LOGIN}?next={URL_ADD}'
URL_LOGIN_REDIRECT_SUCCESS = f'{URL_LOGIN}?next={URL_SUCCESS}'
URL_LOGIN_REDIRECT_EDIT = f'{URL_LOGIN}?next={URL_EDIT}'
URL_LOGIN_REDIRECT_DELETE = f'{URL_LOGIN}?next={URL_DELETE}'
URL_LOGIN_REDIRECT_DETAIL = f'{URL_LOGIN}?next={URL_DETAIL}'
URL_LOGIN_REDIRECT_NOTES_LIST = f'{URL_LOGIN}?next={URL_NOTES_LIST}'


User = get_user_model()


class TestBase(TestCase):

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
            slug=NOTE_SLUG,
            author=cls.author
        )
        cls.form_data = {
            'title': 'New Title News Text',
            'text': 'New Test News Text',
            'slug': 'new-slug-test-0123456789'
        }
