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


def check_notes_added_one(author, title, text, slug):
    """Add check that Note table obtained one record with given fields."""

    def outer(f):
        def wrapper(*args, **kwargs):
            notes_before = list(Note.objects.values())
            f(*args, **kwargs)
            notes_after = list(Note.objects.values())
            assert len(notes_before) + 1 == len(notes_after)
            notes_added = [
                item for item in notes_after if item not in notes_before
            ]
            assert len(notes_added) == 1
            note_added = notes_added[0]
            assert note_added['author_id'] == author.id
            assert note_added['title'] == title
            assert note_added['text'] == text
            assert note_added['slug'] == slug
        return wrapper
    return outer


def check_notes_deleted_one(author, title, text, slug):
    """Add check that from Note table deleted one record with given fields."""

    def outer(f):
        def wrapper(*args, **kwargs):
            notes_before = list(Note.objects.values())
            f(*args, **kwargs)
            notes_after = list(Note.objects.values())
            assert len(notes_before) == len(notes_after) + 1
            notes_deleted = [
                item for item in notes_before if item not in notes_after
            ]
            assert len(notes_deleted) == 1
            note_deleted = notes_deleted[0]
            assert note_deleted['author_id'] == author.id
            assert note_deleted['title'] == title
            assert note_deleted['text'] == text
            assert note_deleted['slug'] == slug
        return wrapper
    return outer


class TestLogic(TestBase):

    def test_user_can_create_note(self):
        @check_notes_added_one(
            self.author,
            self.form_data['title'],
            self.form_data['text'],
            self.form_data['slug']
        )
        def work():
            response = self.author_client.post(
                URL_ADD, data=self.form_data
            )
            self.assertRedirects(response, URL_SUCCESS)
        return work()

    def test_anonymous_user_cant_create_note(self):
        self.assertRedirects(
            self.client.post(URL_ADD, data=self.form_data),
            URL_LOGIN_REDIRECT_ADD
        )
        self.assertEqual(
            set(Note.objects.values_list()),
            self.initial_note_table_content()
        )

    def test_not_unique_slug(self):
        notes_before = list(Note.objects.values())
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(URL_ADD, data=self.form_data)
        self.assertFormError(
            response, 'form', 'slug', errors=(self.note.slug + WARNING)
        )
        notes_after = list(Note.objects.values())
        self.assertEqual(sorted(notes_before), sorted(notes_after))

    def test_empty_slug(self):
        @check_notes_added_one(
            self.author,
            self.form_data['title'],
            self.form_data['text'],
            slugify(self.form_data['title'])
        )
        def work():
            self.form_data.pop('slug')
            response = self.author_client.post(
                URL_ADD, data=self.form_data
            )
            self.assertRedirects(response, URL_SUCCESS)
        return work()

    def test_author_can_edit_note(self):
        response = self.author_client.post(URL_EDIT, self.form_data)
        self.assertRedirects(response, URL_SUCCESS)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(self.form_data['title'], note.title)
        self.assertEqual(self.form_data['text'], note.text)
        self.assertEqual(self.form_data['slug'], note.slug)
        self.assertEqual(self.note.author, note.author)

    def test_other_user_cant_edit_note(self):
        notes_before = list(Note.objects.values())
        response = self.not_author_client.post(URL_EDIT, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_after = list(Note.objects.values())
        self.assertEqual(sorted(notes_before), sorted(notes_after))

    def test_author_can_delete_note(self):
        @check_notes_deleted_one(
            self.note.author,
            self.note.title,
            self.note.text,
            self.note.slug
        )
        def work():
            response = self.author_client.post(URL_DELETE)
            self.assertRedirects(response, URL_SUCCESS)
        return work()

    def test_other_user_cant_delete_note(self):
        notes_before = list(Note.objects.values())
        response = self.not_author_client.post(URL_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_after = list(Note.objects.values())
        self.assertEqual(sorted(notes_before), sorted(notes_after))
