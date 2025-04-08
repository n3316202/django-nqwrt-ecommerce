from decimal import Decimal
from django.core.management.base import BaseCommand
from store.models import Category, Product
import random


class Command(BaseCommand):
    help = "Seed the database with sample Product data"

    def handle(self, *args, **options):
        categories = Category.objects.all()

        if not categories.exists():
            self.stdout.write(self.style.ERROR("❌ 먼저 카테고리를 등록하세요!"))
            return

        sample_names = [
            "양념 소불고기",
            "유기농 브로콜리",
            "레몬맛 탄산수",
            "허브 치킨",
            "프렌치 바게트",
        ]

        for name in sample_names:
            category = random.choice(categories)
            price = Decimal(random.randint(1000, 10000)) / 100
            is_sale = random.choice([True, False])
            sale_price = int(price * Decimal("0.8")) if is_sale else None

            product = Product.objects.create(
                name=name,
                price=price,
                description=f"{name} 상품 설명입니다.",
                category=category,
                is_sale=is_sale,
                sale_price=sale_price,
            )

            self.stdout.write(
                self.style.SUCCESS(f"✔ 생성됨: {product.name} ({category.name})")
            )
