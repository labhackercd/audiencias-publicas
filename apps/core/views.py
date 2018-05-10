from django.conf import settings
from django.http import (Http404, HttpResponseForbidden, HttpResponseRedirect,
                         HttpResponseBadRequest, HttpResponse)
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from apps.core.models import Question, Room, RoomAttachment, Video
from apps.core.utils import encrypt
from apps.core.templatetags.video_utils import belongs_to_group
from django.views.generic import DetailView, ListView
from django.shortcuts import render, redirect
from datetime import datetime
from django.db.models import Q
from channels import Group
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
import json
from itertools import chain
from apps.core.forms import RoomAttachmentForm, VideoForm


def redirect_to_room(request, cod_reunion):
    rooms = Room.objects.filter(cod_reunion=cod_reunion, is_visible=True)
    try:
        obj = rooms.latest('date')
    except rooms.model.DoesNotExist:
        raise Http404(_("No %(verbose_name)s found matching the query") %
                      {'verbose_name': rooms.model._meta.verbose_name})
    return redirect('video_room', pk=obj.id)


def set_answer_time(request, question_id):
    if request.user.is_authenticated() and request.method == 'POST':
        answer_time = request.POST.get('answer_time')
        video_id = request.POST.get('video_id')
        if answer_time:
            question = Question.objects.get(pk=question_id)
            group_name = question.room.legislative_body_initials
            if belongs_to_group(request.user, group_name):
                if answer_time == '0':
                    question.answer_time = None
                    question.answered = False
                else:
                    video = Video.objects.filter(video_id=video_id).first()
                    question.answer_time = answer_time
                    question.answered = True
                    question.video = video
                question.save()
                vote_list = []
                for vote in question.votes.all():
                    vote_list.append(encrypt(str(vote.user.id).rjust(10)))

                html = question.html_question_body(request.user, 'room')
                text = {
                    'question': True,
                    'html': html,
                    'id': question.id,
                    'voteList': vote_list,
                    'answered': question.answered,
                    'groupName': group_name,
                    'handlerAction': encrypt(str(request.user.id).rjust(10)),
                }
                Group(question.room.group_room_name).send(
                    {'text': json.dumps(text)}
                )

                html_question_panel = question.html_question_body(
                    request.user, 'question-panel')
                text_question_panel = {
                    'html': html_question_panel,
                    'id': question.id
                }
                Group(question.room.group_room_questions_name).send(
                    {'text': json.dumps(text_question_panel)}
                )
                return HttpResponse(status=200)
            else:
                return HttpResponseForbidden()
        else:
            return HttpResponseBadRequest('Invalid format.')
    else:
        return HttpResponseForbidden()


def set_answered(request, question_id):
    if request.user.is_authenticated() and request.method == 'POST':
        answered = request.POST.get('answered')
        question = Question.objects.get(pk=question_id)
        group_name = question.room.legislative_body_initials
        if belongs_to_group(request.user, group_name):
            if answered == 'true':
                question.answered = True
            else:
                question.answered = False
                question.answer_time = None
            question.save()
            vote_list = []
            for vote in question.votes.all():
                vote_list.append(encrypt(str(vote.user.id).rjust(10)))

            html = question.html_question_body(request.user, 'room')
            text = {
                'question': True,
                'html': html,
                'id': question.id,
                'voteList': vote_list,
                'answered': question.answered,
                'groupName': group_name,
                'handlerAction': encrypt(str(request.user.id).rjust(10)),
            }
            Group(question.room.group_room_name).send(
                {'text': json.dumps(text)}
            )

            html_question_panel = question.html_question_body(
                request.user, 'question-panel')
            text_question_panel = {
                'html': html_question_panel,
                'id': question.id
            }
            Group(question.room.group_room_questions_name).send(
                {'text': json.dumps(text_question_panel)}
            )

            return HttpResponse(status=200)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def set_priotity(request, question_id):
    if request.user.is_authenticated() and request.method == 'POST':
        is_priority = request.POST.get('is_priority')
        question = Question.objects.get(pk=question_id)
        group_name = question.room.legislative_body_initials
        if belongs_to_group(request.user, group_name):
            if is_priority == 'true':
                question.is_priority = True
            else:
                question.is_priority = False

            question.save()
            vote_list = []
            for vote in question.votes.all():
                vote_list.append(encrypt(str(vote.user.id).rjust(10)))
            html = question.html_question_body(request.user, 'room')
            text = {
                'question': True,
                'html': html,
                'id': question.id,
                'voteList': vote_list,
                'answered': question.answered,
                'groupName': group_name,
                'handlerAction': encrypt(str(request.user.id).rjust(10)),
            }
            Group(question.room.group_room_name).send(
                {'text': json.dumps(text)}
            )
            html_question_panel = question.html_question_body(
                request.user, 'question-panel')
            text_question_panel = {
                'html': html_question_panel,
                'id': question.id
            }
            Group(question.room.group_room_questions_name).send(
                {'text': json.dumps(text_question_panel)}
            )
            return HttpResponse(status=200)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def index(request):
    return render(request, 'index.html', context=dict(
        closed_videos=Room.objects.filter(
            youtube_status=2,
            is_visible=True).order_by('-date')[:5],
        live_videos=Room.objects.filter(
            youtube_status=1,
            is_visible=True).order_by('-date'),
        agendas=Room.objects.filter(
            is_visible=True,
            youtube_status=0).order_by('date'),
    ))


def create_attachment(request, room_id):
    if request.user.is_authenticated() and request.method == 'POST':
        room = Room.objects.get(pk=room_id)
        group_name = room.legislative_body_initials
        if belongs_to_group(request.user, group_name):
            form = RoomAttachmentForm(request.POST)
            if form.is_valid():
                attachment = form.save(commit=False)
                attachment.room = room
                attachment.save()
            return redirect('video_room', pk=room.id)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def delete_attachment(request, attachment_id):
    if request.user.is_authenticated():
        attachment = RoomAttachment.objects.get(pk=attachment_id)
        group_name = attachment.room.legislative_body_initials
        if belongs_to_group(request.user, group_name):
            attachment.delete()
            return redirect('video_room', pk=attachment.room.id)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def add_external_link(request, room_id):
    if request.user.is_authenticated() and request.method == 'POST':
        room = Room.objects.get(pk=room_id)
        group_name = room.legislative_body_initials
        if belongs_to_group(request.user, group_name):
            room.external_link = request.POST.get('link', '')
            room.save()
            return redirect('video_room', pk=room.id)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def remove_external_link(request, room_id):
    if request.user.is_authenticated():
        room = Room.objects.get(pk=room_id)
        group_name = room.legislative_body_initials
        if belongs_to_group(request.user, group_name):
            room.external_link = ''
            room.save()
            return redirect('video_room', pk=room.id)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def create_video_attachment(request, room_id):
    if request.user.is_authenticated() and request.method == 'POST':
        room = Room.objects.get(pk=room_id)
        group_name = room.legislative_body_initials
        if belongs_to_group(request.user, group_name):
            form = VideoForm(request.POST)
            if form.is_valid():
                video = form.save(commit=False)
                video.room = room
                video.is_attachment = True
                video.order = room.get_attachment_videos().count() + 1
                video.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def delete_video(request, video_id):
    if request.user.is_authenticated():
        video = Video.objects.get(pk=video_id)
        group_name = video.room.legislative_body_initials
        if belongs_to_group(request.user, group_name):
            video.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def order_videos(request, room_id):
    if request.user.is_authenticated() and request.method == 'POST':
        room = Room.objects.get(pk=room_id)
        group_name = room.legislative_body_initials
        if belongs_to_group(request.user, group_name):
            videos = json.loads(request.POST['data'])
            for video in videos:
                Video.objects.filter(
                    id=video['id']).update(order=video['order'])
            text = {
                'video': True,
                'thumbs_html': room.html_room_thumbnails(),
            }
            Group(room.group_room_name).send(
                {'text': json.dumps(text)}
            )
            return HttpResponse(status=200)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


class VideoDetail(DetailView):
    model = Room
    template_name = 'room.html'

    def get_context_data(self, **kwargs):
        context = super(VideoDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['handler'] = encrypt(str(self.request.user.id).rjust(10))
            context['groups'] = list(self.request.user.groups.all()
                                     .values_list('name', flat=True))
        context['questions'] = sorted(self.object.questions.all(),
                                      key=lambda vote: vote.votes_count,
                                      reverse=True)
        context['domain'] = Site.objects.get_current().domain
        return context


@method_decorator(xframe_options_exempt, name='dispatch')
class WidgetVideoDetail(DetailView):
    model = Room
    template_name = 'widget.html'

    def get_context_data(self, **kwargs):
        context = super(WidgetVideoDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['handler'] = encrypt(str(self.request.user.id).rjust(10))
            context['groups'] = list(self.request.user.groups.all()
                                     .values_list('name', flat=True))
        context['questions'] = sorted(self.object.questions.all(),
                                      key=lambda vote: vote.votes_count,
                                      reverse=True)
        context['domain'] = Site.objects.get_current().domain
        return context


class RoomReportView(DetailView):
    model = Room
    template_name = 'room_report.html'

    def get_context_data(self, **kwargs):
        context = super(RoomReportView, self).get_context_data(**kwargs)
        context['questions'] = sorted(self.object.questions.all(),
                                      key=lambda vote: vote.votes_count,
                                      reverse=True)
        context['messages'] = self.object.messages.all().order_by('-created')
        return context


class ClosedVideos(ListView):
    model = Room
    template_name = 'video-list.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        initial_date = self.request.GET.get('initial_date')
        end_date = self.request.GET.get('end_date')
        object_list = Room.objects.filter(
            is_visible=True, youtube_status=2).order_by('-date')
        if q:
            object_list = object_list.filter(Q(
                title_reunion__icontains=q) | Q(
                legislative_body_initials__icontains=q) | Q(
                legislative_body__icontains=q) | Q(
                reunion_type__icontains=q) | Q(
                reunion_object__icontains=q) | Q(
                reunion_theme__icontains=q))
        if initial_date:
            initial_date = datetime.strptime(initial_date, '%d/%m/%Y')
            object_list = object_list.filter(date__gte=initial_date)
        if end_date:
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
            object_list = object_list.filter(date__lte=end_date)
        return object_list


class RoomQuestionList(DetailView):
    model = Room
    template_name = 'room_questions_list.html'

    def get_context_data(self, **kwargs):
        context = super(RoomQuestionList, self).get_context_data(**kwargs)
        priorities = self.object.questions.filter(
            is_priority=True, answered=False)
        other = self.object.questions.filter(is_priority=False, answered=False)
        answered = self.object.questions.filter(answered=True)
        priority_questions = sorted(
            priorities, key=lambda vote: vote.votes_count, reverse=True)
        other_questions = sorted(
            other, key=lambda vote: vote.votes_count, reverse=True)
        answered_questions = sorted(
            answered, key=lambda vote: vote.votes_count, reverse=True)
        context['no_offset_top'] = 'no-offset-top'
        context['questions'] = list(chain(
            priority_questions, other_questions, answered_questions))
        context['counter'] = self.object.questions.count()
        if self.request.user.is_authenticated():
            context['handler'] = encrypt(str(self.request.user.id).rjust(10))
        return context

    def get_queryset(self):
        room = Room.objects.get(pk=self.kwargs.get('pk', None))
        group_name = room.legislative_body_initials
        if belongs_to_group(self.request.user, group_name):
            return Room.objects.filter(pk=self.kwargs.get('pk', None))
        else:
            raise Http404()


class QuestionDetail(DetailView):
    model = Question
    template_name = 'question_meta.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context['domain'] = Site.objects.get_current().domain
        context['domain'] += settings.FORCE_SCRIPT_NAME

        return context
