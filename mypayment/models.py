from django.db import models
from django.conf import settings
from mymovie.models import Movie,WebSeries  

class Rental(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank=True, null=True, related_name="rentals")
    webseries = models.ForeignKey(WebSeries, on_delete=models.CASCADE, blank=True, null=True, related_name="rentals")
    razorpay_order_id = models.CharField(max_length=200)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=500, blank=True, null=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=50, default="created")
    rented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.movie} - {self.status}"