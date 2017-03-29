# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-20 13:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def migrate_to_room(apps, schema_editor):
    Room = apps.get_model("core", "Room")
    Video = apps.get_model("core", "Video")
    Message = apps.get_model("core", "Message")
    Question = apps.get_model("core", "Question")

    for video in Video.objects.all():
        room = Room()
        room.video = video
        room.save()
        for question in Question.objects.filter(video=video):
            question.room = room
            question.save()
        for message in Message.objects.filter(video=video):
            message.room = room
            message.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20170123_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('cod_reunion', models.CharField(blank=True, max_length=200, null=True)),
                ('online_users', models.IntegerField(default=0)),
                ('max_online_users', models.IntegerField(default=0)),
                ('is_visible', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'room',
                'verbose_name_plural': 'rooms',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('text', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
        ),
        migrations.RemoveField(
            model_name='video',
            name='max_online_users',
        ),
        migrations.RemoveField(
            model_name='video',
            name='online_users',
        ),
        migrations.AddField(
            model_name='agenda',
            name='cod_reunion',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='video',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='core.Video'),
        ),
        migrations.AddField(
            model_name='room',
            name='agenda',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room', to='core.Agenda'),
        ),
        migrations.AddField(
            model_name='room',
            name='video',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room', to='core.Video'),
        ),
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='core.Room'),
        ),
        migrations.AddField(
            model_name='question',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='core.Room'),
        ),
        migrations.RunPython(
            migrate_to_room
        ),
        migrations.RemoveField(
            model_name='message',
            name='video',
        ),
        migrations.RemoveField(
            model_name='question',
            name='video',
        ),
    ]
