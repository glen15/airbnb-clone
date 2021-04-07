from django.db import models
from django_countries.fields import CountryField
from core import models as core_models  # import 이후 위에거랑 이름 같으니 as 로 명시해주는 것


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
        ordering = ["name"]  # 이름기준 기준으로 순서정리 - 문서에서 ordering 검색


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


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")  # 파일 업로드시 저장될 경로 지정
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )  # on_delete 삭제행동이 진행되는데 User가 삭제되면 연결된 room도 연쇄삭제(cascade)
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name  # list 에서 보일 이름을 룸 명으로 지정했던걸로 가져오는 것 / 기존에는 room_object_1 이런식

    # model에서 들어오는걸 덮어쓰기하는거! 이거 잘알아야겠음. 내가 원하는 형태로 변경 가능 - 사람들이 입력한걸 다 대문자로 바꾼다던지 - 통일화에 좋다
    def save(
        self, *args, **kwargs
    ):  # super()로 부모 속성에 접근하는 것 / 도시를 쓰고 save 했을때 그것을 받아서 새로운걸로 덮어쓸거야. super()에는 원래 입력한게 남겠지
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()
        return all_ratings / len(all_reviews)
