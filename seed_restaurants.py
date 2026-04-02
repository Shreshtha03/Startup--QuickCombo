import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickcombo.settings')
django.setup()

from api.models import Restaurant, Category, MenuItem

def seed_restaurants():
    # ─── CATEGORIES ─────────────────────────────────────────────────────────────
    categories = {
        'beverages': Category.objects.get_or_create(slug='beverages', defaults={'name':'Beverages', 'icon':'🥤'})[0],
        'snacks': Category.objects.get_or_create(slug='snacks', defaults={'name':'Snacks', 'icon':'🍔'})[0],
        'desserts': Category.objects.get_or_create(slug='desserts', defaults={'name':'Desserts', 'icon':'🍨'})[0],
        'seafood': Category.objects.get_or_create(slug='seafood', defaults={'name':'Sea Food', 'icon':'🍤'})[0],
        'rice_pulao': Category.objects.get_or_create(slug='rice-pulao', defaults={'name':'Rice & Pulao', 'icon':'🍚'})[0],
        'noodles': Category.objects.get_or_create(slug='noodles', defaults={'name':'Noodles', 'icon':'🍜'})[0],
        'schezwan': Category.objects.get_or_create(slug='schezwan', defaults={'name':'Schezwan Specials', 'icon':'🔥'})[0],
    }

    # ─── RESTAURANTS ──────────────────────────────────────────────────────────
    disco, _ = Restaurant.objects.get_or_create(
        name="Disco Juice & Snacks",
        defaults={
            "rating": 4.6,
            "delivery_time": 15,
            "cuisines": "Juices, Shakes, Quick Bites, Snacks",
            "image_url": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&q=80&w=800",
            "is_featured": True
        }
    )

    chettinadu, _ = Restaurant.objects.get_or_create(
        name="Classic Chettinadu",
        defaults={
            "rating": 4.4,
            "delivery_time": 30,
            "cuisines": "South Indian, Sea Food, Biryani",
            "image_url": "https://images.unsplash.com/photo-1589187151003-0dd473a09492?auto=format&fit=crop&q=80&w=800",
            "is_featured": True
        }
    )

    # ─── DISCO MENU ITEMS (+25 Logic) ───────────────────────────────────────────
    disco_items = [
        # Milkshakes
        ("Rose Milkshake", 60, 'beverages'),
        ("Apple Shake", 80, 'beverages'),
        ("Fig Shake", 70, 'beverages'),
        ("Chikku Shake", 70, 'beverages'),
        ("Popoya Milkshake", 70, 'beverages'),
        ("Oreo Shake", 70, 'beverages'),
        ("Cold Coffee Shake", 60, 'beverages'),
        ("Cold Horlicks Shake", 60, 'beverages'),
        ("Cold Badam Shake", 60, 'beverages'),
        ("Cold Boost Shake", 60, 'beverages'),
        ("Choco Pie Shake", 80, 'beverages'),
        ("Bourbon Shake", 70, 'beverages'),
        ("Hide & Seek Shake", 80, 'beverages'),
        ("Dark Fantasy Shake", 100, 'beverages'),
        ("Kitkat Shake", 90, 'beverages'),
        ("Munch Shake", 80, 'beverages'),
        ("Snickers Shake", 90, 'beverages'),
        ("Fivestar Shake", 90, 'beverages'),
        ("Dairy Milkshake", 90, 'beverages'),
        ("Milkybar Shake", 80, 'beverages'),
        ("Pomegranate Shake", 90, 'beverages'),
        ("Mango Shake", 70, 'beverages'),
        ("Kiwi Shake", 90, 'beverages'),
        ("Strawberry Shake", 80, 'beverages'),
        ("Bounty Shake", 110, 'beverages'),
        ("Dry Fruit Shake", 100, 'beverages'),

        # Lassi
        ("Plain Lassi", 40, 'beverages'),
        ("Rose Lassi", 50, 'beverages'),
        ("Pista Lassi", 50, 'beverages'),
        ("Fruit Lassi", 50, 'beverages'),
        ("Dates Lassi", 60, 'beverages'),
        ("Mango Lassi", 50, 'beverages'),
        ("Grape Lassi", 50, 'beverages'),
        ("Vanilla Lassi", 50, 'beverages'),
        ("Chikku Lassi", 50, 'beverages'),
        ("Badam Lassi", 50, 'beverages'),
        ("Banana Lassi", 50, 'beverages'),
        ("Black Current Lassi", 50, 'beverages'),
        ("Blueberry Lassi", 50, 'beverages'),
        ("Chocolate Lassi", 50, 'beverages'),
        ("Pineapple Lassi", 50, 'beverages'),
        ("Strawberry Lassi", 50, 'beverages'),
        ("Dry Fruit Lassi", 70, 'beverages'),
        ("Butterscotch Lassi", 50, 'beverages'),

        # Mojitos
        ("Blue Mojito", 50, 'beverages'),
        ("Mint Mojito", 50, 'beverages'),
        ("Lichi Mojito", 50, 'beverages'),
        ("Orange Mojito", 50, 'beverages'),
        ("Mango Mojito", 50, 'beverages'),
        ("Virgin Mojito", 50, 'beverages'),
        ("Watermelon Mojito", 50, 'beverages'),
        ("Strawberry Mojito", 50, 'beverages'),
        ("Green Apple Mojito", 50, 'beverages'),
        ("Passion Fruit Mojito", 50, 'beverages'),
        ("Black Current Mojito", 50, 'beverages'),
        ("Blue Berry Mojito", 50, 'beverages'),

        # Combo Juices
        ("Summer Of", 70, 'beverages'),
        ("Ginger Cooler", 70, 'beverages'),
        ("Detox", 70, 'beverages'),
        ("Vitamin Boom", 70, 'beverages'),
        ("Pain Reduce", 70, 'beverages'),
        ("Power Booster", 70, 'beverages'),
        ("Super Active", 70, 'beverages'),
        ("Mango Surprise", 70, 'beverages'),
        ("Spice Orange", 70, 'beverages'),
        ("Melonade", 70, 'beverages'),
        ("Water Fall", 70, 'beverages'),
        ("Kwicooler", 70, 'beverages'),
        ("Skinglow", 70, 'beverages'),

        # Wraps
        ("Veg Wrap", 70, 'snacks'),
        ("Cheese Veg Wrap", 90, 'snacks'),
        ("Egg Wrap", 80, 'snacks'),
        ("Cheese Egg Wrap", 100, 'snacks'),
        ("Paneer Wrap", 80, 'snacks'),
        ("Chicken Nuggets Wrap", 100, 'snacks'),

        # Burgers
        ("Veg Burger", 70, 'snacks'),
        ("Veg Cheese Burger", 90, 'snacks'),
        ("Chicken Burger", 90, 'snacks'),
        ("Chicken Cheese Burger", 110, 'snacks'),

        # Momos
        ("Veg Momos (5pcs)", 60, 'snacks'),
        ("Chicken Momos (5pcs)", 70, 'snacks'),
        ("Paneer Momos (5pcs)", 90, 'snacks'),

        # Maggie
        ("Plain Maggie", 40, 'snacks'),
        ("Veg Maggie", 60, 'snacks'),
        ("Egg Maggie", 70, 'snacks'),
        ("Chicken Maggie", 90, 'snacks'),
    ]

    # ─── CLASSIC CHETTINADU MENU ITEMS ──────────────────────────────────────────
    chettinadu_items = [
        # Sea Food
        ("Prawn Chettinad", 195, 'seafood'),
        ("Kadai Prawn", 195, 'seafood'),
        ("Prawn Pepper Masala", 195, 'seafood'),
        ("Malabar Fish Curry", 185, 'seafood'),
        ("Prawn Masala", 195, 'seafood'),
        ("Fish Masala", 195, 'seafood'),
        ("Fish Chettinad", 185, 'seafood'),
        ("Kadai Fish", 195, 'seafood'),

        # Rice & Pulao
        ("Steam Rice", 85, 'rice_pulao'),
        ("Peas Pulao", 135, 'rice_pulao'),
        ("Mushroom Pulao", 115, 'rice_pulao'),
        ("Paneer Pulao", 115, 'rice_pulao'),
        ("Gobi Pulao", 125, 'rice_pulao'),
        ("Cashew Nut Pulao", 115, 'rice_pulao'),
        ("Veg Pulao", 105, 'rice_pulao'),
        ("Jeera Rice", 135, 'rice_pulao'),
        ("Ghee Rice", 115, 'rice_pulao'),

        # Regular Rice/Noodles
        ("Egg Rice", 115, 'rice_pulao'),
        ("Egg Noodles", 115, 'noodles'),
        ("Chicken Rice", 115, 'rice_pulao'),
        ("Chicken Noodles", 115, 'noodles'),
        ("Veg Rice", 115, 'rice_pulao'),
        ("Veg Noodles", 115, 'noodles'),
        ("Mushroom Rice", 125, 'rice_pulao'),
        ("Paneer Rice", 135, 'rice_pulao'),
        ("Prawn Rice", 195, 'rice_pulao'),
        ("Mutton Rice", 185, 'rice_pulao'),

        # Schezwan Specials
        ("Sz Prawn Rice", 135, 'schezwan'),
        ("Sz Prawn Noodles", 135, 'schezwan'),
        ("Shanghai Chicken Rice", 115, 'schezwan'),
        ("Sz Paneer Rice", 135, 'schezwan'),
        ("Sz Chicken Rice", 135, 'schezwan'),
        ("Sz Mixed Noodles", 125, 'schezwan'),
    ]

    # Clear existing items for these restaurants
    MenuItem.objects.filter(restaurant__in=[disco, chettinadu]).delete()

    # Seed Disco Items (+25)
    for name, price, cat_key in disco_items:
        MenuItem.objects.create(
            restaurant=disco,
            category=categories[cat_key],
            name=name,
            price=price + 25,  # Adding ₹25 markup
            is_veg=not any(kw in name.lower() for kw in ['chicken', 'egg', 'mutton', 'fish', 'prawn']),
            is_available=True,
            rating=4.5,
            prep_time=15
        )

    # Seed Chettinadu Items
    for name, price, cat_key in chettinadu_items:
        MenuItem.objects.create(
            restaurant=chettinadu,
            category=categories[cat_key],
            name=name,
            price=price,
            is_veg=not any(kw in name.lower() for kw in ['chicken', 'egg', 'mutton', 'fish', 'prawn']),
            is_available=True,
            rating=4.4,
            prep_time=25
        )

    print(f"✅ Successfully seeded {len(disco_items)} items for Disco Juice & Snacks (+₹25 markup)")
    print(f"✅ Successfully seeded {len(chettinadu_items)} items for Classic Chettinadu")

if __name__ == "__main__":
    seed_restaurants()
