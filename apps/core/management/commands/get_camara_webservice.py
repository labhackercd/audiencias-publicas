from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from datetime import datetime
from dateutil.relativedelta import relativedelta
from apps.core.models import Room
import requests
import json
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


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
            room_created = False
            has_video = item['idYoutube'] != ""
            if item['codReuniao'] == item['codReuniaoPrincipal']:
                rooms = Room.objects.filter(cod_reunion=item['codReuniao'])
                if rooms.count() == 0:
                    room = Room.objects.create(
                        cod_reunion=item['codReuniao'],
                        youtube_id=item['idYoutube'])
                    room_created = True
                elif rooms.count() == 1:
                    room = rooms.latest('id')
                    if room.youtube_id != item['idYoutube'] and has_video:
                        if room.youtube_id == "" or room.youtube_id is None or \
                                room.cod_audio == str(item['codAudio']):
                            room.youtube_id = item['idYoutube']
                        else:
                            room, room_created = Room.objects.get_or_create(
                                cod_reunion=item['codReuniao'],
                                youtube_id=item['idYoutube'])
                else:
                    room, room_created = Room.objects.get_or_create(
                        cod_reunion=item['codReuniao'],
                        youtube_id=item['idYoutube'])
                room.reunion_theme = item['txtTemaReuniao']
                room.title_reunion = item['txtTituloReuniao']
                room.cod_audio = item['codAudio']
                room.legislative_body_initials = item['txtSiglaOrgao']
                room.legislative_body_alias = item['txtApelido']
                room.legislative_body = item['txtNomeOrgao']
                room.reunion_status = item['codEstadoReuniao']
                room.reunion_type = item['txtTipoReuniao']
                room.reunion_object = item['txtObjeto']
                room.location = item['txtLocal']
                room.is_joint = item['bolReuniaoConjunta']
                room.is_visible = item['bolHabilitarEventoInterativo']
                room.youtube_status = item['codEstadoTransmissaoYoutube']
                if item['datSisAudio'] == "":
                    date = datetime.strptime(item['datReuniaoString'],
                                             '%d/%m/%Y %H:%M:%S')
                else:
                    date = datetime.strptime(item['datSisAudio'],
                                             '%d/%m/%Y %H:%M:%S')
                room.date = date
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
