from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from datetime import datetime
from dateutil.relativedelta import relativedelta
from apps.core.models import Room, Video
import requests
import json
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import re


class Command(BaseCommand):
    def handle(self, *args, **options):
        today = datetime.today()
        final_date = datetime.today() + relativedelta(months=3)
        params = {'dataInicial': today.strftime('%d/%m/%Y'),
                  'dataFinal': final_date.strftime('%d/%m/%Y'),
                  'codComissao': '0',
                  'bolEdemocracia': '1'}
        response = requests.get(
            settings.WEBSERVICE_URL,
            params=params, verify=False)
        data = json.loads(response.text)
        allowed_rooms = []
        for item in data:
            if item['codReuniao'] == item['codReuniaoPrincipal']:
                room, room_created = Room.objects.get_or_create(
                    cod_reunion=item['codReuniao'])
                room_videos = room.videos.values_list('video_id', flat=True)
                if item['idYoutube'] and not item['idYoutube'] in room_videos:
                    Video.objects.create(room=room, video_id=item['idYoutube'])
                    room.closed_time = None
                if item['bolReuniaoConjunta']:
                    room.title_reunion = item['txtTituloReuniao']
                else:
                    room.title_reunion = item['txtApelido']
                room.reunion_theme = item['txtTemaReuniao']
                room.legislative_body_initials = item['txtSiglaOrgao']
                room.legislative_body = item['txtNomeOrgao']
                room.reunion_type = item['txtTipoReuniao']
                room.reunion_object = item['txtObjeto']
                room.location = item['txtLocal']
                room.is_visible = item['bolHabilitarEventoInterativo']
                if item['codEstadoReuniao'] in [5, 6]:
                    room.is_visible = False
                room.youtube_status = item['codEstadoTransmissaoYoutube']
                if item['datSisAudio'] == "":
                    date = datetime.strptime(item['datReuniaoString'],
                                             '%d/%m/%Y %H:%M:%S')
                else:
                    date = datetime.strptime(item['datSisAudio'],
                                             '%d/%m/%Y %H:%M:%S')
                room.date = date
                if room.reunion_object:
                    lines = room.reunion_object.splitlines()
                    lines = list(filter(str.strip, lines))
                    for i, line in enumerate(lines):
                        if line.startswith('ORGANIZADO POR:'):
                            try:
                                names = lines[i + 1].split('-')
                                room.legislative_body_initials = names[0].strip()
                                room.legislative_body = names[1].strip()
                            except IndexError:
                                pass
                    if not room.reunion_theme:
                        lines = room.reunion_object.splitlines()
                        lines = list(filter(str.strip, lines))
                        theme = ''
                        for i, line in enumerate(lines):
                            line = line.upper()
                            if line == 'TEMA' or line == 'TEMA:':
                                theme = lines[i + 1].upper()
                            elif 'TEMA:' in line:
                                theme = re.sub(r'.*TEMA:', '', line).strip()
                            if theme is not '':
                                if theme.startswith('"'):
                                    theme = re.findall(r'"(.*?)"', theme)[0]
                                elif theme.startswith('“'):
                                    theme = re.findall(r'“(.*?)”', theme)[0]
                                elif theme.startswith("'"):
                                    theme = re.findall(r"'(.*?)'", theme)[0]
                                room.reunion_theme = theme
                room.save()
                Group.objects.get_or_create(
                    name=room.legislative_body_initials
                )
                if room_created:
                    domain = Site.objects.get_current().domain
                    html = render_to_string('email/new-room.html',
                                            {'domain': domain, 'room': room})
                    subject = u'[Audiências Interativas] Nova sala criada'
                    mail = EmailMultiAlternatives(
                        subject, '',
                        settings.EMAIL_HOST_USER,
                        settings.NOTIFICATION_EMAIL_LIST
                    )
                    mail.attach_alternative(html, 'text/html')
                    mail.send()
                allowed_rooms.append(item['codReuniao'])
        rooms_without_interaction = Room.objects.filter(
            date__gte=today).exclude(cod_reunion__in=allowed_rooms).exclude(
            cod_reunion='').exclude(cod_reunion__isnull=True).exclude(
            youtube_status=2)
        rooms_without_interaction.update(is_visible=False)
