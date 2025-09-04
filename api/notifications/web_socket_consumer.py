import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MensagemConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("grupo_mensagens", self.channel_name)
        await self.accept()
        print("✅ Cliente conectado ao WebSocket")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("grupo_mensagens", self.channel_name)

    async def nova_mensagem(self, event):
        mensagem = event["mensagem"]
        await self.send(text_data=json.dumps({"mensagem": mensagem}))
