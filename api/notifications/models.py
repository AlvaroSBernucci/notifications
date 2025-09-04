from django.db import models
import uuid

class Notification(models.Model):
    class NotificationStatus(models.TextChoices):
        QUEUED = "queued", "Na fila"
        DELIVERED = "delivered", "Entregue"

    status = models.CharField(max_length=20, choices=NotificationStatus.choices, default=NotificationStatus.QUEUED)
    notification = models.TextField()
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"

    def __str__(self):
        return f"Notificação"