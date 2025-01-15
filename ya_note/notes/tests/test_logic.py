from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.settings import (
    NOTE_TITLE, NOTE_TEXT, NOTE_SLUG,
    NOTE_TITLE_NEW, NOTE_TEXT_NEW, NOTE_SLUG_NEW,
    NOTE_TITLE_FOR_UPDATE, NOTE_TEXT_FOR_UPDATE,
    URL_NOTES_LIST, URL_ADD, URL_EDIT,
    URL_LOGIN_REDIRECT_ADD, URL_SUCCESS,
    URL_DELETE
)

User = get_user_model()


class TestLogic(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.not_author = User.objects.create(username='Не автор')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)
        cls.form_data = {
            'title': NOTE_TITLE_NEW,
            'text': NOTE_TEXT_NEW,
            'slug': NOTE_SLUG_NEW
        }
        cls.note = Note.objects.create(
            title=NOTE_TITLE,
            text=NOTE_TEXT,
            slug=NOTE_SLUG,
            author=cls.author
        )
        cls.num_of_notes = Note.objects.count()

    def test_user_can_create_note(self):
        response = self.author_client.post(
            URL_ADD, data=self.form_data
        )
        self.assertRedirects(response, URL_SUCCESS)
        self.assertEqual(Note.objects.count(), self.num_of_notes + 1)
        new_note = Note.objects.filter(
            title = self.form_data['title'],
            text = self.form_data['text'],
            slug = self.form_data['slug'],
        ).get()
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        response = self.client.post(URL_ADD, data=self.form_data)
        self.assertRedirects(response, URL_LOGIN_REDIRECT_ADD)
        assert Note.objects.count() == self.num_of_notes

    def test_not_unique_slug(self):
        note = Note.objects.create(
            title=NOTE_TITLE_FOR_UPDATE,
            text=NOTE_TEXT_FOR_UPDATE,
            slug=self.form_data['slug'],
            author=self.author
        )
        response = self.author_client.post(URL_ADD, data=self.form_data)
        self.assertFormError(
            response, 'form', 'slug', errors=(note.slug + WARNING)
        )
        assert Note.objects.count() == self.num_of_notes + 1

    def test_empty_slug(self):
        self.form_data.pop('slug')
        response = self.author_client.post(
            URL_ADD,
            data=self.form_data
        )
        self.assertRedirects(response, URL_SUCCESS)
        self.assertEqual(Note.objects.count(), self.num_of_notes + 1)
        new_note = Note.objects.filter(
            title = self.form_data['title'],
            text = self.form_data['text']
        ).get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        response = self.author_client.post(URL_EDIT, self.form_data)
        self.assertRedirects(response, URL_SUCCESS)
        note_from_db = Note.objects.filter(pk=self.note.pk).get()
        self.assertEqual(note_from_db.title, self.form_data['title'])
        self.assertEqual(note_from_db.text, self.form_data['text'])
        self.assertEqual(note_from_db.slug, self.form_data['slug'])
        self.assertEqual(note_from_db.author, self.author)

    def test_other_user_cant_edit_note(self):
        response = self.not_author_client.post(URL_EDIT, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)

    def test_author_can_delete_note(self):
        response = self.author_client.post(URL_DELETE)
        self.assertRedirects(response, URL_SUCCESS)
        self.assertEqual(Note.objects.filter(pk=self.note.pk).exists(), False)

    def test_other_user_cant_delete_note(self):
        response = self.not_author_client.post(URL_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.filter(pk=self.note.pk).get()
        self.assertEqual(note_from_db.title, self.note.title)
        self.assertEqual(note_from_db.text, self.note.text)
        self.assertEqual(note_from_db.slug, self.note.slug)
        self.assertEqual(note_from_db.author, self.note.author)

