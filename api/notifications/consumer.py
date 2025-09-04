import os
import sys
import django
import pika
import json
import asyncio

from django.conf import settings
from channels.layers import get_channel_layer

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # /api/notifications/
PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)  # /api/
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

class RabbitConsumer:
    def __init__(self, callback):
        self.queue_name = "fila.notificacao.entrada.alvaro"
        self.callback = callback
        self.URL_PARAMETERS = settings.URL_PARAMETERS
        self.connection = pika.BlockingConnection(pika.URLParameters(self.URL_PARAMETERS))
        self.channel = self._create_channel()

    def _create_channel(self):
        channel = self.connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=True)
        channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback,
            auto_ack=True
        )
        return channel

    def start(self):
        print("Listen RabbitMQ on port 5672")
        self.channel.start_consuming()

    async def receive(self, text_data):
        data = json.loads(text_data)
        mensagem = data.get("mensagem")
        await self.send(text_data=json.dumps({
            "mensagem": f"Recebi: {mensagem}"
        }))

def my_callback(ch, method, properties, body):
    mensagem = body.decode()
    print(f"📩 Mensagem recebida do RabbitMQ: {mensagem}")
    channel_layer = get_channel_layer()

    asyncio.run(
        channel_layer.group_send(
            "grupo_mensagens",
            {
                "type": "nova.mensagem",
                "mensagem": mensagem,
            },
        )
    )


if __name__ == "__main__":
    rabbitmq_consumer = RabbitConsumer(my_callback)
    rabbitmq_consumer.start()