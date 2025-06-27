from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .models import Machine
from .serializers import MachineSerializer, UserSerializer

class MachineViewSet(viewsets.ModelViewSet):
    """
    Full CRUD on Machine.
    Only staff can DELETE.
    """
    queryset           = Machine.objects.all()
    serializer_class   = MachineSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class UserViewSet(viewsets.ModelViewSet):
    """
    Exposes non-privileged user info.
    Creation limited to superusers via admin site.
    """
    queryset           = User.objects.all()
    serializer_class   = UserSerializer
    http_method_names  = ["get", "patch", "put"]      # no POST/DELETE here
    permission_classes = [permissions.IsAdminUser]
