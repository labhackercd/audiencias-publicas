from django.conf import settings


def analytics(request):
    analytics_id = settings.GOOGLE_ANALYTICS_ID
    return {'analytics_id': analytics_id}
