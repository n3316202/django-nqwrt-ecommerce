from django.core.management.base import BaseCommand
from store.models import Category


class Command(BaseCommand):
    help = "Seed initial categories into the database"

    def handle(self, *args, **options):
        categories = ["전자제품", "패션", "도서", "가구", "장난감", "스포츠", "식품"]

        for name in categories:
            obj, created = Category.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Created category: {name}"))
            else:
                self.stdout.write(f"… Already exists: {name}")
