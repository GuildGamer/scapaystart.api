from rest_framework.response import Response
from rest_framework import viewsets, parsers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from .models import Subscription
from .serializers import SubscriptionModelSerializer
from django.db import transaction
from . import send_email as sm
from email_validator import validate_email, EmailNotValidError


class SubscriptionViewSet(viewsets.ModelViewSet):

    """
    SubscriptionViewSet
    """

    serializer_class = SubscriptionModelSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
        url_path="add",
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request) -> Response:
        serializer = SubscriptionModelSerializer(data=request.data)

        if not serializer.is_valid():
            print(f"ERROR {serializer.errors}")
            return Response(
                {
                    "success": False,
                    "error": True,
                    "msg": "serializer error",
                    "data": None,
                },
                status=status.HTTP_200_OK,
            )
        email = serializer.data.get("email")
        name = serializer.data.get("name")
        if len(Subscription.objects.filter(email=email)) > 0:
            return Response(
                {
                    "success": False,
                    "error": True,
                    "msg": "email already exists",
                    "data": None,
                },
                status=status.HTTP_200_OK,
            )
        with transaction.atomic():
            try:
                # Validate.
                valid = validate_email(email)
                email = valid.email
            except EmailNotValidError as e:
                print(f"INVALID EMAIL {email}, {e}")
                return Response(
                    {
                        "success": False,
                        "error": True,
                        "msg": "Email is Invalid",
                        "data": None,
                    },
                    status=status.HTTP_200_OK,
                )

            print(f"VALID EMAIL {email}")
            try:
                sm.send_email(name=name, recepient=email)
            except Exception as e:
                return Response(
                    {
                        "success": False,
                        "error": True,
                        "msg": "Email is Invalid",
                        "message": "Email failed to send. Please try again later.",
                        "data": None,
                    },
                    status=status.HTTP_200_OK,
                )

        subscription = Subscription.objects.create(name=name, email=email)
        return Response(
            {"success": True, "error": False, "msg": None, "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
