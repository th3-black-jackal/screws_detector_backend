import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Machine

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Machine)
def machine_changed(sender, instance, created, **kwargs):
    verb = "CREATED" if created else "UPDATED"
    logger.info("Machine %s – %s by %s", instance.name, verb, instance.status)
