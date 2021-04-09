from django.views.generic import ListView
from . import models


class HomeView(ListView):  # core폴더의 url에도 넣어뒀음

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10  # ListView 관련사항 ccv.co.uk확인하면 잘 정리되어있음
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"
