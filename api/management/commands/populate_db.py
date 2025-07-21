import random
from decimal import Decimal
from faker import Faker

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import User, Product, Order, OrderItem


class Command(BaseCommand):
    help = 'Creates more realistic application data'

    def handle(self, *args, **kwargs):
        # get or create superuser
        user = User.objects.filter(username='admin').first()
        if not user:
            user = User.objects.create_superuser(
                username='admin', password='test')

        # Clean up existing data to avoid duplicates on re-run
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()

        self.stdout.write("Cleared existing data...")

        fake = Faker()

        # create products
        products = []
        self.stdout.write("Creating products...")
        for _ in range(50):  # Create 50 products
            products.append(
                Product(
                    name=fake.company() + " " + fake.bs(),
                    description=fake.text(),
                    price=Decimal(random.randrange(100, 10000)) / 100,
                    stock=random.randint(0, 100)
                )
            )

        Product.objects.bulk_create(products)
        products = Product.objects.all()
        self.stdout.write(f"Created {len(products)} products.")

        # create some dummy orders tied to the superuser
        self.stdout.write("Creating orders...")
        for _ in range(15):
            # create an Order with a random number of items (1 to 5)
            order = Order.objects.create(user=user)
            num_items = random.randint(1, 5)
            # Ensure we don't try to sample more products than exist
            sample_size = min(num_items, len(products))
            for product in random.sample(list(products), sample_size):
                OrderItem.objects.create(
                    order=order, product=product, quantity=random.randint(1, 5)
                )

        self.stdout.write(self.style.SUCCESS(
            'Successfully populated the database with realistic data.'))
