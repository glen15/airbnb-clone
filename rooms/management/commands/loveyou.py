from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "This command tells me that she loves me"

    def add_arguments(self, parser):
        parser.add_argument(
            "--times",
            help="How many times do you wnat me to tell you that I love you",
        )

    def handle(self, *args, **options):
        times = options.get(
            "times"
        )  # "times" 는 콘솔에서 python manage.py loveyou --times 50 했을때 50을 받아둔다. {'times' : '50'}
        for t in range(0, int(times)):
            self.stdout.write(self.style.SUCCESS("I love you"))  # 표준 output
