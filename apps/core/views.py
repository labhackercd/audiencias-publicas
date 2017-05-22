from django.conf import settings
from django.http import (Http404, HttpResponseForbidden,
                         HttpResponseBadRequest)
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from apps.core.models import Question, Room
from apps.core.utils import encrypt
from apps.core.templatetags.video_utils import belongs_to_group
from django.views.generic import DetailView, ListView
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime
from django.db.models import Q
from channels import Group
import json


def set_answer_time(request, question_id):
    if request.user.is_authenticated() and request.method == 'POST':
        answer_time = request.POST.get('answered_time')
        if answer_time:
            time = datetime.strptime(answer_time, '%H:%M:%S')
            seconds = time.second
            seconds += time.minute * 60
            seconds += time.hour * 3600

            question = Question.objects.get(pk=question_id)
            question.answer_time = seconds
            question.save()
            return redirect('video_room', pk=question.room.pk)
        else:
            return HttpResponseBadRequest('Invalid date format.')
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

            question.save()
            vote_list = []
            for vote in question.votes.all():
                vote_list.append(encrypt(str(vote.user.id).rjust(10)))

            html = question.html_question_body(request.user)
            text = {
                'html': html,
                'id': question.id,
                'voteList': vote_list,
                'answered': question.answered,
                'groupName': group_name,
            }
            Group(question.room.group_questions_name).send(
                {'text': json.dumps(text)}
            )
            return redirect('video_room', pk=question.room.pk)
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
        agendas=Room.objects.filter(Q(
            is_visible=True,
            reunion_status=2,
            youtube_id='') | Q(
            is_visible=True,
            reunion_status=2,
            youtube_id__isnull=True)).order_by('date'),
    ))


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
        context['answer_time'] = self.request.GET.get('t', None)
        context['domain'] = Site.objects.get_current().domain
        context['domain'] += settings.FORCE_SCRIPT_NAME
        context['url_prefix'] = settings.FORCE_SCRIPT_NAME
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


class VideoReunionDetail(DetailView):
    model = Room
    template_name = 'room.html'

    def get_context_data(self, **kwargs):
        context = super(VideoReunionDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['handler'] = encrypt(str(self.request.user.id).rjust(10))
        context['questions'] = sorted(self.object.questions.all(),
                                      key=lambda vote: vote.votes_count,
                                      reverse=True)
        context['answer_time'] = self.request.GET.get('t', None)
        context['domain'] = Site.objects.get_current().domain
        context['domain'] += settings.FORCE_SCRIPT_NAME

        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        cod_reunion = self.kwargs.get('cod_reunion')
        if cod_reunion is not None:
            queryset = queryset.filter(
                cod_reunion=cod_reunion, is_visible=True)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


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
                legislative_body_alias__icontains=q) | Q(
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
        questions = self.object.questions.all()
        context['no_offset_top'] = 'no-offset-top'
        context['questions'] = sorted(questions,
                                      key=lambda vote: vote.votes_count,
                                      reverse=True)

        return context


class QuestionDetail(DetailView):
    model = Question
    template_name = 'question_meta.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context['domain'] = Site.objects.get_current().domain
        context['domain'] += settings.FORCE_SCRIPT_NAME

        return context
