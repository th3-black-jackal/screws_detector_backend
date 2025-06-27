from django.db import models
from django.core.validators import MinValueValidator

class Machine(models.Model):
    STATUS_CHOICES = [
        ("OFF", "Off"),
        ("ON", "On"),
        ("ERR", "Error"),
    ]

    name            = models.CharField(max_length=120, unique=True)
    description     = models.TextField(blank=True)
    status          = models.CharField(max_length=3, choices=STATUS_CHOICES, default="OFF")
    last_heartbeat  = models.DateTimeField(auto_now=True)
    is_active       = models.BooleanField(default=True)

    # e.g. current temperature, runtime secs, etc.
    operating_param = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Example numeric parameter"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.status})"
