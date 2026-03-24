from django.core.management.base import BaseCommand
from api.models import Category, MenuItem
from django.db import transaction

class Command(BaseCommand):
    help = 'Seeds the database with initial menu items'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Categories
        cat_data = [
            {'name': 'Combos', 'slug': 'combos'},
            {'name': 'Food', 'slug': 'food'},
            {'name': 'Snacks', 'slug': 'snacks'},
            {'name': 'Drinks', 'slug': 'beverages'},
            {'name': 'Essentials', 'slug': 'essentials'},
        ]

        categories = {}
        for c in cat_data:
            cat, created = Category.objects.get_or_create(slug=c['slug'], defaults={'name': c['name']})
            categories[c['slug']] = cat

        # Menu Items
        menu_data = [
            {
                'name': 'Ultimate Burger Combo',
                'description': 'Double cheese burger + Large fries + Coke',
                'price': 299.00,
                'category': categories['combos'],
                'image_url': 'https://images.unsplash.com/photo-1594212848116-e8d0337d11ce?auto=format&fit=crop&q=80&w=800',
                'is_veg': False,
                'rating': 4.8,
                'prep_time': 20,
                'is_featured': True
            },
            {
                'name': 'Veggie Supreme Pizza',
                'description': 'Loaded with mushrooms, olives, bell peppers and extra cheese',
                'price': 349.00,
                'category': categories['food'],
                'image_url': 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&q=80&w=800',
                'is_veg': True,
                'rating': 4.6,
                'prep_time': 25,
                'is_featured': True
            },
            {
                'name': 'Spicy Chicken Wings',
                'description': '6 pieces of hot wings with blue cheese dip',
                'price': 199.00,
                'category': categories['snacks'],
                'image_url': 'https://images.unsplash.com/photo-1569691899455-88464f6d3310?auto=format&fit=crop&q=80&w=800',
                'is_veg': False,
                'rating': 4.7,
                'prep_time': 15,
                'is_featured': False
            },
            {
                'name': 'Classic Cold Coffee',
                'description': 'Thick and creamy cold coffee with ice cream',
                'price': 149.00,
                'category': categories['beverages'],
                'image_url': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&q=80&w=800',
                'is_veg': True,
                'rating': 4.9,
                'prep_time': 10,
                'is_featured': True
            },
            {
                'name': 'Lays Magic Masala',
                'description': 'Big pack',
                'price': 40.00,
                'category': categories['essentials'],
                'image_url': 'https://www.bigbasket.com/media/uploads/p/l/104193_7-lays-potato-chips-magic-masala.jpg',
                'is_veg': True,
                'rating': 4.5,
                'prep_time': 5,
                'is_featured': False
            },
            {
                'name': 'Margherita Pizza Combo',
                'description': 'Classic margherita + Garlic Bread + Pepsi',
                'price': 249.00,
                'category': categories['combos'],
                'image_url': 'https://images.unsplash.com/photo-1573821663173-cbcebda47528?auto=format&fit=crop&q=80&w=800',
                'is_veg': True,
                'rating': 4.5,
                'prep_time': 20,
                'is_featured': False
            },
            {
                'name': 'Paneer Tikka Roll',
                'description': 'Soft paneer marinated in spices, wrapped in flaky paratha',
                'price': 129.00,
                'category': categories['food'],
                'image_url': 'https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&q=80&w=800',
                'is_veg': True,
                'rating': 4.4,
                'prep_time': 15,
                'is_featured': True
            },
            {
                'name': 'Dark Chocolate Shake',
                'description': 'Rich Belgian dark chocolate shake',
                'price': 169.00,
                'category': categories['beverages'],
                'image_url': 'https://images.unsplash.com/photo-1572490122747-3968b75bb827?auto=format&fit=crop&q=80&w=800',
                'is_veg': True,
                'rating': 4.8,
                'prep_time': 10,
                'is_featured': False
            }
        ]

        with transaction.atomic():
            for c in menu_data:
                MenuItem.objects.get_or_create(
                    name=c['name'],
                    defaults={
                        'description': c['description'],
                        'price': c['price'],
                        'category': c['category'],
                        'image_url': c['image_url'],
                        'is_veg': c['is_veg'],
                        'rating': c['rating'],
                        'prep_time': c['prep_time'],
                        'is_featured': c['is_featured']
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with beautiful realistic food data!'))
