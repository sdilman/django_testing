from django.test.client import Client
from django.urls import reverse
import pytest

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст заметки'
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        text='Текст заметки',
        news=news,
        author=author
    )

@pytest.fixture()
def news_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture()
def comments_url(news_url):
    return f'{news_url}#comments'