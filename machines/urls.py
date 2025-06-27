from rest_framework.routers import DefaultRouter
from .views import MachineViewSet, UserViewSet

router = DefaultRouter()
router.register(r"machines", MachineViewSet, basename="machine")
router.register(r"users",    UserViewSet,    basename="user")

urlpatterns = router.urls
