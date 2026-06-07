import os
import django
import cloudinary
import cloudinary.uploader
from django.conf import settings

# ===============================
# 1. Django Setup
# ===============================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movieDB.settings")
django.setup()

# ===============================
# 2. Cloudinary Config
# ===============================
cloudinary.config(
    cloud_name="degiuwqhz",
    api_key="251445754961193",
    api_secret="96fgHTeudQvToGPdwzDBOGDgcgw"
)

# ===============================
# 3. Models
# ===============================
from mymovie.models import Actor, Movie, Platform, WebSeries


# ===============================
# 4. Upload Function
# ===============================
def upload_image(file_path):
    result = cloudinary.uploader.upload(file_path)
    return result["secure_url"]


def process_instance(instance, field_name):

    if not getattr(instance, field_name):
        return

    value = str(getattr(instance, field_name)).strip()

    # Skip already cloudinary
    if value.startswith("http"):
        print(f"Skipping (already cloudinary): {value}")
        return

    value = value.replace("image/upload/", "")

    local_path = os.path.join(settings.MEDIA_ROOT, value)

    if os.path.exists(local_path):
        print(f"Uploading: {local_path}")

        try:
            url = upload_image(local_path)
        except Exception as e:
            print(f"Upload failed: {local_path} -> {e}")
            return

        setattr(instance, field_name, url)
        instance.save()

        print(f"Updated: {url}")

    else:
        print(f"File not found: {local_path}")
        setattr(instance, field_name, None)
        instance.save()


# ===============================
# 5. Run Migration
# ===============================
print("🚀 Starting Cloudinary Migration...\n")

# Actor
for obj in Actor.objects.all():
    process_instance(obj, "act_image")

# Movie
for obj in Movie.objects.all():
    process_instance(obj, "mov_banner")

# Platform
for obj in Platform.objects.all():
    process_instance(obj, "plat_logo")

# WebSeries
for obj in WebSeries.objects.all():
    process_instance(obj, "series_banner")

print("\n✅ Migration Completed Successfully!")