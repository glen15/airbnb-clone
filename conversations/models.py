from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):

    """ Conversation Model Definition """

    participants = models.ManyToManyField(
        "users.User", related_name="conversation", blank=True
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():  # qurey set이 모든 users를 줄거야
            usernames.append(user.username)
        return " / ".join(
            usernames
        )  # join 메소드를 이용해서 리스트를 스트링으로만들었음. 앞에 붙는거는 항목사이에 들어가는것. 지금은 / 넣음

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = (
        "Number of Messages"  # admin.py 에 list display 에 나오는 이름 바꾸기
    )

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "Number of Participants"


class Message(core_models.TimeStampedModel):

    """ Message Model Definition """

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    Conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"
