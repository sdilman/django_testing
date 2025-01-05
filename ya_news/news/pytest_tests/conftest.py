import pytest

from django.test.client import Client

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
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки'
    )
    return news


@pytest.fixture
def news_id_args(news):
    return (news.id,)


@pytest.fixture
def comment(author, news):
    news = Comment.objects.create(
        text='Текст заметки',
        news=news,
        author=author,
    )
    return news


@pytest.fixture
def comment_id_args(comment):
    return (comment.id,)


@pytest.fixture
def news_form_data():
    return {
        'title': 'Новый заголовок',
        'text': 'Новый текст'
    }


@pytest.fixture
def comment_form_data():
    return {
        'text': 'Новый текст'
    }
