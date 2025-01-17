from datetime import datetime, timedelta

from django.test.client import Client
from django.urls import reverse
import pytest

from news.models import News, Comment
from yanews import settings


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
def news_collection():
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=datetime.today() - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        text='Текст заметки',
        news=news,
        author=author
    )


@pytest.fixture()
def news_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture()
def news_home_url(news):
    return reverse('news:home')


@pytest.fixture()
def comments_url(news_url):
    return f'{news_url}#comments'


@pytest.fixture()
def comment_edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture()
def comment_delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture()
def login_url(news):
    return reverse('users:login')


@pytest.fixture()
def logout_url(news):
    return reverse('users:logout')


@pytest.fixture()
def signup_url(news):
    return reverse('users:signup')


@pytest.fixture()
def comment_edit_redirect_url(login_url, comment_edit_url):
    return f'{login_url}?next={comment_edit_url}'


@pytest.fixture()
def comment_delete_redirect_url(login_url, comment_delete_url):
    return f'{login_url}?next={comment_delete_url}'
