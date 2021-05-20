from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.room}"

    def rating_average(self):
        avg = (
            self.accuracy
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
            + self.communication
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "Avg."

    # model이 list에 있을때 정렬 순서를 정해주기 위해서
    # 리뷰 새 작성글이 밑에 들어가는게 아니라 위로 쌓이도록 순서 변경
    class Meta:
        ordering = ("-created",)  # - 붙여서 역방향으로 했음
