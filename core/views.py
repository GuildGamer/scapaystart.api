from rest_framework.response import Response
from rest_framework import viewsets, parsers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from .models import Subscription
from .serializers import SubscriptionModelSerializer
from django.db import transaction
from . import send_email as sm
from validate_email_address import validate_email
from . import check_email as ce


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
        if Subscription.objects.filter(email=email).len() > 0:
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
            is_valid = ce.check(email)
            if is_valid == True:
                print(f"VALID EMAIL {email}, {is_valid}")
                try:
                    sm.send_email(name=name, recepient=email)
                except Exception as e:
                    return Response(
                        {
                            "success": False,
                            "error": True,
                            "msg": "Email failed to send. Please check your email and try again",
                            "data": None,
                        },
                        status=status.HTTP_200_OK,
                    )
            else:
                print(f"INVALID EMAIL {email}, {is_valid}")
                return Response(
                    {
                        "success": False,
                        "error": True,
                        "msg": "Email is Invalid",
                        "data": None,
                    },
                    status=status.HTTP_200_OK,
                )

        subscription = Subscription.objects.create(name=name, email=email)
        return Response(
            {"success": True, "error": False, "msg": None, "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
