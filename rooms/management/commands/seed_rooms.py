import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
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
        # 룸에 사진, amenity facility rules 램덤으로 등록하는 것
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        created_photos = seeder.execute()
        created_clean = flatten(
            list(created_photos.values())
        )  # 2중 리스트라서 flatten으로 안에꺼만 꺼내는 것
        for pk in created_clean:  # 생성된 룸에서 id(pk)로 불러들여서 i pk로넣는것
            room = room_models.Room.objects.get(pk=pk)  # 프라이머리 키(pk=id)로 그 룸을 찾고
            for i in range(3, random.randint(10, 17)):
                room_models.Photo.objects.create(  # 룸 모델에서 사진을 생성 하면서 캡션 룸이름 사진까지 만드는거
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",  # 사진파일 경로, 그중에서 1~31 랜덤에 파일 형식까지 지정
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:  # 나머지 0이면 추가되도록 (그냥 램덤성을 주기 위해서 한거지)
                    room.amenities.add(a)  # many to many 에서는 add를 활용해서 추가할것

            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)

            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created"))
