from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from notes.forms import NoteForm
from notes.models import Note


User = get_user_model()


class TestContent(TestCase):

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

    def test_notes_list_for_different_users(self):
        user_results = (
            (self.author, self.assertIn), (self.not_author, self.assertNotIn)
        )
        url = reverse('notes:list')
        for user, verify in user_results:
            with self.subTest(user=user):
                self.client.force_login(user)
                response = self.client.get(url)
                object_list = response.context['object_list']
                verify(self.note, object_list)

    def test_pages_contains_form(self):
        name_args = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for name, args in name_args:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                self.client.force_login(self.author)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
