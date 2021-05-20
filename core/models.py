from django.db import models
from . import managers

""" componant 같이 쓸애들을 모아놓을 곳, 가상환경안에서 django-admin startapp core 로 만들었음"""


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)  # 모델 생성될때 날짜시간 자동 저장
    updated = models.DateTimeField(auto_now=True)  # 저장할때 날짜시간 자동저장
    objects = managers.CustomModelManager()  # manager를 모두에게 보내줄거야

    class Meta:
        abstract = True  # abstract model은 데이터베이스에 안들어가는 코드에서만 쓰이는 추상 모델
