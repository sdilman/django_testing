from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from notes.tests.test_base import TestBase, URL_NOTES_LIST, URL_ADD, URL_EDIT


User = get_user_model()


class TestContent(TestBase):

    def test_notes_list_for_author(self):
        response_context = self.author_client.get(URL_NOTES_LIST).context
        self.assertIn('object_list', response_context)
        note = response_context['object_list'].get(id=self.note.id)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.author, note.author)

    def test_notes_list_for_non_author(self):
        self.assertNotIn(
            self.note,
            self.not_author_client.get(URL_NOTES_LIST).context['object_list']
        )

    def test_pages_contains_form(self):
        for url in (URL_ADD, URL_EDIT):
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context.get('form'),
                    NoteForm
                )
