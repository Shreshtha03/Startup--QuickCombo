from django.core.management.base import BaseCommand
from api.models import Category, MenuItem, Restaurant
from django.db import transaction
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds the database with Classic Chettinadu restaurant and its menu'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Classic Chettinadu data...')

        # 1. Create/Get Restaurant
        rest, created = Restaurant.objects.get_or_create(
            name='Classic Chettinadu',
            defaults={
                'rating': 4.6,
                'delivery_time': 35,
                'cuisines': 'Chettinad, South Indian, Biryani',
                'image_url': 'https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=800&q=80',
                'is_featured': True
            }
        )

        # Clear existing items ONLY for this restaurant
        MenuItem.objects.filter(restaurant=rest).delete()

        # 2. Categories
        cats_to_create = [
            {'name': 'Starters (Non-Veg)', 'icon': '🍗'},
            {'name': 'Kebabs & Tandoori', 'icon': '🍢'},
            {'name': 'Chicken Specials', 'icon': '🍗'},
            {'name': 'Non-Veg Biryani', 'icon': '🍗'},
            {'name': 'Veg Biryani', 'icon': '🍚'},
            {'name': 'Others', 'icon': '🍚'},
        ]
        
        categories = {}
        for ct in cats_to_create:
            slug = slugify(ct['name'])
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': ct['name'], 'icon': ct['icon']})
            categories[slug] = cat

        # 3. Menu Items
        menu_data = [
            # Starters (Non-Veg)
            {'name': 'Fish 65', 'price': 195, 'cat': 'starters-non-veg', 'is_veg': False},
            {'name': 'Andhra Chicken 65', 'price': 185, 'cat': 'starters-non-veg', 'is_veg': False},
            {'name': 'Prawn 65', 'price': 185, 'cat': 'starters-non-veg', 'is_veg': False},
            {'name': 'Chicken Drumstick (5 pcs)', 'price': 155, 'cat': 'starters-non-veg', 'is_veg': False},
            {'name': 'Chicken 65 Boneless (6 pcs)', 'price': 165, 'cat': 'starters-non-veg', 'is_veg': False},
            {'name': 'Chicken 65 Bone (6 pcs)', 'price': 155, 'cat': 'starters-non-veg', 'is_veg': False},
            {'name': 'Chicken Lollipop (5 pcs)', 'price': 165, 'cat': 'starters-non-veg', 'is_veg': False},

            # Kebabs & Tandoori
            {'name': 'Hariyali Kabab', 'price': 145, 'cat': 'kebabs-tandoori', 'is_veg': False},
            {'name': 'Paneer Tikka', 'price': 185, 'cat': 'kebabs-tandoori', 'is_veg': True},
            {'name': 'Fish Tikka', 'price': 185, 'cat': 'kebabs-tandoori', 'is_veg': False},
            {'name': 'Reshmi Kabab (6 pcs)', 'price': 175, 'cat': 'kebabs-tandoori', 'is_veg': False},
            {'name': 'Malai Kabab (6 pcs)', 'price': 205, 'cat': 'kebabs-tandoori', 'is_veg': False},
            {'name': 'Chicken Tikka (6 pcs)', 'price': 185, 'cat': 'kebabs-tandoori', 'is_veg': False},
            {'name': 'Badami Kabab', 'price': 175, 'cat': 'kebabs-tandoori', 'is_veg': False},
            {'name': 'Lasooni Kabab', 'price': 165, 'cat': 'kebabs-tandoori', 'is_veg': False},
            {'name': 'Tangdi Kabab (2 pcs)', 'price': 175, 'cat': 'kebabs-tandoori', 'is_veg': False},

            # Chicken Specials
            {'name': 'Afghani Chicken Full', 'price': 425, 'cat': 'chicken-specials', 'is_veg': False},
            {'name': 'Afghani Chicken Half', 'price': 205, 'cat': 'chicken-specials', 'is_veg': False},
            {'name': 'Tandoori Chicken Full', 'price': 445, 'cat': 'chicken-specials', 'is_veg': False},
            {'name': 'Tandoori Chicken Half', 'price': 225, 'cat': 'chicken-specials', 'is_veg': False},
            {'name': 'Tandoori Chicken Quarter', 'price': 135, 'cat': 'chicken-specials', 'is_veg': False},

            # Non-Veg Biryani
            {'name': 'Chicken Biryani', 'price': 165, 'cat': 'non-veg-biryani', 'is_veg': False},
            {'name': 'Mogal Chicken Biryani', 'price': 175, 'cat': 'non-veg-biryani', 'is_veg': False},
            {'name': 'Chicken Tikka Biryani', 'price': 155, 'cat': 'non-veg-biryani', 'is_veg': False},
            {'name': 'Chilli Chicken Biryani', 'price': 125, 'cat': 'non-veg-biryani', 'is_veg': False},
            {'name': 'Chicken 65 Biryani', 'price': 165, 'cat': 'non-veg-biryani', 'is_veg': False},
            {'name': 'Chicken Hyderabadi Biryani', 'price': 125, 'cat': 'non-veg-biryani', 'is_veg': False},
            {'name': 'Chettinadu Special Chicken Biryani', 'price': 165, 'cat': 'non-veg-biryani', 'is_veg': False},
            {'name': 'Egg Biryani', 'price': 135, 'cat': 'non-veg-biryani', 'is_veg': False},
            {'name': 'Tandoori Chicken Biryani', 'price': 155, 'cat': 'non-veg-biryani', 'is_veg': False},
            {'name': 'Mutton Biryani', 'price': 245, 'cat': 'non-veg-biryani', 'is_veg': False},
            {'name': 'Fish Biryani', 'price': 205, 'cat': 'non-veg-biryani', 'is_veg': False},
            {'name': 'Prawn Biryani', 'price': 235, 'cat': 'non-veg-biryani', 'is_veg': False},

            # Veg Biryani
            {'name': 'Veg Biryani', 'price': 145, 'cat': 'veg-biryani', 'is_veg': True},
            {'name': 'Paneer Biryani', 'price': 205, 'cat': 'veg-biryani', 'is_veg': True},
            {'name': 'Mushroom Biryani', 'price': 175, 'cat': 'veg-biryani', 'is_veg': True},

            # Others
            {'name': 'Plain Biryani', 'price': 105, 'cat': 'others', 'is_veg': True, 'desc': 'classic chettinadu restraunt'},
        ]

        img_base = "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&q=80" # Placeholder
        
        for item in menu_data:
            MenuItem.objects.create(
                restaurant=rest,
                category=categories[item['cat']],
                name=item['name'],
                price=item['price'],
                is_veg=item['is_veg'],
                description=item.get('desc', ''),
                image_url=img_base,
                prep_time=25,
                rating=4.4
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded Classic Chettinadu!'))
