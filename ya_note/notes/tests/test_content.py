from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from notes.tests.settings import (
    URL_NOTES_LIST, URL_ADD, URL_EDIT
)
from notes.tests.test_base import TestBase


User = get_user_model()


class TestContent(TestBase):

    def test_notes_list_for_different_users(self):
        user_results = (
            (self.author_client, self.assertIn),
            (self.not_author_client, self.assertNotIn)
        )
        for client, verify in user_results:
            with self.subTest(client=client):
                verify(
                    self.note,
                    client.get(URL_NOTES_LIST).context['object_list']
                )

    def test_pages_contains_form(self):
        for url in (URL_ADD, URL_EDIT):
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context.get('form'),
                    NoteForm
                )
