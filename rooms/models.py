from django.db import models
from django_countries.fields import CountryField
from core import models as core_models  # import 이후 위에거랑 이름 같으니 as 로 명시해주는 것
from users import (
    models as user_models,
)  # host에 필요한 user 정보를 ForeignKey에 연결하기 위해서 import


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    discription = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    pircie = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    isntant_book = models.BooleanField(default=False)
    host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)