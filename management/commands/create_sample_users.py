from django.core.management.base import BaseCommand, CommandError
from mirumee_webapp.models import User


class Command(BaseCommand):
    help = 'Creates three sample users: sample_user_1, sample_user_2 ... with passwords 1, 2 and 3, without a favorite' \
           'rocket core.'

    def handle(self, *args, **options):
        for i in range(0,3):
            user = User.objects.create_user(f'sample_user_{i}', password=f'{i}')
            user.save()
