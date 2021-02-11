from audiencias_publicas.celery import app
from django.contrib.auth import get_user_model
from apps.reports.models import (NewUsers, VotesReport, RoomsReport,
                                 QuestionsReport)
from apps.core.models import UpDownVote, Room, Question
from collections import Counter
from datetime import date, timedelta
import calendar
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Sum


def create_new_users_object(registers_by_date, period='daily'):
    if period == 'daily':
        registers_count = registers_by_date[1]
        start_date = end_date = registers_by_date[0]

    else:
        registers_count = registers_by_date['total_registers']

        if period == 'monthly':
            start_date = registers_by_date['month']
            last_day = calendar.monthrange(start_date.year,
                                           start_date.month)[1]
            end_date = start_date.replace(day=last_day)

        elif period == 'yearly':
            start_date = registers_by_date['year']
            end_date = start_date.replace(day=31, month=12)

    report_object = NewUsers(start_date=start_date, end_date=end_date,
                             new_users=registers_count, period=period)
    return report_object


@app.task(name="get_new_users_daily")
def get_new_users_daily(start_date=None):
    batch_size = 100
    yesterday = date.today() - timedelta(days=1)

    if not start_date:
        start_date = yesterday.strftime('%Y-%m-%d')

    users = get_user_model().objects.filter(date_joined__gte=start_date)

    date_joined_list = [user.date_joined.strftime('%Y-%m-%d')
                        for user in users]

    registers_by_day = Counter(date_joined_list)

    registers_daily = [create_new_users_object(result, 'daily')
                       for result in registers_by_day.items()]

    NewUsers.objects.bulk_create(registers_daily, batch_size)


@app.task(name="get_new_users_monthly")
def get_new_users_monthly(start_date=None):
    batch_size = 100
    end_date = date.today()

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
    today = date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]

    if not start_date:
        start_date = today.replace(day=1).strftime('%Y-%m-%d')

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
    if period == 'daily':
        votes_count = votes_by_date[1]
        start_date = end_date = votes_by_date[0]

    else:
        votes_count = votes_by_date['total_votes']

        if period == 'monthly':
            start_date = votes_by_date['month']
            last_day = calendar.monthrange(start_date.year,
                                           start_date.month)[1]
            end_date = start_date.replace(day=last_day)

        elif period == 'yearly':
            start_date = votes_by_date['year']
            end_date = start_date.replace(day=31, month=12)

    report_object = VotesReport(start_date=start_date, end_date=end_date,
                                votes=votes_count, period=period)
    return report_object


@app.task(name="get_votes_daily")
def get_votes_daily(start_date=None):
    batch_size = 100
    yesterday = date.today() - timedelta(days=1)

    if not start_date:
        start_date = yesterday.strftime('%Y-%m-%d')

    votes = UpDownVote.objects.filter(created__gte=start_date)

    votes_by_date_list = [vote.created.strftime('%Y-%m-%d')
                          for vote in votes]

    votes_by_day = Counter(votes_by_date_list)

    votes_daily = [create_votes_object(result, 'daily')
                   for result in votes_by_day.items()]

    VotesReport.objects.bulk_create(votes_daily, batch_size)


@app.task(name="get_votes_monthly")
def get_votes_monthly(start_date=None):
    batch_size = 100
    end_date = date.today()

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
    today = date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]

    if not start_date:
        start_date = today.replace(day=1).strftime('%Y-%m-%d')

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
    if period == 'daily':
        rooms_count = rooms_by_date[1]
        start_date = end_date = rooms_by_date[0]

    else:
        rooms_count = rooms_by_date['total_rooms']

        if period == 'monthly':
            start_date = rooms_by_date['month']
            last_day = calendar.monthrange(start_date.year,
                                           start_date.month)[1]
            end_date = start_date.replace(day=last_day)

        elif period == 'yearly':
            start_date = rooms_by_date['year']
            end_date = start_date.replace(day=31, month=12)

    report_object = RoomsReport(start_date=start_date, end_date=end_date,
                                rooms=rooms_count, period=period)
    return report_object


@app.task(name="get_rooms_daily")
def get_rooms_daily(start_date=None):
    batch_size = 100
    yesterday = date.today() - timedelta(days=1)

    if not start_date:
        start_date = yesterday.strftime('%Y-%m-%d')

    rooms = Room.objects.filter(created__gte=start_date)

    rooms_by_date_list = [room.created.strftime('%Y-%m-%d')
                          for room in rooms]

    rooms_by_day = Counter(rooms_by_date_list)

    rooms_daily = [create_rooms_object(result, 'daily')
                   for result in rooms_by_day.items()]

    RoomsReport.objects.bulk_create(rooms_daily, batch_size)


@app.task(name="get_rooms_monthly")
def get_rooms_monthly(start_date=None):
    batch_size = 100
    end_date = date.today()

    if not start_date:
        start_date = end_date.replace(day=1).strftime('%Y-%m-%d')

    rooms_daily = RoomsReport.objects.filter(
        period='daily',
        start_date__gte=start_date,
        end_date__lte=end_date.strftime('%Y-%m-%d'))

    rooms_by_month = rooms_daily.annotate(
        month=TruncMonth('start_date')).values('month').annotate(
            total_rooms=Sum('rooms')).values(
                'month', 'total_rooms')

    rooms_monthly = [create_rooms_object(result, 'monthly')
                         for result in rooms_by_month]

    RoomsReport.objects.bulk_create(rooms_monthly, batch_size)


@app.task(name="get_rooms_yearly")
def get_rooms_yearly(start_date=None):
    batch_size = 100
    today = date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]

    if not start_date:
        start_date = today.replace(day=1).strftime('%Y-%m-%d')

    rooms_monthly = RoomsReport.objects.filter(
        period='monthly',
        start_date__gte=start_date,
        end_date__lte=today.replace(day=last_day).strftime('%Y-%m-%d'))

    rooms_by_year = rooms_monthly.annotate(
        year=TruncYear('start_date')).values('year').annotate(
            total_rooms=Sum('rooms')).values(
                'year', 'total_rooms')

    rooms_yearly = [create_rooms_object(result, 'yearly')
                    for result in rooms_by_year]

    RoomsReport.objects.bulk_create(rooms_yearly, batch_size)


def create_questions_object(questions_by_date, period='daily'):
    if period == 'daily':
        questions_count = questions_by_date[1]
        start_date = end_date = questions_by_date[0]

    else:
        questions_count = questions_by_date['total_questions']

        if period == 'monthly':
            start_date = questions_by_date['month']
            last_day = calendar.monthrange(start_date.year,
                                           start_date.month)[1]
            end_date = start_date.replace(day=last_day)

        elif period == 'yearly':
            start_date = questions_by_date['year']
            end_date = start_date.replace(day=31, month=12)

    report_object = QuestionsReport(start_date=start_date, end_date=end_date,
                                    questions=questions_count, period=period)
    return report_object


@app.task(name="get_questions_daily")
def get_questions_daily(start_date=None):
    batch_size = 100
    yesterday = date.today() - timedelta(days=1)

    if not start_date:
        start_date = yesterday.strftime('%Y-%m-%d')

    questions = Question.objects.filter(created__gte=start_date)

    questions_by_date_list = [question.created.strftime('%Y-%m-%d')
                          for question in questions]

    questions_by_day = Counter(questions_by_date_list)

    questions_daily = [create_questions_object(result, 'daily')
                   for result in questions_by_day.items()]

    QuestionsReport.objects.bulk_create(questions_daily, batch_size)


@app.task(name="get_questions_monthly")
def get_questions_monthly(start_date=None):
    batch_size = 100
    end_date = date.today()

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
    today = date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]

    if not start_date:
        start_date = today.replace(day=1).strftime('%Y-%m-%d')

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