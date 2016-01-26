import io
from PIL import Image, ImageDraw
from datetime import timedelta
from django.utils import timezone
from .models import Visit, Counter


VISIT_TIME_DELTA = timedelta(minutes=30)


def make_graphic_counter(counter):
    # create png-image with views/visits
    buffer = io.BytesIO()
    image = Image.new('RGBA', (120, 40))
    draw = ImageDraw.Draw(image)
    text_color = 'white'
    draw.text((0, 12), 'visits')
    draw.text((0, 23), 'views')
    draw.text((40, 0), 'today')
    draw.text((40, 12), '{}'.format(counter.today_visits), fill=text_color)
    draw.text((40, 23), '{}'.format(counter.today_views), fill=text_color)
    draw.text((80, 0), 'total')
    draw.text((80, 12), '{}'.format(counter.total_visits), fill=text_color)
    draw.text((80, 23), '{}'.format(counter.total_views), fill=text_color)
    image.save(buffer, 'PNG')
    buffer.seek(0)
    return buffer.read()


# Counter
def handle_views(request):
    ip = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT')
    resolution = request.POST.get('resolution')
    now = timezone.now()
    accept_period_timestamp = (now - VISIT_TIME_DELTA).timestamp()
    last_view_timestamp = request.session.get('last-view')
    request.session['last-view'] = now.timestamp()
    if last_view_timestamp is not None:
        if accept_period_timestamp > last_view_timestamp:
            Visit.add_visit(ip, user_agent, resolution)
    else:
        last_visit_from_ip = Visit.get_last_by_ip(ip)
        if last_visit_from_ip is None:
            Visit.add_visit(ip, user_agent, resolution)
        else:
            last_visit_timestamp = last_visit_from_ip.datetime.timestamp()
            if accept_period_timestamp > last_visit_timestamp:
                Visit.add_visit(ip, user_agent, resolution)
    Counter.inc_counter()
    return {}
