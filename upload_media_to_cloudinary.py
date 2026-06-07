import os
import django
import cloudinary
import cloudinary.uploader
from django.conf import settings

# ✅ 1. Django setup FIRST
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movieDB.settings")
django.setup()

# ✅ 2. Cloudinary config (use env variables in production)
cloudinary.config(
    cloud_name="degiuwqhz",
    api_key="251445754961193",
    api_secret="96fgHTeudQvToGPdwzDBOGDgcgw"
)

from mymovie.models import Actor


def upload_image(file_path):
    result = cloudinary.uploader.upload(file_path)
    return result['secure_url']


for actor in Actor.objects.all():
    if not actor.act_image:
        continue

    value = str(actor.act_image)

    # ✅ Skip if already Cloudinary URL
    if value.startswith("http"):
        print("Skipping (already uploaded):", value)
        continue

    # ✅ Fix broken prefix if exists
    value = value.replace("image/upload/", "")

    local_path = os.path.join(settings.MEDIA_ROOT, value)

    if os.path.exists(local_path):
        print("Uploading:", local_path)

        url = upload_image(local_path)

        actor.act_image = url
        actor.save()

        print("Updated:", url)

    else:
        print("File not found:", local_path)