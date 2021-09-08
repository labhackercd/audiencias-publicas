# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2021-04-20 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MessagesReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('start_date', models.DateField(db_index=True, verbose_name='start date')),
                ('end_date', models.DateField(db_index=True, verbose_name='end date')),
                ('period', models.CharField(choices=[('daily', 'Daily'), ('monthly', 'Monthly'), ('yearly', 'Yearly'), ('all', 'All the time')], db_index=True, default='daily', max_length=200, verbose_name='period')),
                ('messages', models.IntegerField(blank=True, default=0, null=True, verbose_name='messages')),
            ],
            options={
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
            },
        ),
        migrations.CreateModel(
            name='NewUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('start_date', models.DateField(db_index=True, verbose_name='start date')),
                ('end_date', models.DateField(db_index=True, verbose_name='end date')),
                ('period', models.CharField(choices=[('daily', 'Daily'), ('monthly', 'Monthly'), ('yearly', 'Yearly'), ('all', 'All the time')], db_index=True, default='daily', max_length=200, verbose_name='period')),
                ('new_users', models.IntegerField(blank=True, default=0, null=True, verbose_name='new users')),
            ],
            options={
                'verbose_name': 'new user',
                'verbose_name_plural': 'new users',
            },
        ),
        migrations.CreateModel(
            name='ParticipantsReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('start_date', models.DateField(db_index=True, verbose_name='start date')),
                ('end_date', models.DateField(db_index=True, verbose_name='end date')),
                ('period', models.CharField(choices=[('daily', 'Daily'), ('monthly', 'Monthly'), ('yearly', 'Yearly'), ('all', 'All the time')], db_index=True, default='daily', max_length=200, verbose_name='period')),
                ('participants', models.IntegerField(blank=True, default=0, null=True, verbose_name='participants')),
            ],
            options={
                'verbose_name': 'participant',
                'verbose_name_plural': 'participants',
            },
        ),
        migrations.CreateModel(
            name='QuestionsReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('start_date', models.DateField(db_index=True, verbose_name='start date')),
                ('end_date', models.DateField(db_index=True, verbose_name='end date')),
                ('period', models.CharField(choices=[('daily', 'Daily'), ('monthly', 'Monthly'), ('yearly', 'Yearly'), ('all', 'All the time')], db_index=True, default='daily', max_length=200, verbose_name='period')),
                ('questions', models.IntegerField(blank=True, default=0, null=True, verbose_name='questions')),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
            },
        ),
        migrations.CreateModel(
            name='RoomsReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('start_date', models.DateField(db_index=True, verbose_name='start date')),
                ('end_date', models.DateField(db_index=True, verbose_name='end date')),
                ('period', models.CharField(choices=[('daily', 'Daily'), ('monthly', 'Monthly'), ('yearly', 'Yearly'), ('all', 'All the time')], db_index=True, default='daily', max_length=200, verbose_name='period')),
                ('finished_rooms', models.IntegerField(blank=True, default=0, null=True, verbose_name='finished rooms')),
                ('canceled_rooms', models.IntegerField(blank=True, default=0, null=True, verbose_name='canceled rooms')),
                ('total_rooms', models.IntegerField(blank=True, default=0, null=True, verbose_name='total rooms')),
            ],
            options={
                'verbose_name': 'room',
                'verbose_name_plural': 'rooms',
            },
        ),
        migrations.CreateModel(
            name='VotesReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('start_date', models.DateField(db_index=True, verbose_name='start date')),
                ('end_date', models.DateField(db_index=True, verbose_name='end date')),
                ('period', models.CharField(choices=[('daily', 'Daily'), ('monthly', 'Monthly'), ('yearly', 'Yearly'), ('all', 'All the time')], db_index=True, default='daily', max_length=200, verbose_name='period')),
                ('votes', models.IntegerField(blank=True, default=0, null=True, verbose_name='votes')),
            ],
            options={
                'verbose_name': 'vote',
                'verbose_name_plural': 'votes',
            },
        ),
        migrations.AlterUniqueTogether(
            name='votesreport',
            unique_together=set([('start_date', 'period')]),
        ),
        migrations.AlterUniqueTogether(
            name='roomsreport',
            unique_together=set([('start_date', 'period')]),
        ),
        migrations.AlterUniqueTogether(
            name='questionsreport',
            unique_together=set([('start_date', 'period')]),
        ),
        migrations.AlterUniqueTogether(
            name='participantsreport',
            unique_together=set([('start_date', 'period')]),
        ),
        migrations.AlterUniqueTogether(
            name='newusers',
            unique_together=set([('start_date', 'period')]),
        ),
        migrations.AlterUniqueTogether(
            name='messagesreport',
            unique_together=set([('start_date', 'period')]),
        ),
    ]
