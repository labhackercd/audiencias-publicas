from django.http import JsonResponse


def initial_view(request):
    data = {}

    return JsonResponse(data)
