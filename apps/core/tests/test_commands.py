import pytest
import responses
from responses import matchers
from mixer.backend.django import mixer
from django.conf import settings
from apps.core.models import Room
from apps.core.tests.mock_infoleg_api import RESPONSE_API
from django.core.management import call_command
from datetime import date
from dateutil.relativedelta import relativedelta


TEST_WEBSERVICE_URL = 'https://webservice-test.camara.leg.br'


@pytest.mark.django_db
@responses.activate
def test_camara_webservice():
    settings.WEBSERVICE_URL = TEST_WEBSERVICE_URL
    today = date.today()
    final_date = today + relativedelta(months=3)
    params = {'dataInicial': today.strftime('%d/%m/%Y'),
              'dataFinal': final_date.strftime('%d/%m/%Y'),
              'codComissao': '0',
              'bolEdemocracia': '1'}
    
    responses.add(
        method=responses.GET,
        url=TEST_WEBSERVICE_URL,
        match=[
            matchers.query_param_matcher(params)
        ],
        match_querystring=False,
        status=201,
        json=RESPONSE_API, 
    )
    
    mixer.blend(Room, cod_reunion=63610, youtube_status=1)
    
    call_command("get_camara_webservice")

    assert Room.objects.all().count() == 3