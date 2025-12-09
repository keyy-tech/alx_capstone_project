from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import BaseRegistrationSerializer, UserProfileSerializer


class RegisterCustomerView(CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Extract profile data
        profile_data = request.data.pop("user_profile", None)

        # Create user
        user_serializer = BaseRegistrationSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(is_customer=True)  # Set customer flag

        # Create profile
        profile_response_data = None
        if profile_data:
            profile_serializer = UserProfileSerializer(data=profile_data)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save(user=user)
            profile_response_data = profile_serializer.data

        # Return response manually
        data = {
            "message": "Customer account created successfully",
            "status": True,
            "user": user_serializer.data,
            "user_profile": profile_response_data,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class RegisterOwnerView(CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        profile_data = request.data.pop("user_profile", None)

        # Create user
        user_serializer = BaseRegistrationSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(is_owner=True)

        # Create profile
        profile_response_data = None
        if profile_data:
            profile_serializer = UserProfileSerializer(data=profile_data)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save(user=user)
            profile_response_data = profile_serializer.data

        data = {
            "message": "Owner account created successfully",
            "status": True,
            "user": user_serializer.data,
            "user_profile": profile_response_data,
        }
        return Response(data, status=status.HTTP_201_CREATED)
