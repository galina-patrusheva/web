from django.utils import timezone
from datetime import datetime
from .models import History, GalleryUser


def site_menu(_):
    return {'menu': [('Главная', '/'),
                     ('Контакты', '/contacts'),
                     ('Галерея', '/gallery')]
            }


def last_seen(request):
    last_view = request.session.get('last-view')
    if last_view is not None:
        return {
            'last_view': timezone.make_aware(datetime.fromtimestamp(last_view))
        }
    return {}


def history(requset):
    try:
        user = GalleryUser.get_confirmed_user_by_id(
            requset.session.get('auth_user_id'))
    except GalleryUser.DoesNotExist:
        return {}
    event = History(datetime=timezone.now(),
                    user=user,
                    user_agent=requset.META.get('HTTP_USER_AGENT', 'None'),
                    query=requset.get_full_path(),
                    ip=requset.META.get('REMOTE_ADDR', 'None'))
    event.save()
    return {}
