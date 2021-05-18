import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()

# 위에 두개 필수, 폴더명도 반드시 templatetags로 해야함


@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return
    try:
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        reservation_models.BookedDay.objects.get(day=date, reservation__room=room)
        return True
    except reservation_models.BookedDay.DoesNotExist:
        return False