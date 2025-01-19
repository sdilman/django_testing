from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.test_base import (
    URL_ADD, URL_EDIT,
    URL_LOGIN_REDIRECT_ADD, URL_SUCCESS,
    URL_DELETE
)
from notes.tests.test_base import TestBase


User = get_user_model()


class TestLogic(TestBase):

    def add_note_execute_check(self, expected_slug):
        """Make call to add note and check one record added."""
        notes = set(Note.objects.all())
        response = self.author_client.post(
            URL_ADD, data=self.form_data
        )
        self.assertRedirects(response, URL_SUCCESS)
        notes = set(Note.objects.all()) - notes
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, expected_slug)
        self.assertEqual(note.author, self.author)

    def test_user_can_create_note(self):
        self.add_note_execute_check(self.form_data['slug'])

    def test_empty_slug(self):
        self.form_data.pop('slug')
        expected_slug = slugify(self.form_data['title'])
        self.add_note_execute_check(expected_slug)

    def test_anonymous_user_cant_create_note(self):
        notes_before = set(Note.objects.all())
        response = self.client.post(URL_ADD, data=self.form_data)
        self.assertRedirects(response, URL_LOGIN_REDIRECT_ADD)
        notes_after = set(Note.objects.all())
        self.assertEqual(notes_before, notes_after)

    def test_not_unique_slug(self):
        notes_before = set(Note.objects.all())
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(URL_ADD, data=self.form_data)
        self.assertFormError(
            response, 'form', 'slug', errors=(self.note.slug + WARNING)
        )
        notes_after = set(Note.objects.all())
        self.assertEqual(notes_before, notes_after)

    def test_author_can_edit_note(self):
        response = self.author_client.post(URL_EDIT, self.form_data)
        self.assertRedirects(response, URL_SUCCESS)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(self.form_data['title'], note.title)
        self.assertEqual(self.form_data['text'], note.text)
        self.assertEqual(self.form_data['slug'], note.slug)
        self.assertEqual(self.note.author, note.author)

    def test_other_user_cant_edit_note(self):
        response = self.not_author_client.post(URL_EDIT, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.author, note.author)

    def test_author_can_delete_note(self):
        notes_count = Note.objects.count()
        response = self.author_client.post(URL_DELETE)
        self.assertRedirects(response, URL_SUCCESS)
        self.assertEqual(Note.objects.count(), notes_count - 1)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_other_user_cant_delete_note(self):
        notes_before = set(Note.objects.values_list())
        response = self.not_author_client.post(URL_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_after = set(Note.objects.values_list())
        self.assertEqual(notes_before, notes_after)
