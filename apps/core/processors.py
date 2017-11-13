from django.conf import settings


def analytics(request):
    analytics_id = settings.GOOGLE_ANALYTICS_ID
    olark_id = settings.OLARK_ID
    recaptcha_site_key = settings.RECAPTCHA_SITE_KEY
    return {'recaptcha_site_key': recaptcha_site_key,
            'analytics_id': analytics_id, 'olark_id': olark_id}


def home_customization(request):
    return {'site_name': settings.SITE_NAME}
