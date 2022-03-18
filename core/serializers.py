from rest_framework import serializers
from .models import Subscription


class SubscriptionModelSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
