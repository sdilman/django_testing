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

    def add_note_execute_check(self, form_data, expected_slug):
        """Make call to add note and check one record added."""
        notes_before = set(Note.objects.values_list())
        response = self.author_client.post(
            URL_ADD, data=form_data
        )
        self.assertRedirects(response, URL_SUCCESS)
        notes_after = set(Note.objects.values_list())
        self.assertTrue(notes_before <= notes_after)
        notes_added = notes_after - notes_before
        self.assertEqual(len(notes_added), 1)
        note_added = notes_added.pop()
        self.assertEqual(
            note_added[1:],
            (
                self.form_data['title'],
                self.form_data['text'],
                expected_slug,
                self.author.id
            )
        )

    def test_user_can_create_note(self):
        expected_slug = self.form_data['slug']
        self.add_note_execute_check(self.form_data, expected_slug)

    def test_empty_slug(self):
        self.form_data.pop('slug')
        expected_slug = slugify(self.form_data['title'])
        self.add_note_execute_check(self.form_data, expected_slug)

    def test_anonymous_user_cant_create_note(self):
        notes_before = set(Note.objects.values_list())
        response = self.client.post(URL_ADD, data=self.form_data)
        self.assertRedirects(response, URL_LOGIN_REDIRECT_ADD)
        notes_after = set(Note.objects.values_list())
        assert notes_before == notes_after

    def test_not_unique_slug(self):
        notes_before = list(Note.objects.values())
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(URL_ADD, data=self.form_data)
        self.assertFormError(
            response, 'form', 'slug', errors=(self.note.slug + WARNING)
        )
        notes_after = list(Note.objects.values())
        assert sorted(notes_before) == sorted(notes_after)

    def test_author_can_edit_note(self):
        response = self.author_client.post(URL_EDIT, self.form_data)
        self.assertRedirects(response, URL_SUCCESS)
        note_from_db = Note.objects.filter(pk=self.note.pk).get()
        self.assertEqual(self.form_data['title'], note_from_db.title)
        self.assertEqual(self.form_data['text'], note_from_db.text)
        self.assertEqual(self.form_data['slug'], note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_other_user_cant_edit_note(self):
        notes_before = set(Note.objects.values_list())
        response = self.not_author_client.post(URL_EDIT, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_after = set(Note.objects.values_list())
        assert notes_before == notes_after

    def test_author_can_delete_note(self):
        notes_before = set(Note.objects.values_list())
        response = self.author_client.post(URL_DELETE)
        self.assertRedirects(response, URL_SUCCESS)
        notes_after = set(Note.objects.values_list())
        self.assertTrue(notes_after <= notes_before)
        notes_deleted = notes_before - notes_after
        self.assertEqual(len(notes_deleted), 1)
        note_deleted = notes_deleted.pop()
        self.assertEqual(
            note_deleted[1:],
            (
                self.note.title,
                self.note.text,
                self.note.slug,
                self.note.author.id
            )
        )

    def test_other_user_cant_delete_note(self):
        notes_before = set(Note.objects.values_list())
        response = self.not_author_client.post(URL_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_after = set(Note.objects.values_list())
        assert notes_before == notes_after
