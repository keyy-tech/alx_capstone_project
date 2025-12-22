from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status, generics
from django.db import transaction
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    AdminUpdateRoleSerializer,
)
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from django.conf import settings
from djoser import signals


@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "password": {"type": "string"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "user_profile": {
                    "type": "object",
                    "properties": {
                        "other_name": {"type": "string"},
                        "date_of_birth": {"type": "string", "format": "date"},
                        "phone_number": {"type": "string"},
                    },
                },
            },
        }
    },
    tags=["users"],
)
class RegisterCustomerView(CreateAPIView):
    """
    Register a new customer user.

    Accepts user registration data and an optional `user_profile` object in
    the request payload. Creates a new User with the `is_customer` flag set
    and optionally creates an associated UserProfile.
    """

    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        profile_data = request.data.pop("user_profile", None)

        with transaction.atomic():
            # Create user
            user_serializer = UserRegistrationSerializer(data=request.data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()

            if settings.DJOSER.get("SEND_ACTIVATION_EMAIL"):
                user.is_active = False  # Deactivate account until it is confirmed
                user.save()
                print("User account set to inactive until email confirmation")

            # Create profile
            profile_response_data = None
            if profile_data:
                profile_serializer = UserProfileSerializer(data=profile_data)
                profile_serializer.is_valid(raise_exception=True)
                profile_serializer.save(user=user)
                profile_response_data = profile_serializer.data

            # Send signal for user registration
            if settings.DJOSER.get("SEND_ACTIVATION_EMAIL"):
                signals.user_registered.send(
                    sender=self.__class__, user=user, request=request
                )
                print("Successfully sent user_registered signal")

        data = {
            "message": "Customer account created successfully",
            "status": True,
            "user": user_serializer.data,
            "user_profile": profile_response_data,
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()

        if not user.is_authenticated:
            return Response(
                {
                    "message": "Authentication credentials were not provided.",
                    "status": False,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Check if the user is a superuser
        if not user.is_superuser:
            return Response(
                {
                    "message": "You don't have the permission to perform this action, Contact the customer support",
                    "status": False,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Pop role from the data to prevent updating it
        data.pop("role", None)

        with transaction.atomic():
            # Update user
            user_serializer = UserRegistrationSerializer(user, data=data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

            # Update profile if provided
            profile_data = data.pop("user_profile", None)
            profile_response_data = None
            if profile_data:
                profile_serializer = UserProfileSerializer(
                    user.user_profile, data=profile_data, partial=True
                )
                profile_serializer.is_valid(raise_exception=True)
                profile_serializer.save()
                profile_response_data = profile_serializer.data
        response_data = {
            "message": "Customer account updated successfully",
            "status": True,
            "user": user_serializer.data,
            "user_profile": profile_response_data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["users"],
)
class AdminUpdateRoleView(generics.UpdateAPIView):
    """
    Allows admin users to update the role of a user.
    """

    permission_classes = [IsAdminUser]
    serializer_class = AdminUpdateRoleSerializer
    queryset = User.objects.all()

    def get_object(self):
        user_id = self.kwargs["user_id"]
        return generics.get_object_or_404(User, id=user_id)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        if user.role == "owner":
            return Response(
                {
                    "message": "User is already an owner.",
                    "status": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        role_serializer = self.serializer_class(user, data=request.data, partial=True)
        role_serializer.is_valid(raise_exception=True)
        role_serializer.save()

        # Send notification email to the user about role change
        send_mail(
            "Congratulations on Becoming a Restaurant Owner",
            f"Dear {user.first_name},\n\n"
            "We are delighted to inform you that your account has been successfully upgraded to a Restaurant Owner.\n\n"
            "You now have full access to manage your restaurant on our platform, including adding menu items, updating restaurant details, and tracking orders.\n\n"
            "We look forward to supporting you as you grow your restaurant business with us.\n\n"
            "Thank you for being a valued member of our community.\n\n"
            "Sincerely,\n"
            "The Multi Restaurant Team",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response(
            {
                "message": "User role updated successfully.",
                "status": True,
                "user": role_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
