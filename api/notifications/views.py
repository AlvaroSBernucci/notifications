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
        new_notification = serializer.save()

        try:
            exchange_name = "fila.notificacao.entrada.alvaro"
            body = {
                "mensagemId": str(new_notification.uuid), 
                "conteudoMensagem": new_notification.notification
            }
            publish = RabbitPublisher(exchange_name)
            publish.send_message(body)
            return Response({"status": new_notification.status, "mensagemId": new_notification.uuid},
                status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        