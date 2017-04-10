from django.conf import settings
from django.http import Http404
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from apps.core.models import Question, Room
from apps.core.utils import encrypt
from django.views.generic import DetailView, ListView
from django.shortcuts import render


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
            reunion_status=2,
            youtube_id__isnull=True).order_by('date'),
    ))


class VideoDetail(DetailView):
    model = Room
    template_name = 'room.html'

    def get_context_data(self, **kwargs):
        context = super(VideoDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['handler'] = encrypt(str(self.request.user.id).rjust(10))
        context['questions'] = sorted(self.object.questions.all(),
                                      key=lambda vote: vote.votes_count,
                                      reverse=True)
        context['answer_time'] = self.request.GET.get('t', None)
        context['domain'] = Site.objects.get_current().domain
        context['domain'] += settings.FORCE_SCRIPT_NAME

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
        return Room.objects.filter(
            is_visible=True,
            youtube_status=2,
        ).order_by('-date')


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
