from rest_framework import serializers
from .models import Rental

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ["id", "user", "amount", "status", "rented_at"]



class RentalReadSerializer(serializers.ModelSerializer):
    movie = serializers.CharField(source="movie.mov_name", read_only=True)
    webseries = serializers.CharField(source="webseries.series_name", read_only=True)
    user = serializers.CharField(source="user.username", read_only=True)

    movie_id = serializers.IntegerField(source="movie.id", read_only=True)
    webseries_id = serializers.IntegerField(source="webseries.id", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Rental
        fields = "__all__"


class RentalWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = [
            "id",
            "user",
            "movie",
            "webseries",
            "amount",
            "status",
            "razorpay_order_id"
        ]