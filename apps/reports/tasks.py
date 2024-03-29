from audiencias_publicas.celery import app
from django.contrib.auth import get_user_model
from apps.reports.models import (NewUsers, VotesReport, RoomsReport,
                                 QuestionsReport, MessagesReport,
                                 ParticipantsReport)
from apps.core.models import UpDownVote, Room, Question, Message
from collections import Counter
from datetime import date, timedelta
import calendar
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Sum
from django.utils import timezone


def create_new_users_object(registers_by_date, period='daily'):
    yesterday = timezone.now().date() - timedelta(days=1)

    if period == 'daily':
        registers_count = registers_by_date[1]
        start_date = end_date = registers_by_date[0]

    else:
        registers_count = registers_by_date['total_registers']

        if period == 'monthly':
            start_date = registers_by_date['month']
            if (start_date.year == yesterday.year and
                start_date.month == yesterday.month):
                end_date = yesterday.strftime('%Y-%m-%d')
            else:
                last_day = calendar.monthrange(start_date.year,
                                               start_date.month)[1]
                end_date = start_date.replace(day=last_day)

        elif period == 'yearly':
            start_date = registers_by_date['year']
            if start_date.year == yesterday.year:
                end_date = yesterday.strftime('%Y-%m-%d')
            else:
                end_date = start_date.replace(day=31, month=12)

        if NewUsers.objects.filter(
            start_date=start_date, period=period).exists():
            NewUsers.objects.filter(
                start_date=start_date, period=period).delete()

    report_object = NewUsers(start_date=start_date, end_date=end_date,
                             new_users=registers_count, period=period)
    return report_object


@app.task(name="get_new_users_daily")
def get_new_users_daily(start_date=None):
    batch_size = 100
    yesterday = timezone.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=23, minute=59, second=59)

    if not start_date:
        start_date = yesterday.replace(
            hour=0, minute=0, second=0, microsecond=0)

    users = get_user_model().objects.filter(date_joined__gte=start_date,
                                            date_joined__lte=yesterday)

    date_joined_list = [user.date_joined.strftime('%Y-%m-%d')
                        for user in users]

    registers_by_day = Counter(date_joined_list)

    registers_daily = [create_new_users_object(result, 'daily')
                       for result in registers_by_day.items()]

    NewUsers.objects.bulk_create(registers_daily, batch_size)


@app.task(name="get_new_users_monthly")
def get_new_users_monthly(start_date=None):
    batch_size = 100
    end_date = timezone.now().date()

    if not start_date:
        start_date = end_date.replace(day=1).strftime('%Y-%m-%d')

    registers_daily = NewUsers.objects.filter(
        period='daily',
        start_date__gte=start_date,
        end_date__lte=end_date.strftime('%Y-%m-%d'))

    data_by_month = registers_daily.annotate(
        month=TruncMonth('start_date')).values('month').annotate(
            total_registers=Sum('new_users')).values(
                'month', 'total_registers')

    registers_monthly = [create_new_users_object(result, 'monthly')
                         for result in data_by_month]

    NewUsers.objects.bulk_create(registers_monthly, batch_size)


@app.task(name="get_new_users_yearly")
def get_new_users_yearly(start_date=None):
    batch_size = 100
    today = timezone.now().date()
    last_day = calendar.monthrange(today.year, today.month)[1]

    if not start_date:
        start_date = today.replace(day=1, month=1).strftime('%Y-%m-%d')

    registers_monthly = NewUsers.objects.filter(
        period='monthly',
        start_date__gte=start_date,
        end_date__lte=today.replace(day=last_day).strftime('%Y-%m-%d'))

    data_by_year = registers_monthly.annotate(
        year=TruncYear('start_date')).values('year').annotate(
            total_registers=Sum('new_users')).values(
                'year', 'total_registers')

    registers_yearly = [create_new_users_object(result, 'yearly')
                        for result in data_by_year]

    NewUsers.objects.bulk_create(registers_yearly, batch_size)


def create_votes_object(votes_by_date, period='daily'):
    yesterday = timezone.now().date() - timedelta(days=1)

    if period == 'daily':
        votes_count = votes_by_date[1]
        start_date = end_date = votes_by_date[0]

    else:
        votes_count = votes_by_date['total_votes']

        if period == 'monthly':
            start_date = votes_by_date['month']
            if (start_date.year == yesterday.year and
                start_date.month == yesterday.month):
                end_date = yesterday.strftime('%Y-%m-%d')
            else:
                last_day = calendar.monthrange(start_date.year,
                                               start_date.month)[1]
                end_date = start_date.replace(day=last_day)

        elif period == 'yearly':
            start_date = votes_by_date['year']
            if start_date.year == yesterday.year:
                end_date = yesterday.strftime('%Y-%m-%d')
            else:
                end_date = start_date.replace(day=31, month=12)

        if VotesReport.objects.filter(
            start_date=start_date, period=period).exists():
            VotesReport.objects.filter(
                start_date=start_date, period=period).delete()

    report_object = VotesReport(start_date=start_date, end_date=end_date,
                                votes=votes_count, period=period)
    return report_object


@app.task(name="get_votes_daily")
def get_votes_daily(start_date=None):
    batch_size = 100
    yesterday = timezone.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=23, minute=59, second=59)

    if not start_date:
        start_date = yesterday.replace(
            hour=0, minute=0, second=0, microsecond=0)

    votes = UpDownVote.objects.filter(created__gte=start_date,
                                      created__lte=yesterday)

    votes_by_date_list = [vote.created.strftime('%Y-%m-%d')
                          for vote in votes]

    votes_by_day = Counter(votes_by_date_list)

    votes_daily = [create_votes_object(result, 'daily')
                   for result in votes_by_day.items()]

    VotesReport.objects.bulk_create(votes_daily, batch_size)


@app.task(name="get_votes_monthly")
def get_votes_monthly(start_date=None):
    batch_size = 100
    end_date = timezone.now().date()

    if not start_date:
        start_date = end_date.replace(day=1).strftime('%Y-%m-%d')

    votes_daily = VotesReport.objects.filter(
        period='daily',
        start_date__gte=start_date,
        end_date__lte=end_date.strftime('%Y-%m-%d'))

    votes_by_month = votes_daily.annotate(
        month=TruncMonth('start_date')).values('month').annotate(
            total_votes=Sum('votes')).values(
                'month', 'total_votes')

    votes_monthly = [create_votes_object(result, 'monthly')
                         for result in votes_by_month]

    VotesReport.objects.bulk_create(votes_monthly, batch_size)


@app.task(name="get_votes_yearly")
def get_votes_yearly(start_date=None):
    batch_size = 100
    today = timezone.now().date()
    last_day = calendar.monthrange(today.year, today.month)[1]

    if not start_date:
        start_date = today.replace(day=1, month=1).strftime('%Y-%m-%d')

    votes_monthly = VotesReport.objects.filter(
        period='monthly',
        start_date__gte=start_date,
        end_date__lte=today.replace(day=last_day).strftime('%Y-%m-%d'))

    votes_by_year = votes_monthly.annotate(
        year=TruncYear('start_date')).values('year').annotate(
            total_votes=Sum('votes')).values(
                'year', 'total_votes')

    votes_yearly = [create_votes_object(result, 'yearly')
                    for result in votes_by_year]

    VotesReport.objects.bulk_create(votes_yearly, batch_size)


def create_rooms_object(rooms_by_date, period='daily'):
    yesterday = timezone.now().date() - timedelta(days=1)

    if period == 'daily':
        total_rooms = rooms_by_date[1][0]
        finished_rooms = rooms_by_date[1][1]
        canceled_rooms = rooms_by_date[1][2]
        start_date = end_date = rooms_by_date[0]

    else:
        total_rooms = rooms_by_date['total']
        finished_rooms = rooms_by_date['finished']
        canceled_rooms = rooms_by_date['canceled']

        if period == 'monthly':
            start_date = rooms_by_date['month']
            if (start_date.year == yesterday.year and
                start_date.month == yesterday.month):
                end_date = yesterday.strftime('%Y-%m-%d')
            else:
                last_day = calendar.monthrange(start_date.year,
                                               start_date.month)[1]
                end_date = start_date.replace(day=last_day)

        elif period == 'yearly':
            start_date = rooms_by_date['year']
            if start_date.year == yesterday.year:
                end_date = yesterday.strftime('%Y-%m-%d')
            else:
                end_date = start_date.replace(day=31, month=12)

        if RoomsReport.objects.filter(
            start_date=start_date, period=period).exists():
            RoomsReport.objects.filter(
                start_date=start_date, period=period).delete()

    report_object = RoomsReport(start_date=start_date, end_date=end_date,
                                period=period, total_rooms=total_rooms,
                                finished_rooms=finished_rooms,
                                canceled_rooms=canceled_rooms)
    return report_object


@app.task(name="get_rooms_daily")
def get_rooms_daily(start_date=None):
    batch_size = 100
    yesterday = timezone.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=23, minute=59, second=59)

    if not start_date:
        start_date = yesterday.replace(
            hour=0, minute=0, second=0, microsecond=0)

    total_rooms = Room.objects.filter(date__gte=start_date,
                                      date__lte=yesterday)
    finished_rooms = total_rooms.filter(is_active=True)
    canceled_rooms = total_rooms.filter(is_active=False)

    total_by_date_list = [room.date.strftime('%Y-%m-%d')
                          for room in total_rooms]

    finished_by_date_list = [room.date.strftime('%Y-%m-%d')
                             for room in finished_rooms]

    canceled_by_date_list = [room.date.strftime('%Y-%m-%d')
                             for room in canceled_rooms]

    total_by_day = dict(Counter(total_by_date_list))
    finished_by_day = dict(Counter(finished_by_date_list))
    canceled_by_day = dict(Counter(canceled_by_date_list))

    dicts = total_by_day, finished_by_day, canceled_by_day

    result_dict = {day: [d.get(day, 0) for d in dicts]
                       for day in {day for d in dicts for day in d}}

    rooms_daily = [create_rooms_object(result, 'daily')
                   for result in result_dict.items()]

    RoomsReport.objects.bulk_create(rooms_daily, batch_size)


@app.task(name="get_rooms_monthly")
def get_rooms_monthly(start_date=None):
    batch_size = 100
    end_date = timezone.now().date()

    if not start_date:
        start_date = end_date.replace(day=1).strftime('%Y-%m-%d')

    rooms_daily = RoomsReport.objects.filter(
        period='daily',
        start_date__gte=start_date,
        end_date__lte=end_date.strftime('%Y-%m-%d'))

    rooms_by_month = rooms_daily.annotate(
        month=TruncMonth('start_date')).values('month').annotate(
            total=Sum('total_rooms'), finished=Sum('finished_rooms'),
            canceled=Sum('canceled_rooms')).values(
                'month', 'total', 'finished', 'canceled')

    rooms_monthly = [create_rooms_object(result, 'monthly')
                         for result in rooms_by_month]

    RoomsReport.objects.bulk_create(rooms_monthly, batch_size)


@app.task(name="get_rooms_yearly")
def get_rooms_yearly(start_date=None):
    batch_size = 100
    today = timezone.now().date()
    last_day = calendar.monthrange(today.year, today.month)[1]

    if not start_date:
        start_date = today.replace(day=1, month=1).strftime('%Y-%m-%d')

    rooms_monthly = RoomsReport.objects.filter(
        period='monthly',
        start_date__gte=start_date,
        end_date__lte=today.replace(day=last_day).strftime('%Y-%m-%d'))

    rooms_by_year = rooms_monthly.annotate(
        year=TruncYear('start_date')).values('year').annotate(
            total=Sum('total_rooms'), finished=Sum('finished_rooms'),
            canceled=Sum('canceled_rooms')).values(
                'year', 'total', 'finished', 'canceled')

    rooms_yearly = [create_rooms_object(result, 'yearly')
                    for result in rooms_by_year]

    RoomsReport.objects.bulk_create(rooms_yearly, batch_size)


def create_questions_object(questions_by_date, period='daily'):
    yesterday = timezone.now().date() - timedelta(days=1)

    if period == 'daily':
        questions_count = questions_by_date[1]
        start_date = end_date = questions_by_date[0]

    else:
        questions_count = questions_by_date['total_questions']

        if period == 'monthly':
            start_date = questions_by_date['month']
            if (start_date.year == yesterday.year and
                start_date.month == yesterday.month):
                end_date = yesterday.strftime('%Y-%m-%d')
            else:
                last_day = calendar.monthrange(start_date.year,
                                               start_date.month)[1]
                end_date = start_date.replace(day=last_day)

        elif period == 'yearly':
            start_date = questions_by_date['year']
            if start_date.year == yesterday.year:
                end_date = yesterday.strftime('%Y-%m-%d')
            else:
                end_date = start_date.replace(day=31, month=12)

        if QuestionsReport.objects.filter(
            start_date=start_date, period=period).exists():
            QuestionsReport.objects.filter(
                start_date=start_date, period=period).delete()

    report_object = QuestionsReport(start_date=start_date, end_date=end_date,
                                    questions=questions_count, period=period)
    return report_object


@app.task(name="get_questions_daily")
def get_questions_daily(start_date=None):
    batch_size = 100
    yesterday = timezone.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=23, minute=59, second=59)

    if not start_date:
        start_date = yesterday.replace(
            hour=0, minute=0, second=0, microsecond=0)

    questions = Question.objects.filter(created__gte=start_date,
                                        created__lte=yesterday)

    questions_by_date_list = [question.created.strftime('%Y-%m-%d')
                          for question in questions]

    questions_by_day = Counter(questions_by_date_list)

    questions_daily = [create_questions_object(result, 'daily')
                   for result in questions_by_day.items()]

    QuestionsReport.objects.bulk_create(questions_daily, batch_size)


@app.task(name="get_questions_monthly")
def get_questions_monthly(start_date=None):
    batch_size = 100
    end_date = timezone.now().date()

    if not start_date:
        start_date = end_date.replace(day=1).strftime('%Y-%m-%d')

    questions_daily = QuestionsReport.objects.filter(
        period='daily',
        start_date__gte=start_date,
        end_date__lte=end_date.strftime('%Y-%m-%d'))

    questions_by_month = questions_daily.annotate(
        month=TruncMonth('start_date')).values('month').annotate(
            total_questions=Sum('questions')).values(
                'month', 'total_questions')

    questions_monthly = [create_questions_object(result, 'monthly')
                         for result in questions_by_month]

    QuestionsReport.objects.bulk_create(questions_monthly, batch_size)


@app.task(name="get_questions_yearly")
def get_questions_yearly(start_date=None):
    batch_size = 100
    today = timezone.now().date()
    last_day = calendar.monthrange(today.year, today.month)[1]

    if not start_date:
        start_date = today.replace(day=1, month=1).strftime('%Y-%m-%d')

    questions_monthly = QuestionsReport.objects.filter(
        period='monthly',
        start_date__gte=start_date,
        end_date__lte=today.replace(day=last_day).strftime('%Y-%m-%d'))

    questions_by_year = questions_monthly.annotate(
        year=TruncYear('start_date')).values('year').annotate(
            total_questions=Sum('questions')).values(
                'year', 'total_questions')

    questions_yearly = [create_questions_object(result, 'yearly')
                    for result in questions_by_year]

    QuestionsReport.objects.bulk_create(questions_yearly, batch_size)


def create_messages_object(messages_by_date, period='daily'):
    yesterday = timezone.now().date() - timedelta(days=1)

    if period == 'daily':
        messages_count = messages_by_date[1]
        start_date = end_date = messages_by_date[0]

    else:
        messages_count = messages_by_date['total_messages']

        if period == 'monthly':
            start_date = messages_by_date['month']
            if (start_date.year == yesterday.year and
                start_date.month == yesterday.month):
                end_date = yesterday.strftime('%Y-%m-%d')
            else:
                last_day = calendar.monthrange(start_date.year,
                                               start_date.month)[1]
                end_date = start_date.replace(day=last_day)

        elif period == 'yearly':
            start_date = messages_by_date['year']
            if start_date.year == yesterday.year:
                end_date = yesterday.strftime('%Y-%m-%d')
            else:
                end_date = start_date.replace(day=31, month=12)

        if MessagesReport.objects.filter(
            start_date=start_date, period=period).exists():
            MessagesReport.objects.filter(
                start_date=start_date, period=period).delete()

    report_object = MessagesReport(start_date=start_date, end_date=end_date,
                                   messages=messages_count, period=period)
    return report_object


@app.task(name="get_messages_daily")
def get_messages_daily(start_date=None):
    batch_size = 100
    yesterday = timezone.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=23, minute=59, second=59)

    if not start_date:
        start_date = yesterday.replace(
            hour=0, minute=0, second=0, microsecond=0)

    messages = Message.objects.filter(created__gte=start_date,
                                      created__lte=yesterday)

    messages_by_date_list = [message.created.strftime('%Y-%m-%d')
                             for message in messages]

    messages_by_day = Counter(messages_by_date_list)

    messages_daily = [create_messages_object(result, 'daily')
                      for result in messages_by_day.items()]

    MessagesReport.objects.bulk_create(messages_daily, batch_size)


@app.task(name="get_messages_monthly")
def get_messages_monthly(start_date=None):
    batch_size = 100
    end_date = timezone.now().date()

    if not start_date:
        start_date = end_date.replace(day=1).strftime('%Y-%m-%d')

    messages_daily = MessagesReport.objects.filter(
        period='daily',
        start_date__gte=start_date,
        end_date__lte=end_date.strftime('%Y-%m-%d'))

    messages_by_month = messages_daily.annotate(
        month=TruncMonth('start_date')).values('month').annotate(
            total_messages=Sum('messages')).values(
                'month', 'total_messages')

    messages_monthly = [create_messages_object(result, 'monthly')
                         for result in messages_by_month]

    MessagesReport.objects.bulk_create(messages_monthly, batch_size)


@app.task(name="get_messages_yearly")
def get_messages_yearly(start_date=None):
    batch_size = 100
    today = timezone.now().date()
    last_day = calendar.monthrange(today.year, today.month)[1]

    if not start_date:
        start_date = today.replace(day=1, month=1).strftime('%Y-%m-%d')

    messages_monthly = MessagesReport.objects.filter(
        period='monthly',
        start_date__gte=start_date,
        end_date__lte=today.replace(day=last_day).strftime('%Y-%m-%d'))

    messages_by_year = messages_monthly.annotate(
        year=TruncYear('start_date')).values('year').annotate(
            total_messages=Sum('messages')).values(
                'year', 'total_messages')

    messages_yearly = [create_messages_object(result, 'yearly')
                        for result in messages_by_year]

    MessagesReport.objects.bulk_create(messages_yearly, batch_size)


def create_participants_object(participants_by_date, period='daily'):
    yesterday = timezone.now().date() - timedelta(days=1)
    participants_count = participants_by_date[1]

    if period == 'daily':
        start_date = end_date = participants_by_date[0]

    elif period == 'monthly':
        year, month = participants_by_date[0].split('-')
        start_date = date(year=int(year), month=int(month), day=1)
        if (start_date.year == yesterday.year and
            start_date.month == yesterday.month):
            end_date = yesterday.strftime('%Y-%m-%d')
        else:
            last_day = calendar.monthrange(start_date.year,
                                           start_date.month)[1]
            end_date = start_date.replace(day=last_day)

    elif period == 'yearly':
        start_date = date(year=int(participants_by_date[0]), month=1, day=1)
        if start_date.year == yesterday.year:
            end_date = yesterday.strftime('%Y-%m-%d')
        else:
            end_date = start_date.replace(day=31, month=12)

    if ParticipantsReport.objects.filter(
        start_date=start_date, period=period).exists():
        ParticipantsReport.objects.filter(
            start_date=start_date, period=period).delete()

    report_object = ParticipantsReport(start_date=start_date,
        end_date=end_date, participants=participants_count, period=period)

    return report_object


@app.task(name="get_participants_daily")
def get_participants_daily(start_date=None):
    batch_size = 100
    yesterday = timezone.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=23, minute=59, second=59)

    if not start_date:
        start_date = yesterday.replace(
            hour=0, minute=0, second=0, microsecond=0)

    votes = UpDownVote.objects.filter(created__gte=start_date,
                                      created__lte=yesterday)
    vote_users = [(user_id, dt.strftime('%Y-%m-%d'))
                  for user_id, dt in votes.values_list(
                      'user_id', 'created')]

    messages = Message.objects.filter(created__gte=start_date,
                                      created__lte=yesterday)
    message_users = [(user_id, dt.strftime('%Y-%m-%d'))
                     for user_id, dt in messages.values_list(
                        'user_id', 'created')]

    questions = Question.objects.filter(created__gte=start_date,
                                        created__lte=yesterday)
    question_users = [(user_id, dt.strftime('%Y-%m-%d'))
                      for user_id, dt in questions.values_list(
                          'user_id', 'created')]

    participants = list(set(
        list(vote_users) + list(message_users) + list(question_users)))

    participants_by_day = Counter(elem[1] for elem in participants)

    participants_daily = [create_participants_object(result, 'daily')
                      for result in participants_by_day.items()]

    ParticipantsReport.objects.bulk_create(participants_daily, batch_size)


@app.task(name="get_participants_monthly")
def get_participants_monthly(start_date=None):
    batch_size = 100
    yesterday = timezone.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=23, minute=59, second=59)

    if not start_date:
        start_date = yesterday.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)

    votes = UpDownVote.objects.filter(created__gte=start_date,
                                      created__lte=yesterday)
    vote_users = [(user_id, dt.strftime('%Y-%m'))
                  for user_id, dt in votes.values_list(
                      'user_id', 'created')]

    messages = Message.objects.filter(created__gte=start_date,
                                      created__lte=yesterday)
    message_users = [(user_id, dt.strftime('%Y-%m'))
                     for user_id, dt in messages.values_list(
                        'user_id', 'created')]

    questions = Question.objects.filter(created__gte=start_date,
                                        created__lte=yesterday)
    question_users = [(user_id, dt.strftime('%Y-%m'))
                      for user_id, dt in questions.values_list(
                          'user_id', 'created')]

    participants = list(set(
        list(vote_users) + list(message_users) + list(question_users)))

    participants_by_month = Counter(elem[1] for elem in participants)

    participants_monthly = [create_participants_object(result, 'monthly')
                            for result in participants_by_month.items()]

    ParticipantsReport.objects.bulk_create(participants_monthly, batch_size)


@app.task(name="get_participants_yearly")
def get_participants_yearly(start_date=None):
    batch_size = 100
    yesterday = timezone.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=23, minute=59, second=59)

    if not start_date:
        start_date = yesterday.replace(
            day=1, month=1, hour=0, minute=0, second=0, microsecond=0)

    votes = UpDownVote.objects.filter(created__gte=start_date,
                                      created__lte=yesterday)
    vote_users = [(user_id, dt.strftime('%Y'))
                  for user_id, dt in votes.values_list(
                      'user_id', 'created')]

    messages = Message.objects.filter(created__gte=start_date,
                                      created__lte=yesterday)
    message_users = [(user_id, dt.strftime('%Y'))
                     for user_id, dt in messages.values_list(
                        'user_id', 'created')]

    questions = Question.objects.filter(created__gte=start_date,
                                        created__lte=yesterday)
    question_users = [(user_id, dt.strftime('%Y'))
                      for user_id, dt in questions.values_list(
                          'user_id', 'created')]

    participants = list(set(
        list(vote_users) + list(message_users) + list(question_users)))

    participants_by_year = Counter(elem[1] for elem in participants)

    participants_yearly = [create_participants_object(result, 'yearly')
                            for result in participants_by_year.items()]

    ParticipantsReport.objects.bulk_create(participants_yearly, batch_size)


@app.task(name="get_participants_all_the_time")
def get_participants_all_the_time():
    yesterday = timezone.now() - timedelta(days=1)

    vote_users = UpDownVote.objects.all().values_list('user_id')
    message_users = Message.objects.all().values_list('user_id')
    question_users = Question.objects.all().values_list('user_id')

    count_participants = len(list(set(
        list(vote_users) + list(message_users) + list(question_users))))

    first_room = Room.objects.all().order_by('date').first()

    ParticipantsReport.objects.update_or_create(
        period='all',
        start_date=first_room.date,
        defaults={
            'end_date': yesterday,
            'participants': count_participants
        })
