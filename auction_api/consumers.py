import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Bid, Product
from django.core.cache import cache
from django.utils import timezone
class BidConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.product_id = self.scope['url_route']['kwargs']['product_id']
        self.product_group_name = f'bid_{self.product_id}'
        self.timer_key = f'product_{self.product_id}_timer'

        await self.channel_layer.group_add(
            self.product_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.product_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope['user']
        product = Product.objects.get(id=self.product_id)

        try:
            amount = int(data['amount'])
        except KeyError:
            return

        if amount < product.min_bid:
            return

        try:
            Bid.place_bid(user, product, amount)
        except ValueError:
            return


        cache.set(self.timer_key, timezone.now(), timeout=60)

        await self.channel_layer.group_send(
            self.product_group_name,
            {
                'type': 'bid_update',
                'amount': amount,
                'username': user.username,
            }
        )

    async def bid_update(self, event):
        amount = event['amount']
        username = event['username']

        await self.send(text_data=json.dumps({
            'amount': amount,
            'username': username,
        }))