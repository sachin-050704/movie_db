from django.shortcuts import render
import razorpay
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Rental
from mymovie.models import Movie,WebSeries
from razorpay.errors import SignatureVerificationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .signals import rental_success

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    amount = int(request.data.get('amount', 0)) * 100  # in paise
    content_type = request.data.get('type')  # "movie" or "webseries"
    content_id = request.data.get('id')

    # Validate ID
    try:
        content_id = int(content_id)
    except (ValueError, TypeError):
        return Response({"error": "Content ID must be a number"}, status=400)

    if not content_type or not content_id:
        return Response({"error": "Content type and ID are required"}, status=400)

    movie = None
    webseries = None

    try:
        if content_type == "movie":
            movie = Movie.objects.get(id=content_id)
        elif content_type == "webseries":
            webseries = WebSeries.objects.get(id=content_id)
        else:
            return Response({"error": "Invalid content type"}, status=400)
    except (Movie.DoesNotExist, WebSeries.DoesNotExist):
        return Response({"error": "Invalid content ID"}, status=400)

    # Create Razorpay order
    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    # Save order in DB
    rental = Rental.objects.create(
        user=request.user,
        movie=movie,
        webseries=webseries,
        amount=amount,
        razorpay_order_id=order['id']
    )

    return Response(order)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    data = request.data

    required_fields = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature']
    if not all(field in data for field in required_fields):
        return Response({"status": "failed", "error": "Missing fields"}, status=400)

    params_dict = {
        'razorpay_order_id': data['razorpay_order_id'],
        'razorpay_payment_id': data['razorpay_payment_id'],
        'razorpay_signature': data['razorpay_signature']
    }

    try:
        # Verify signature
        client.utility.verify_payment_signature(params_dict)

        rental = Rental.objects.get(razorpay_order_id=params_dict['razorpay_order_id'])
        rental.razorpay_payment_id = params_dict['razorpay_payment_id']
        rental.razorpay_signature = params_dict['razorpay_signature']
        rental.status = "success"
        rental.save()
        rental_success.send(
            sender=Rental,
            rental=rental
        )

        return Response({"status": "success"})

    except SignatureVerificationError:
        return Response({"status": "failed", "error": "Signature verification failed"}, status=400)

    except Rental.DoesNotExist:
        return Response({"status": "failed", "error": "Order not found"}, status=400)
    




class AdminRentalViewSet(ModelViewSet):
    queryset = Rental.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH", "PUT"]:
            return RentalWriteSerializer
        return RentalReadSerializer