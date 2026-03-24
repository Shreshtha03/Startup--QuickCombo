import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Quickcombo.settings")
django.setup()

from api.models import Restaurant

def cleanup():
    allowed_terms = ["classic", "disco", "chettinadu", "chettinad"]
    deleted_count = 0
    for r in Restaurant.objects.all():
        name_lower = r.name.lower()
        if not any(term in name_lower for term in allowed_terms):
            print(f"Deleting leftover restaurant: {r.name}")
            r.delete()
            deleted_count += 1
            
    print(f"✅ Cleanup Complete. Deleted {deleted_count} dummy restaurants.")
    print("Remaining Authentic Restaurants:")
    for r in Restaurant.objects.all():
        print(f"- {r.name}")

if __name__ == "__main__":
    cleanup()
