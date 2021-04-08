import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command creates many rooms"

    def add_arguments(self, parser):  # 보통 몇번 반복할지를 정할때 add_arguments를 쓰면 좋은거같아
        parser.add_argument(
            "--number", default=2, type=int, help="how many users do you want to create"
        )  # type=int 안해주면 뒤에 쓰는 숫자를 str로 인식해서 안될거임

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "room_type": lambda x: random.choice(room_types),
                "host": lambda x: random.choice(all_users),
                "name": lambda x: seeder.faker.address(),  # faker 에 이미 만들어진 것을 활용
                "guests": lambda x: random.randint(1, 15),
                "price": lambda x: random.randint(1, 300),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} rooms created"))
