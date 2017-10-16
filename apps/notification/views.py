from django.conf import settings
from apps.core.models import Question, Room, UpDownVote, Message
from apps.notification.models import ParticipantNotification
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect


def send_participants_notification(request, room_id):
    if request.POST:
        room = Room.objects.get(id=room_id)
        questions_id = Question.objects.filter(
            room=room).values_list('id', flat=True)
        votes_users = UpDownVote.objects.filter(
            question_id__in=questions_id).values_list('user_id', flat=True)
        questions_users = Question.objects.filter(
            room=room).values_list('user_id', flat=True)
        messages_users = Message.objects.filter(
            room=room).values_list('user_id', flat=True)
        all_users = set(
            list(votes_users) + list(questions_users) + list(messages_users))
        users_email = get_user_model().objects.filter(
            id__in=all_users).values_list('email', flat=True)
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        # Definir template do corpo de email
        html = render_to_string('email/participants-notification.html',
                                {'room': room,
                                 'content': content})
        # Definir assunto do email
        email_subject = u'[Audiências Interativas] %s' % subject

        for email in users_email:
            mail = EmailMultiAlternatives(
                email_subject, '',
                settings.EMAIL_HOST_USER,
                [email]
            )
            mail.attach_alternative(html, 'text/html')
            mail.send()

        notification = ParticipantNotification()
        notification.room = room
        notification.emails = users_email
        notification.content = content
        notification.save()

        return redirect('video_room', pk=room_id)
