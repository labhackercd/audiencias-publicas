import pytest
from apps.core.templatetags.video_utils import *
from apps.core.models import Question, Room, UpDownVote
from mixer.backend.django import mixer
from django.contrib.auth.models import Group
from apps.accounts.models import UserProfile


@pytest.fixture
def test_user(db, django_user_model):
    return django_user_model.objects.create_user(
        username='testuser', email='test@e.com', is_active=True)


@pytest.mark.django_db
def test_vote_action_answered(test_user):
    question = mixer.blend(Question, answered=True, user=test_user)
    html = vote_action(question, test_user.username)

    assert 'Pergunta Respondida' in html


@pytest.mark.django_db
def test_vote_action_same_user(test_user):
    question = mixer.blend(Question, answered=False, user=test_user)
    html = vote_action(question, test_user.username)

    assert 'Sua Pergunta' in html


@pytest.mark.django_db
def test_vote_action_disabled_same_user(test_user):
    room = mixer.blend(Room, youtube_status=2)
    question = mixer.blend(Question, answered=False, room=room)
    mixer.blend(UpDownVote, question=question, user=test_user)
    html = vote_action(question, test_user.username)

    assert 'disabled' in html
    assert 'voted' in html
    assert 'Apoiada por você' in html


@pytest.mark.django_db
def test_vote_action_enabled_same_user(test_user):
    room = mixer.blend(Room, youtube_status=1)
    question = mixer.blend(Question, answered=False, room=room)
    mixer.blend(UpDownVote, question=question, user=test_user)
    html = vote_action(question, test_user.username)

    assert 'voted' in html
    assert 'Apoiada por você' in html


@pytest.mark.django_db
def test_vote_action_disabled_diferent_user(test_user):
    room = mixer.blend(Room, youtube_status=2)
    question = mixer.blend(Question, answered=False, room=room)
    html = vote_action(question, test_user.username)

    assert 'disabled' in html
    assert 'Votar Nesta Pergunta' in html


@pytest.mark.django_db
def test_vote_action_enabled_diferent_user(test_user):
    room = mixer.blend(Room, youtube_status=1)
    question = mixer.blend(Question, answered=False, room=room)
    html = vote_action(question, test_user.username)

    assert 'JS-voteBtnEnabled' in html
    assert 'Votar Nesta Pergunta' in html


def test_format_seconds():
    answer_time = format_seconds(4926.150556015259) # 1hour 22 minutes 6 seconds
    assert answer_time == '1:22:06'


@pytest.mark.django_db
def test_belongs_to_group_not_exists(test_user):
    has_group = belongs_to_group(test_user, 'GroupDoesNotExist')
    
    assert has_group == False


@pytest.mark.django_db
def test_belongs_to_group_exists(test_user):
    group = mixer.blend(Group, name='testgroup')
    test_user.groups.add(group)
    has_group = belongs_to_group(test_user, 'testgroup')

    assert has_group == True


@pytest.mark.django_db
def test_belongs_to_group_is_adamin(test_user):
    mixer.blend(UserProfile, is_admin=True, user=test_user)
    has_group = belongs_to_group(test_user, 'testgroup')

    assert has_group == True

