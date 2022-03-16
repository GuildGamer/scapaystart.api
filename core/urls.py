from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet

router = DefaultRouter()
router.register(r"join-us", SubscriptionViewSet, basename="join-us")

urlpatterns = router.urls
app_name = "core"
