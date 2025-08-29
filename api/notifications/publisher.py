import pika
import json
from django.conf import settings


class RabbitPublisher():
    def __init__(self, exchange_name: str):
        self.exchange_name = exchange_name
        self.URL_PARAMETERS = settings.URL_PARAMETERS
        self.connection = pika.BlockingConnection(pika.URLParameters(self.URL_PARAMETERS))
        

    def _create_channel(self):
        return self.connection.channel()

    def send_message(self, body: dict) -> None:
        try:
            channel = self._create_channel()
            channel.queue_declare(queue=self.exchange_name, durable=True)
            channel.basic_publish(
                exchange="",
                routing_key=self.exchange_name,
                body=json.dumps(body),
                properties=pika.BasicProperties(delivery_mode=2),
            )
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
        finally:
            channel.close()
            
            
