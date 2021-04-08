from django.core.management.base import BaseCommand
from rooms import (
    models as room_models,
)  # amenities를 바꿀거니까 그게 들어가있는 room의 models를 가져오는 것


class Command(BaseCommand):

    help = "This command creates amenities"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times",
    #         help="How many times do you wnat me to tell you that I love you",
    #     )

    # def handle(self, *args, **options):
    #     times = options.get(
    #         "times"
    #     )  # "times" 는 콘솔에서 python manage.py loveyou --times 50 했을때 50을 받아둔다. {'times' : '50'}
    #     for t in range(0, int(times)):
    #         self.stdout.write(self.style.SUCCESS("I love you"))  # 표준 output

    def handle(self, *args, **options):
        amenities = [
            "Air conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Bathtub",
            "Bed Linen",
            "Boating",
            "Cable TV",
            "Carbon monoxide detectors",
            "Chairs",
            "Children Area",
            "Coffee Maker in Room",
            "Cooking hob",
            "Cookware & Kitchen Utensils",
            "Dishwasher",
            "Double bed",
            "En suite bathroom",
            "Free Parking",
            "Free Wireless Internet",
            "Freezer",
            "Fridge / Freezer",
            "Golf",
            "Hair Dryer",
            "Heating",
            "Hot tub",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Outdoor Pool",
            "Outdoor Tennis",
            "Oven",
            "Queen size bed",
            "Restaurant",
            "Shopping Mall",
            "Shower",
            "Smoke detectors",
            "Sofa",
            "Stereo",
            "Swimming pool",
            "Toilet",
            "Towels",
            "TV",
        ]
        for a in amenities:
            room_models.Amenity.objects.create(
                name=a
            )  # amenities 어레이에서 하나씩 가져와서 오브젝트 생성하는 것
        self.stdout.write(self.style.SUCCESS(f"{len(amenities)} amenities created"))