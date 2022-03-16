from rest_framework import serializers
from .models import Subscription


class SubscriptionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["name", "email"]
