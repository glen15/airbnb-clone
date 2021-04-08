import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models


NAME = "lists"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help=f"how many {NAME} do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(users)}
        )
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[
                random.randint(0, 5) : random.randint(6, 15)
            ]  # room의 쿼리셋 받아와서 일정 부분만 슬라이스한거
            list_model.rooms.add(*to_add)  # * 없으면 어레이 그대로 가져올거야. 넣어서 안에 요소만 가져오는 것
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created"))
