from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as users_models


class Command(BaseCommand):

    help = "This command creates many users"

    def add_arguments(self, parser):  # 보통 몇번 반복할지를 정할때 add_arguments를 쓰면 좋은거같아
        parser.add_argument(
            "--number", default=2, type=int, help="how many users do you want to create"
        )  # type=int 안해주면 뒤에 쓰는 숫자를 str로 인식해서 안될거임

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(
            users_models.User, number, {"is_staff": False, "is_superuser": False}
        )  # 스태프랑 슈퍼유저 빼고 생성하도록하는 것
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} users created"))
