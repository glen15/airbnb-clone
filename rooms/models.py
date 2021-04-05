from django.db import models
from django_countries.fields import CountryField
from core import models as core_models  # import 이후 위에거랑 이름 같으니 as 로 명시해주는 것
from users import (
    models as user_models,
)  # host에 필요한 user 정보를 ForeignKey에 연결하기 위해서 import


class AbstractItem(core_models.TimeStampedModel):

    """ Absotract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """RoomType Model Definition"""

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):

    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


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
    host = models.ForeignKey(
        user_models.User, on_delete=models.CASCADE
    )  # on_delete 삭제행동이 진행되는데 User가 삭제되면 연결된 room도 연쇄삭제(cascade)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity)
    facilities = models.ManyToManyField(Facility)
    house_rules = models.ManyToManyField(HouseRule)

    def __str__(self):
        return self.name  # list 에서 보일 이름을 룸 명으로 지정했던걸로 가져오는 것 / 기존에는 room_object_1 이런식
