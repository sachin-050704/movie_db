import os
import cloudinary.uploader
from django.conf import settings
import django
import cloudinary

cloudinary.config(
    cloud_name="degiuwqhz",
    api_key="251445754961193",
    api_secret="96fgHTeudQvToGPdwzDBOGDgcgw"
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movieDB.settings")
django.setup()

from mymovie.models import Actor  # change if your model name differs

def upload_image(file_path):
    result = cloudinary.uploader.upload(file_path)
    return result['secure_url']

for actor in Actor.objects.all():
    if actor.act_image:
        local_path = os.path.join(settings.MEDIA_ROOT, str(actor.act_image))

        if os.path.exists(local_path):
            print("Uploading:", local_path)
            url = upload_image(local_path)
            actor.act_image = url
            actor.save()
            print("Updated:", url)