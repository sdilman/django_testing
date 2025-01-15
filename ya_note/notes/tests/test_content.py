from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from notes.forms import NoteForm
from notes.models import Note
from notes.tests.settings import (
    NOTE_TITLE, NOTE_TEXT, NOTE_SLUG,
    URL_NOTES_LIST, URL_ADD, URL_EDIT
)

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.not_author = User.objects.create(username='Не автор')
        cls.note = Note.objects.create(
            title=NOTE_TITLE,
            text=NOTE_TEXT,
            slug=NOTE_SLUG,
            author=cls.author
        )

    def test_notes_list_for_different_users(self):
        user_results = (
            (self.author, self.assertIn), (self.not_author, self.assertNotIn)
        )
        for user, verify in user_results:
            with self.subTest(user=user):
                self.client.force_login(user)
                response = self.client.get(URL_NOTES_LIST)
                verify(self.note, response.context['object_list'])

    def test_pages_contains_form(self):
        for url in (URL_ADD, URL_EDIT):
            with self.subTest(url=url):
                self.client.force_login(self.author)
                self.assertIsInstance(
                    self.client.get(url).context.get('form'), NoteForm
                ) 
