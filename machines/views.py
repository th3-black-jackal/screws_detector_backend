from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from .models import Machine
from .serializers import MachineSerializer, UserSerializer
import paho.mqtt.client as mqtt

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_USERNAME = "testuser"
MQTT_PASSWORD = "testpass"
MQTT_TOPIC_PREFIX = "machines"


class MachineViewSet(viewsets.ModelViewSet):
    """
    Full CRUD on Machine.
    Only staff can DELETE.
    """
    queryset           = Machine.objects.all()
    serializer_class   = MachineSerializer

    def _publish_status(self, machine_id, status_message):
        client = mqtt.Client()
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        client.connect(MQTT_BROKER, MQTT_PORT)
        topic = f"{MQTT_TOPIC_PREFIX}/{machine_id}/status"
        client.publish(topic, status_message)
        client.disconnect()

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=["post"])
    def open(self, request, pk=None):
        machine = self.get_object()
        machine.status = "ON"
        machine.save(update_fields=["status"])
        self._publish_status(machine.id, "ON")
        return Response({"status": "opened"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        machine = self.get_object()
        machine.status = "OFF"
        machine.save(update_fields=["status"])
        self._publish_status(machine.id, "OFF")

        return Response({"status": "closed"}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    """
    Exposes non-privileged user info.
    Creation limited to superusers via admin site.
    """
    queryset           = User.objects.all()
    serializer_class   = UserSerializer
    http_method_names  = ["get", "patch", "put"]      # no POST/DELETE here
    permission_classes = [permissions.IsAdminUser]
