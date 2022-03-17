from rest_framework.response import Response
from rest_framework import viewsets, parsers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from .models import Subscription
from .serializers import SubscriptionModelSerializer
from django.db import transaction
from . import send_email as sm
from validate_email import validate_email


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
                    "msg": serializer.errors,
                    "data": None,
                },
                status=status.HTTP_200_OK,
            )
        with transaction.atomic():
            subscription = serializer.save()
            is_valid = validate_email(subscription.email, verify=True)
            if is_valid == True:
                try:
                    sm.send_email(name=subscription.name, recepient=subscription.email)
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
                return Response(
                    {
                        "success": False,
                        "error": True,
                        "msg": "Email is Invalid",
                        "data": None,
                    },
                    status=status.HTTP_200_OK,
                )

        return Response(
            {"success": True, "error": False, "msg": None, "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
