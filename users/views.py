from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import BaseRegistrationSerializer, UserProfileSerializer


@extend_schema(request=BaseRegistrationSerializer, tags=["users"])
class RegisterCustomerView(CreateAPIView):
    """
    Register a new customer user.

    Accepts user registration data and an optional `user_profile` object in
    the request payload. Creates a new User with the `is_customer` flag set
    and optionally creates an associated UserProfile.

    Methods:
        post(request): Validate and create a customer user (and profile).
    """

    permission_classes = [AllowAny]
    serializer_class = BaseRegistrationSerializer

    def post(self, request, *args, **kwargs):
        """
        Create a new customer user and optional profile.

        Args:
            request (rest_framework.request.Request): Incoming request. The
                payload should include user fields expected by
                BaseRegistrationSerializer. Optionally include
                `user_profile` dict for profile creation.

        Returns:
            rest_framework.response.Response: JSON response with created
            user data and profile data (HTTP 201) on success.

        Side effects:
            Creates a new User (is_customer=True) and possibly a UserProfile.
        """
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


@extend_schema(request=BaseRegistrationSerializer, tags=["users"])
class RegisterOwnerView(CreateAPIView):
    """
    Register a new owner user.

    Similar to RegisterCustomerView but sets the `is_owner` flag on the
    created User. Optionally creates an associated UserProfile.

    Methods:
        post(request): Validate and create an owner user (and profile).
    """

    permission_classes = [AllowAny]
    serializer_class = BaseRegistrationSerializer

    def post(self, request, *args, **kwargs):
        """
        Create a new owner user and optional profile.

        Args:
            request (rest_framework.request.Request): Incoming request. The
                payload should include user fields expected by
                BaseRegistrationSerializer. Optionally include
                `user_profile` dict for profile creation.

        Returns:
            rest_framework.response.Response: JSON response with created
            user data and profile data (HTTP 201) on success.

        Side effects:
            Creates a new User (is_owner=True) and possibly a UserProfile.
        """
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
