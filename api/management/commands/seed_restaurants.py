from django.core.management.base import BaseCommand
from api.models import Restaurant
from django.db import transaction

class Command(BaseCommand):
    help = 'Seeds the database with premium restaurants'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding restaurants...')

        restaurants_data = [
            {
                'name': 'The Burger Club',
                'rating': 4.8,
                'delivery_time': 25,
                'cuisines': 'American, Burgers, Fast Food',
                'image_url': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800&q=80',
                'is_featured': True
            },
            {
                'name': 'Spice Roots',
                'rating': 4.6,
                'delivery_time': 40,
                'cuisines': 'North Indian, Mughlai',
                'image_url': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800&q=80',
                'is_featured': True
            },
            {
                'name': 'Piazza Pizza',
                'rating': 4.5,
                'delivery_time': 35,
                'cuisines': 'Italian, Pizza, Fast Food',
                'image_url': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=800&q=80',
                'is_featured': False
            },
            {
                'name': 'Dragon Chopstix',
                'rating': 4.3,
                'delivery_time': 30,
                'cuisines': 'Chinese, Asian',
                'image_url': 'https://images.unsplash.com/photo-1525755662778-989d0524087e?w=800&q=80',
                'is_featured': False
            },
            {
                'name': 'Biryani Blues',
                'rating': 4.7,
                'delivery_time': 45,
                'cuisines': 'Hyderabadi, Biryani, Curries',
                'image_url': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&q=80',
                'is_featured': True
            },
            {
                'name': 'Healthy Bites',
                'rating': 4.9,
                'delivery_time': 20,
                'cuisines': 'Salads, Healthy Food, Smoothies',
                'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&q=80',
                'is_featured': False
            }
        ]

        with transaction.atomic():
            for r in restaurants_data:
                Restaurant.objects.get_or_create(
                    name=r['name'],
                    defaults={
                        'rating': r['rating'],
                        'delivery_time': r['delivery_time'],
                        'cuisines': r['cuisines'],
                        'image_url': r['image_url'],
                        'is_featured': r['is_featured']
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with premium restaurants!'))
