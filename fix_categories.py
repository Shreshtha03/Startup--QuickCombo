import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Quickcombo.settings')
django.setup()

from api.models import Category, MenuItem

def fix_categories():
    food_cat, _ = Category.objects.get_or_create(name='Food', slug='food', defaults={'icon':'🍔'})
    bev_cat, _ = Category.objects.get_or_create(name='Beverages', slug='beverages', defaults={'icon':'🥤'})
    snack_cat, _ = Category.objects.get_or_create(name='Snacks', slug='snacks', defaults={'icon':'🍿'})

    all_items = MenuItem.objects.all()
    
    drink_keywords = [
        'shake', 'lassi', 'mojito', 'cooler', 'tea', 'coffee', 'milk', 'boost', 
        'horlicks', 'bournvita', 'juice', 'water', 'melonade', 'detox', 'boom', 
        'reduce', 'active', 'surprise', 'orange', 'skinglow', 'beverage', 'badam'
    ]

    for item in all_items:
        name_lower = item.name.lower()
        rest_name_lower = item.restaurant.name.lower()
        
        # Priority 1: All drinks go to Beverages regardless of restaurant
        if any(kw in name_lower for kw in drink_keywords):
            item.category = bev_cat
        else:
            # Priority 2: Disco items are Snacks, Chettinadu are Food
            if 'disco' in rest_name_lower:
                item.category = snack_cat
            else:
                item.category = food_cat
        
        item.save()

    print("✅ Successfully re-mapped categories: Chettinad -> Food, Disco -> Snacks, Drinks -> Beverages")

if __name__ == "__main__":
    fix_categories()
