from apps.core.processors import analytics
from django.test import RequestFactory
from django.conf import settings

TEST_GOOGLE_ANALYTICS_ID = 'testGAID'
TEST_OLARK_ID = 'testOID'
TEST_RECAPTCHA_SITE_KEY = 'testRecap'
TEST_CAMARA_LOGIN = True


def test_processors():
    settings.GOOGLE_ANALYTICS_ID = TEST_GOOGLE_ANALYTICS_ID
    settings.OLARK_ID = TEST_OLARK_ID
    settings.RECAPTCHA_SITE_KEY = TEST_RECAPTCHA_SITE_KEY
    settings.CAMARA_LOGIN = TEST_CAMARA_LOGIN

    request = RequestFactory().get('/')
    response = analytics(request)

    assert response['recaptcha_site_key'] == TEST_RECAPTCHA_SITE_KEY
    assert response['olark_id'] == TEST_OLARK_ID
    assert response['analytics_id'] == TEST_GOOGLE_ANALYTICS_ID
    assert response['CAMARA_LOGIN'] == TEST_CAMARA_LOGIN