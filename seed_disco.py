import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Quickcombo.settings')
django.setup()

from api.models import Restaurant, Category, MenuItem

def seed_disco():
    cat_shakes, _ = Category.objects.get_or_create(name='Beverages', slug='beverages', defaults={'icon':'🥤'})
    cat_food, _ = Category.objects.get_or_create(name='Snacks', slug='snacks', defaults={'icon':'🍔'})
    cat_desserts, _ = Category.objects.get_or_create(name='Desserts', slug='desserts', defaults={'icon':'🍨'})

    restaurant, _ = Restaurant.objects.get_or_create(
        name="Disco Juice & Snacks",
        defaults={
            "rating": 4.6,
            "delivery_time": 15,
            "cuisines": "Juices, Shakes, Quick Bites, Snacks",
            "image_url": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&q=80&w=800",
            "is_featured": True
        }
    )

    items_to_create = [
        # MILKSHAKES
        ("Milkshake - Rose", 60, cat_shakes),
        ("Milkshake - Apple", 80, cat_shakes),
        ("Milkshake - Chikku", 70, cat_shakes),
        ("Milkshake - Papaya", 70, cat_shakes),
        ("Milkshake - Oreo", 70, cat_shakes),
        ("Cold Coffee", 60, cat_shakes),
        ("Cold Horlicks", 60, cat_shakes),
        ("Cold Badam", 60, cat_shakes),
        ("Cold Boost", 60, cat_shakes),
        ("Milkshake - Choco Pie", 80, cat_shakes),
        ("Milkshake - Bourbon", 70, cat_shakes),
        ("Milkshake - Hide & Seek", 80, cat_shakes),
        ("Milkshake - Dark Fantasy", 100, cat_shakes),
        ("Milkshake - Kitkat", 90, cat_shakes),
        ("Milkshake - Munch", 80, cat_shakes),
        ("Milkshake - Snickers", 90, cat_shakes),
        ("Milkshake - Fivestar", 90, cat_shakes),
        ("Milkshake - Dairy Milk", 90, cat_shakes),
        ("Milkshake - Pomegranate", 80, cat_shakes),
        ("Milkshake - Mango", 70, cat_shakes),
        ("Milkshake - Kiwi", 90, cat_shakes),
        ("Milkshake - Strawberry", 80, cat_shakes),
        ("Milkshake - Bounty", 110, cat_shakes),
        ("Milkshake - Dry Fruit", 100, cat_shakes),
        ("Milkshake - Chocolate", 90, cat_shakes),
        ("Milkshake - Banana Dates", 90, cat_shakes),

        # ICE CREAM SHAKE
        ("Ice Cream Shake - Mango", 90, cat_shakes),
        ("Ice Cream Shake - Black Current", 90, cat_shakes),
        ("Ice Cream Shake - Strawberry", 90, cat_shakes),
        ("Ice Cream Shake - Butter Scotch", 90, cat_shakes),
        ("Ice Cream Shake - Vanilla", 90, cat_shakes),
        ("Ice Cream Shake - Pista", 90, cat_shakes),
        ("Ice Cream Shake - Chocolate", 90, cat_shakes),

        # LASSI
        ("Lassi - Plain", 40, cat_shakes),
        ("Lassi - Rose", 50, cat_shakes),
        ("Lassi - Pista", 50, cat_shakes),
        ("Lassi - Fruit", 50, cat_shakes),
        ("Lassi - Mango", 50, cat_shakes),
        ("Lassi - Grape", 50, cat_shakes),
        ("Lassi - Vanilla", 50, cat_shakes),
        ("Lassi - Chikku", 50, cat_shakes),
        ("Lassi - Badam", 50, cat_shakes),
        ("Lassi - Banana", 50, cat_shakes),
        ("Lassi - Black Current", 50, cat_shakes),
        ("Lassi - Blueberry", 50, cat_shakes),
        ("Lassi - Chocolate", 50, cat_shakes),
        ("Lassi - Pineapple", 50, cat_shakes),
        ("Lassi - Strawberry", 50, cat_shakes),
        ("Lassi - Dry Fruit", 70, cat_shakes),
        ("Lassi - Butterscotch", 50, cat_shakes),

        # MOJITO
        ("Mojito - Blue", 50, cat_shakes),
        ("Mojito - Mint", 50, cat_shakes),
        ("Mojito - Lichi", 50, cat_shakes),
        ("Mojito - Orange", 50, cat_shakes),
        ("Mojito - Mango", 50, cat_shakes),
        ("Mojito - Virgin", 50, cat_shakes),
        ("Mojito - Watermelon", 50, cat_shakes),
        ("Mojito - Strawberry", 50, cat_shakes),
        ("Mojito - Green Apple", 50, cat_shakes),
        ("Mojito - Passion Fruit", 50, cat_shakes),
        ("Mojito - Black Current", 50, cat_shakes),
        ("Mojito - Blue Berry", 50, cat_shakes),
        
        # TENDER COCONUT SHAKE
        ("Tender Coconut Shake", 90, cat_shakes),
        ("Tender Coconut Shake with Icecream", 110, cat_shakes),
        
        # ICE CREAM SCOOP
        ("Ice Cream (2 Scoops) - Vanilla", 50, cat_desserts),
        ("Ice Cream (2 Scoops) - Strawberry", 50, cat_desserts),
        ("Ice Cream (2 Scoops) - Butter Scotch", 50, cat_desserts),
        ("Ice Cream (2 Scoops) - Chocolate", 50, cat_desserts),
        ("Ice Cream (2 Scoops) - Mango", 50, cat_desserts),
        ("Ice Cream (2 Scoops) - Pista", 50, cat_desserts),
        ("Ice Cream (2 Scoops) - Black Current", 50, cat_desserts),
        ("Ice Cream (2 Scoops) - Mixed", 70, cat_desserts),

        # FRUIT SALAD
        ("Fruit Salad", 80, cat_desserts),
        ("Fruit Salad with Ice Cream", 100, cat_desserts),
        ("Special Fruit Salad", 100, cat_desserts),
        ("Special Fruit with Ice cream", 120, cat_desserts),

        # COMBO JUICE
        ("Combo Juice - Summer Of", 70, cat_shakes),
        ("Combo Juice - Ginger Cooler", 70, cat_shakes),
        ("Combo Juice - Detox", 70, cat_shakes),
        ("Combo Juice - Vitamin Boom", 70, cat_shakes),
        ("Combo Juice - Pain Reduce", 70, cat_shakes),
        ("Combo Juice - Power Booster", 70, cat_shakes),
        ("Combo Juice - Super Active", 70, cat_shakes),
        ("Combo Juice - Mango Surprise", 70, cat_shakes),
        ("Combo Juice - Spice Orange", 70, cat_shakes),
        ("Combo Juice - Melonade", 70, cat_shakes),
        ("Combo Juice - Water Fall", 70, cat_shakes),
        ("Combo Juice - Kwicooler", 70, cat_shakes),
        ("Combo Juice - Skinglow", 70, cat_shakes),

        # HOT BEVERAGE
        ("Hot Tea", 12, cat_shakes),
        ("Black Tea", 12, cat_shakes),
        ("Special Tea", 15, cat_shakes),
        ("Black Coffee", 15, cat_shakes),
        ("Filter Coffee", 15, cat_shakes),
        ("Lemon Tea", 15, cat_shakes),
        ("Green Tea", 15, cat_shakes),
        ("Hot Milk", 15, cat_shakes),
        ("Sukku Coffee", 20, cat_shakes),
        ("Badham Milk", 20, cat_shakes),
        ("Ragi Malt", 20, cat_shakes),
        ("Boost", 20, cat_shakes),
        ("Horlicks", 20, cat_shakes),
        ("Bournvita", 25, cat_shakes),

        # WRAP
        ("Wrap - Egg", 80, cat_food),
        ("Wrap - Cheese Egg", 100, cat_food),
        ("Wrap - Veg", 70, cat_food),
        ("Wrap - Cheese Veg", 90, cat_food),
        ("Wrap - Paneer", 80, cat_food),
        ("Wrap - Cheese Paneer", 100, cat_food),
        ("Wrap - Mushroom", 80, cat_food),
        ("Wrap - Cheese Mushroom", 100, cat_food),
        ("Wrap - Sweetcorn", 80, cat_food),
        ("Wrap - Cheese Sweetcorn", 100, cat_food),
        ("Wrap - Chicken Nuggets", 100, cat_food),

        # BURGER VEG
        ("Burger - Veg", 70, cat_food),
        ("Burger - Veg Cheese", 90, cat_food),
        ("Burger - Veg Nuggets", 100, cat_food),
        ("Burger - Veg Nuggets Cheese", 120, cat_food),
        ("Burger - Veg Double Patty", 120, cat_food),
        ("Burger - Veg Double Patty Cheese", 140, cat_food),

        # BURGER NON-VEG
        ("Burger - Egg", 80, cat_food),
        ("Burger - Egg Cheese", 100, cat_food),
        ("Burger - Chicken", 90, cat_food),
        ("Burger - Chicken Cheese", 110, cat_food),
        ("Burger - Chicken Nuggets", 110, cat_food),
        ("Burger - Chicken Nuggets Cheese", 130, cat_food),
        ("Burger - Chicken Double Patty", 130, cat_food),
        ("Burger - Chicken Double Patty Cheese", 150, cat_food),

        # NUGGET
        ("Chicken Nugget (6pcs)", 90, cat_food),
        ("Veg Nugget (7pcs)", 80, cat_food),

        # CUTLET
        ("Veg Cutlet (2pcs)", 40, cat_food),
        ("Chicken Cutlet (2pcs)", 50, cat_food),

        # ROLL
        ("Veg Roll", 40, cat_food),
        ("Paneer Roll", 50, cat_food),
        ("Chicken Roll", 60, cat_food),

        # FRENCH FRIES
        ("Peri Peri French Fries", 100, cat_food),
        ("Classic French Fries", 80, cat_food),
        ("Masala French Fries", 90, cat_food),
        ("Chicken Cheese Ball", 90, cat_food),
        ("Chicken Popcorn", 100, cat_food),
        ("Cheese French Fries", 130, cat_food),

        # GRILL SANDWICH
        ("Grill Sandwich - Sweetcorn", 60, cat_food),
        ("Grill Sandwich - Veg", 60, cat_food),
        ("Grill Sandwich - Paneer", 80, cat_food),
        ("Grill Sandwich - Mushroom", 80, cat_food),
        ("Grill Sandwich - Egg", 70, cat_food),
        ("Grill Sandwich - Chicken", 90, cat_food),
        ("Chilly Sandwich Cheese", 60, cat_food),
        ("Cheese Toast", 40, cat_food),

        # MOMOS
        ("Momos - Veg (5pcs)", 60, cat_food),
        ("Momos - Paneer (5pcs)", 90, cat_food),
        ("Momos - Chicken (5pcs)", 70, cat_food),
        ("Momos - Chicken Peri Peri (5pcs)", 90, cat_food),
        ("Momos - Chicken Cheese (5pcs)", 90, cat_food),

        # MAGGIE
        ("Maggie - Plain", 40, cat_food),
        ("Maggie - Veg", 60, cat_food),
        ("Maggie - Masala", 70, cat_food),
        ("Maggie - Paneer", 90, cat_food),
        ("Maggie - Mushroom", 80, cat_food),
        ("Maggie - Egg", 70, cat_food),
        ("Maggie - Chicken", 90, cat_food),

        # CHAPATHI & PAROTTA ROLL
        ("Paneer Chapathi Roll", 70, cat_food),
        ("Paneer Parotta Roll", 80, cat_food),
        ("Chicken Chapathi Roll", 70, cat_food),
        ("Chicken Parotta Roll", 100, cat_food),
    ]

    MenuItem.objects.filter(restaurant=restaurant).delete()
    for name, price, cat in items_to_create:
        MenuItem.objects.create(
            restaurant=restaurant,
            category=cat,
            name=name,
            price=price + 25,
            is_veg=not ("Chicken" in name or "Egg" in name),
            is_available=True,
            rating=4.5,
            prep_time=15
        )

    print("✅ Disco Juice & Snacks Menu Seeded Completely")

if __name__ == "__main__":
    seed_disco()
