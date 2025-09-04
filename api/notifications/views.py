import pika
import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from .publisher import RabbitPublisher

class NotificationView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            temp_notification = Notification(notification=serializer.validated_data["notification"])
            exchange_name = "fila.notificacao.entrada.alvaro"
            body = {
                "mensagemId": str(temp_notification.uuid), 
                "conteudoMensagem": temp_notification.notification
            }
            publish = RabbitPublisher(exchange_name)
            publish.send_message(body)

            temp_notification.status = Notification.NotificationStatus.QUEUED
            temp_notification.save()
            return Response({"status": temp_notification.get_status_display(), "mensagemId": temp_notification.uuid, "notification": temp_notification.notification},
                status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        