from django.shortcuts import render
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def register_page(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'Message':'Registration Successful'},status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def user_list(request):
    user = User.objects.all()
    serializer = UserReadSerializer(user, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)  
    if serializer.is_valid():
        if 'password' in serializer.validated_data:
            user.set_password(serializer.validated_data['password'])
        serializer.save()
        return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "username": request.user.username,
        "email": request.user.email,
        "contact": request.user.contact,
        "profile": request.user.profile.url if request.user.profile else None,
        "created_at": request.user.created_at
    })



class AdminUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH", "PUT"]:
            return UserWriteSerializer
        return UserReadSerializer
    
    