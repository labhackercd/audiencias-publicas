import pytest
from apps.core.models import Question, Room, UpDownVote, Video, RoomAttachment
from apps.accounts.models import UserProfile
from apps.core.views import index
from mixer.backend.django import mixer
from django.urls import reverse
from django.test import RequestFactory
import json


@pytest.fixture
def test_user(db, django_user_model):
    return django_user_model.objects.create_user(
        username='testuser', email='test@e.com', is_active=True)


@pytest.mark.django_db
def test_redirect_to_room(client):
    room = mixer.blend(Room, cod_reunion='12345', is_visible=True)
    url = reverse(
        'video_reunion_room', kwargs={'cod_reunion': room.cod_reunion})
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_redirect_to_room_not_exists(client):
    url = reverse(
        'video_reunion_room', kwargs={'cod_reunion': '123'})
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_set_answer_time_with_time(client, test_user):
    mixer.blend(UserProfile, is_admin=True, user=test_user)
    question = mixer.blend(Question)
    video = mixer.blend(Video, video_id='testId')
    mixer.blend(UpDownVote, question=question)

    data = {'answer_time': '10', 'video_id': video.video_id}
    url = reverse('set_question_answer_time', kwargs={
        'question_id': question.id})

    client.force_login(test_user)
    response = client.post(url, data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_set_answer_time_without_time(client, test_user):
    mixer.blend(UserProfile, is_admin=True, user=test_user)
    question = mixer.blend(Question)
    video = mixer.blend(Video, video_id='testId')

    data = {'answer_time': '0', 'video_id': video.video_id}
    url = reverse('set_question_answer_time', kwargs={
        'question_id': question.id})

    client.force_login(test_user)
    response = client.post(url, data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_set_answer_time_user_no_group(client, test_user):
    question = mixer.blend(Question)
    video = mixer.blend(Video, video_id='testId')

    data = {'answer_time': '0', 'video_id': video.video_id}
    url = reverse('set_question_answer_time', kwargs={
        'question_id': question.id})

    client.force_login(test_user)
    response = client.post(url, data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_set_answer_time_no_answer(client, test_user):
    question = mixer.blend(Question)
    video = mixer.blend(Video, video_id='testId')

    data = {'video_id': video.video_id}
    url = reverse('set_question_answer_time', kwargs={
        'question_id': question.id})

    client.force_login(test_user)
    response = client.post(url, data)

    assert response.status_code == 400


@pytest.mark.django_db
def test_set_answer_time_unauthenticated(client):
    question = mixer.blend(Question)
    video = mixer.blend(Video, video_id='testId')

    data = {'video_id': video.video_id}
    url = reverse('set_question_answer_time', kwargs={
        'question_id': question.id})

    response = client.post(url, data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_set_answered(client, test_user):
    mixer.blend(UserProfile, is_admin=True, user=test_user)
    question = mixer.blend(Question)
    mixer.blend(UpDownVote, question=question)

    data = {'answered': 'true'}
    url = reverse('set_question_answered', kwargs={
        'question_id': question.id})

    client.force_login(test_user)
    response = client.post(url, data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_set_answered_false(client, test_user):
    mixer.blend(UserProfile, is_admin=True, user=test_user)
    question = mixer.blend(Question)
    mixer.blend(UpDownVote, question=question)

    data = {'answered': 'false'}
    url = reverse('set_question_answered', kwargs={
        'question_id': question.id})

    client.force_login(test_user)
    response = client.post(url, data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_set_answered_unauthorizated(client, test_user):
    question = mixer.blend(Question)

    url = reverse('set_question_answered', kwargs={
        'question_id': question.id})

    client.force_login(test_user)
    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_set_answered_unauthenticated(client):
    question = mixer.blend(Question)

    url = reverse('set_question_answered', kwargs={
        'question_id': question.id})

    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_set_priotity(client, test_user):
    mixer.blend(UserProfile, is_admin=True, user=test_user)
    question = mixer.blend(Question)
    mixer.blend(UpDownVote, question=question)

    data = {'is_priority': 'true'}
    url = reverse('set_question_priotity', kwargs={
                  'question_id': question.id})

    client.force_login(test_user)
    response = client.post(url, data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_set_priotity_false(client, test_user):
    mixer.blend(UserProfile, is_admin=True, user=test_user)
    question = mixer.blend(Question)
    mixer.blend(UpDownVote, question=question)

    data = {'is_priority': 'false'}
    url = reverse('set_question_priotity', kwargs={
                  'question_id': question.id})

    client.force_login(test_user)
    response = client.post(url, data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_set_priotity_unauthorizated(client, test_user):
    question = mixer.blend(Question)

    url = reverse('set_question_priotity', kwargs={
                  'question_id': question.id})

    client.force_login(test_user)
    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_set_priotity_unauthenticated(client):
    question = mixer.blend(Question)

    url = reverse('set_question_priotity', kwargs={
        'question_id': question.id})

    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_index():
    request = RequestFactory().get('/')
    response = index(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_create_attachment(client, test_user):
    room = mixer.blend(Room)
    mixer.blend(UserProfile, is_admin=True, user=test_user)
    client.force_login(test_user)

    data = {'url': 'test.com', 'title': 'test link'}

    url = reverse('create_attachment',
                  kwargs={'room_id': room.id})

    response = client.post(url, data)

    assert response.status_code == 302


@pytest.mark.django_db
def test_create_attachment_unauthorizated(client, test_user):
    room = mixer.blend(Room)

    url = reverse('create_attachment',
                  kwargs={'room_id': room.id})

    client.force_login(test_user)
    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_attachment_unauthenticated(client):
    room = mixer.blend(Room)

    url = reverse('create_attachment',
                  kwargs={'room_id': room.id})

    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_attachment(client, test_user):
    attachment = mixer.blend(RoomAttachment)
    mixer.blend(UserProfile, is_admin=True, user=test_user)
    client.force_login(test_user)

    url = reverse('delete_attachment',
                  kwargs={'attachment_id': attachment.id})

    response = client.post(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_attachment_unauthorizated(client, test_user):
    attachment = mixer.blend(RoomAttachment)

    url = reverse('delete_attachment',
                  kwargs={'attachment_id': attachment.id})

    client.force_login(test_user)
    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_attachment_unauthenticated(client):
    attachment = mixer.blend(RoomAttachment)

    url = reverse('delete_attachment',
                  kwargs={'attachment_id': attachment.id})

    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_add_external_link(client, test_user):
    room = mixer.blend(Room)
    mixer.blend(UserProfile, is_admin=True, user=test_user)
    client.force_login(test_user)

    url = reverse('add_external_link',
                  kwargs={'room_id': room.id})

    response = client.post(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_add_external_link_unauthorizated(client, test_user):
    room = mixer.blend(Room)

    url = reverse('add_external_link',
                  kwargs={'room_id': room.id})

    client.force_login(test_user)
    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_add_external_link_unauthenticated(client):
    room = mixer.blend(Room)

    url = reverse('add_external_link',
                  kwargs={'room_id': room.id})

    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_remove_external_link(client, test_user):
    room = mixer.blend(Room)
    mixer.blend(UserProfile, is_admin=True, user=test_user)
    client.force_login(test_user)

    url = reverse('remove_external_link',
                  kwargs={'room_id': room.id})

    response = client.post(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_remove_external_link_unauthorizated(client, test_user):
    room = mixer.blend(Room)

    url = reverse('remove_external_link',
                  kwargs={'room_id': room.id})

    client.force_login(test_user)
    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_remove_external_link_unauthenticated(client):
    room = mixer.blend(Room)

    url = reverse('remove_external_link',
                  kwargs={'room_id': room.id})

    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_video_attachment(client, test_user):
    room = mixer.blend(Room)
    mixer.blend(UserProfile, is_admin=True, user=test_user)
    client.force_login(test_user)

    data = {'video_id': 'testID', 'title': 'testTitle'}

    url = reverse('create_video_attachment',
                  kwargs={'room_id': room.id})

    response = client.post(url, data)

    assert response.status_code == 302


@pytest.mark.django_db
def test_create_video_attachment_unauthorizated(client, test_user):
    room = mixer.blend(Room)

    url = reverse('create_video_attachment',
                  kwargs={'room_id': room.id})

    client.force_login(test_user)
    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_video_attachment_unauthenticated(client):
    room = mixer.blend(Room)

    url = reverse('create_video_attachment',
                  kwargs={'room_id': room.id})

    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_video(client, test_user):
    video = mixer.blend(Video)
    mixer.blend(UserProfile, is_admin=True, user=test_user)
    client.force_login(test_user)

    url = reverse('delete_video',
                  kwargs={'video_id': video.id})

    response = client.post(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_video_unauthorizated(client, test_user):
    video = mixer.blend(Video)

    url = reverse('delete_video',
                  kwargs={'video_id': video.id})

    client.force_login(test_user)
    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_video_unauthenticated(client):
    video = mixer.blend(Video)

    url = reverse('delete_video',
                  kwargs={'video_id': video.id})

    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_order_videos(test_user, client):
    room = mixer.blend(Room)
    video = mixer.blend(Video, video_id='testVideo', order=1)
    mixer.blend(UserProfile, is_admin=True, user=test_user)
    client.force_login(test_user)

    data = {'data': json.dumps([{'id': video.id, 'order': 2}])}

    url = reverse('order_videos',
                  kwargs={'room_id': room.id})
    
    response = client.post(
        url,
        data=data,
    )
    ordered_video = Video.objects.get(video_id='testVideo')
    assert response.status_code == 200
    assert ordered_video.order == 2


@pytest.mark.django_db
def test_order_videos_unauthorizated(client, test_user):
    room = mixer.blend(Room)

    url = reverse('order_videos',
                  kwargs={'room_id': room.id})

    client.force_login(test_user)
    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_order_videos_unauthenticated(client):
    room = mixer.blend(Room)

    url = reverse('order_videos',
                  kwargs={'room_id': room.id})

    response = client.post(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_video_detail(client, test_user):
    room = mixer.blend(Room, is_active=True)

    url = reverse('video_room',
                  kwargs={'pk': room.id})

    client.force_login(test_user)
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_video_detail_inactive(client, test_user):
    room = mixer.blend(Room, is_active=False)

    url = reverse('video_room',
                  kwargs={'pk': room.id})

    client.force_login(test_user)
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_widget(client, test_user):
    room = mixer.blend(Room, is_active=True)

    url = reverse('widget_index',
                  kwargs={'pk': room.id})

    client.force_login(test_user)
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_widget_inactive(client, test_user):
    room = mixer.blend(Room, is_active=False)

    url = reverse('widget_index',
                  kwargs={'pk': room.id})

    client.force_login(test_user)
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_room_report(client, test_user):
    room = mixer.blend(Room, is_active=True)

    url = reverse('room_report',
                  kwargs={'pk': room.id})

    client.force_login(test_user)
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_room_report_inactive(client, test_user):
    room = mixer.blend(Room, is_active=False)

    url = reverse('room_report',
                  kwargs={'pk': room.id})

    client.force_login(test_user)
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_closed_videos(client):
    mixer.blend(Room,
        title_reunion='test',
        date='2022-01-01',
        is_visible=True,
        youtube_status=2,
        is_active=True)

    url = '%s?q=test&initial_date=01/01/2021&end_date=01/02/2022' % (
        reverse('video_list'))

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_room_question_list(client, test_user):
    room = mixer.blend(Room, is_active=True)
    mixer.blend(UserProfile, is_admin=True, user=test_user)

    url = reverse('questions_list', kwargs={'pk': room.id})

    client.force_login(test_user)
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_room_question_list_unauthorized(client, test_user):
    room = mixer.blend(Room, is_active=True)

    url = reverse('questions_list', kwargs={'pk': room.id})

    client.force_login(test_user)
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_question_detail(client):
    question = mixer.blend(Question)

    url = reverse('question_detail',
                  kwargs={'pk': question.id})

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_cenorship(client):
    url = reverse('censorship')
    data = {'text': 'test text pqp'}

    response = client.post(url, data)

    assert response.content == b'{"original": "test text pqp", "censored": "test text \\u2665"}' # noqa


@pytest.mark.django_db
def test_cenorship_bad_request(client):
    url = reverse('censorship')

    response = client.post(url)

    assert response.content == b'Missing parameters'


@pytest.mark.django_db
def test_get_cenorship(client):
    url = reverse('censorship')

    response = client.get(url)

    assert 'pqp' in str(response.content)