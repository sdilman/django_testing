from django.urls import reverse

NOTE_TITLE='Test News Title'
NOTE_TEXT='Test News Text'
NOTE_SLUG='slug-test-0123456789'
NOTE_TITLE_NEW='New Test News Title'
NOTE_TEXT_NEW='New Test News Text'
NOTE_SLUG_NEW='new-slug-test-0123456789'
NOTE_TITLE_FOR_UPDATE='New Test News Title'
NOTE_TEXT_FOR_UPDATE='New Test News Text'
URL_HOME=reverse('notes:home')
URL_NOTES_LIST=reverse('notes:list')
URL_ADD=reverse('notes:add')
URL_EDIT=reverse('notes:edit', args=(NOTE_SLUG,))
URL_LOGIN=reverse('users:login')
URL_LOGOUT=reverse('users:logout')
URL_SIGNUP=reverse('users:signup')
URL_SUCCESS=reverse('notes:success')
URL_DELETE=reverse('notes:delete', args=(NOTE_SLUG,))
URL_DETAIL=reverse('notes:detail', args=(NOTE_SLUG,))
URL_LOGIN_REDIRECT_ADD=URL_LOGIN + '?next=' + URL_ADD
URL_LOGIN_REDIRECT_SUCCESS=URL_LOGIN + '?next=' + URL_SUCCESS
URL_LOGIN_REDIRECT_EDIT=URL_LOGIN + '?next=' + URL_EDIT
URL_LOGIN_REDIRECT_DELETE=URL_LOGIN + '?next=' + URL_DELETE
URL_LOGIN_REDIRECT_DETAIL=URL_LOGIN + '?next=' + URL_DETAIL
URL_LOGIN_REDIRECT_NOTES_LIST=URL_LOGIN + '?next=' + URL_NOTES_LIST
