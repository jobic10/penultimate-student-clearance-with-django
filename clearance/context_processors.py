from django.conf import settings


def SITENAME(request):
    # return {'SITENAME': settings.APP_NAME, 'no_of_weeks': settings.NO_OF_WEEKS}
    context = {'SITENAME': settings.APP_NAME,
               'DEVELOPER': settings.DEVELOPER, 'SUPERVISOR': settings.SUPERVISOR}
    return context
