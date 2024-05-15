from django.contrib.auth.models import User
from django.utils import timezone
from django.core.management.base import BaseCommand
from faker import Faker
from app.models import Job, Account
from random import randint

fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with fake data'

    def add_arguments(self, parser):
        parser.add_argument('--number', type=int, help='The number of fake users to create')

    def handle(self, *args, **options):
        number = options['number']
        if number is None:
            number = 8
        for i in range(number):
            user = User.objects.create_user(username=fake.user_name(), email=fake.email(), password='password')
            account = Account.objects.create(user=user, name=fake.name(), translator=False, balance=fake.random_int(min=300, max=1000))
            for j in range(10):
                job = Job.objects.create(
                    user = user,
                    title = fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                    description =fake.text(max_nb_chars=300, ext_word_list=None),
                    source_lang ='English',
                    target_lang =fake.random_element(elements=("Spanish", "French", "German", "Croatian")),
                    field=fake.random_element(elements=('Art', 'Business', 'Computers', 'Education', 'Engineering', 'Finance', 'Law', 'Literature', 'Medicine', 'Science', 'Social Sciences', 'Technology')),
                    budget=fake.random_int(min=1, max=300),
                    text=fake.text(max_nb_chars=1000, ext_word_list=None),
                    status='available',
                )
                job.save()
            self.stdout.write(self.style.SUCCESS(f'{number} fake users created!'))
