from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client, TestCase

from notes.models import Note
from notes.tests.settings import (
    NOTE_TITLE, NOTE_TEXT, NOTE_SLUG
)

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
            title=NOTE_TITLE,
            text=NOTE_TEXT,
            slug=NOTE_SLUG,
            author=cls.author
        )