import asyncio
import datetime
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Thread, Whiteboard, WhiteboardData
from ..corporatevaluation.models import XBRLCompanyInfo, XBRLRealEquityPrices
from ..courses.models import Section, CourseSchedule
from ..core.OptionsAmeriTrade import BaseTDAmeriTrade
from ..core.utils import log_debug


class OptionsConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # print("connected", event)
        await self.send({
            'type': 'websocket.accept'
        })

        self.chat_room = self.scope['url_route']['kwargs']['group']
        me = self.scope['user']

        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )
        response_ = {
            'msg': 'onconnect',
            'username': me.username,
            'type': 'connected',
            'sender_channel_name': self.channel_name
        }
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response_)
            })

    async def websocket_receive(self, event, white=None):
        data = event.get("text", None)
        if data is not None:
            text_data = json.loads(data)
            type = text_data.get("type")

            user = self.scope['user']
            is_instructor = ""
            try:
                is_instructor = text_data.get("is_instructor")
            except Exception as ex:
                pass
            msg = ""
            try:
                msg = text_data.get("message")
            except Exception as ex:
                pass
            ticker = ""
            try:
                ticker = text_data.get("ticker")
            except Exception as ex:
                pass
            user_call_id = ""
            try:
                user_call_id = text_data.get("user_call_id")
            except Exception as ex:
                pass

            if type == "start_stream":
                for n in range(3):
                    msg = "   from start_stream: : " + str(n)
                    await self.send_stream(msg, n)
            # else:
                # if type == "data_received_chart_equity":
                #     await self.record_data_received_chart_equity(msg)

                response_ = {
                    'msg': msg,
                    'ticker': ticker,
                    'username': user.username,
                    'user_id': user.id,
                    'is_instructor': is_instructor,
                    'user_call_id': user_call_id,
                    'type': type,
                    'sender_channel_name': self.channel_name
                }
                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        'type': 'chat_message',
                        'text': json.dumps(response_)
                    })

    async def send_stream(self, msg, n):
        # await asyncio.sleep(n)
        s__ = str(datetime.datetime.now())
        response_ = {
            'msg': msg + " == " + s__,
            'type': "received_stream",
            'sender_channel_name': self.channel_name,
            'ticker': "ticker",
            'username': "amos",
            'user_id': "5",
            'is_instructor': "none",
            'user_call_id': "6",
        }
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response_)
            })

    async def chat_message(self, event):
        type_ = json.loads(event['text'])['type']
        msg_ = json.loads(event['text'])['msg']

        if type_ == "data_received_chart_equity":
            await self.record_data_received_chart_equity(msg_)

        # if (self.channel_name != sender_channel_name) or (type == "chat_message"):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def whiteboard_created_message(self, event):
        type = json.loads(event['text'])['type']
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.chat_room,
            self.channel_name
        )

    @database_sync_to_async
    def record_data_received_chart_equity(self, msg):
        for k in msg:
            ll = msg[k]
            log_debug("before data update for " + k)
            XBRLRealEquityPrices.objects.create(ticker=k, t=ll[0], o=ll[1], h=ll[2], l=ll[3], c=ll[4], v=ll[5])
            log_debug("data for " + k + " was updated")


class ChatWhiteBaordConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # print("connected", event)
        await self.send({
            'type': 'websocket.accept'
        })

        self.chat_room = self.scope['url_route']['kwargs']['group']
        me = self.scope['user']

        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )
        response_ = {
            'msg': 'onconnect',
            'username': me.username,
            'type': 'connected',
            'sender_channel_name': self.channel_name
        }
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response_)
            })

    async def websocket_receive(self, event, white=None):
        data = event.get("text", None)
        if data is not None:
            text_data = json.loads(data)
            msg = text_data.get("message")
            type = text_data.get("type")
            user = self.scope['user']
            is_instructor = ""
            try:
                is_instructor = text_data.get("is_instructor")
            except Exception as ex:
                pass

            user_call_id = ""
            try:
                user_call_id = text_data.get("user_call_id")
            except Exception as ex:
                pass

            # print('---type---')
            # print(type)
            # print('----type----')
            # print('---msg---')
            # print(msg)
            # print('---msg---')

            if type == "wm":
                await self.record_whiteboard_movment(msg)

            response_ = {
                'msg': msg,
                'username': user.username,
                'user_id': user.id,
                'is_instructor': is_instructor,
                'user_call_id': user_call_id,
                'type': type,
                'sender_channel_name': self.channel_name
            }

            # print(response_)

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(response_)
                })

    async def whiteboard_created_message(self, event):
        type = json.loads(event['text'])['type']
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def chat_message(self, event):
        sender_channel_name = json.loads(event['text'])['sender_channel_name']
        type = json.loads(event['text'])['type']

        if (self.channel_name != sender_channel_name) or (type == "chat_message"):
            await self.send({
                'type': 'websocket.send',
                'text': event['text']
            })

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.chat_room,
            self.channel_name
        )

    @database_sync_to_async
    def record_whiteboard_movment(self, msg):
        ll = msg.split(",")
        # print('-'*150)
        # print(ll)
        # print(ll[7])
        # print('-'*100)
        wb = Whiteboard.objects.get(id=ll[7])
        # print(wb)
        u = get_user_model().objects.get(id=ll[8])
        # print(u)
        # print('-'*150)
        WhiteboardData.objects.create(whiteboard=wb, painter=u, color=ll[0], xf=ll[1], yf=ll[2], xt=ll[3],
                                      yt=ll[4], mode=ll[5], pen_size=ll[6])
        # print('---saved----')
        # print('-'*150)

    @database_sync_to_async
    def get_whiteboard(self):
        return Thread.objects.get_or_new(user, other_username)


# class ChatConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         # print("connected", event)
#         await self.send({
#             'type': 'websocket.accept'
#         })
#
#         self.chat_room = self.scope['url_route']['kwargs']['group']
#         me = self.scope['user']
#         await self.channel_layer.group_add(
#             self.chat_room,
#             self.channel_name
#         )
#
#     async def websocket_receive(self, event):
#         data = event.get("text", None)
#         if data is not None:
#             text_data = json.loads(data)
#             msg = text_data.get("message")
#         user = self.scope['user']
#
#         response_ = {
#             'msg': msg,
#             'username': user.username
#         }
#
#         await self.channel_layer.group_send(
#             self.chat_room,
#             {
#                 'type': 'chat_message',
#                 'text': json.dumps(response_)
#             }
#         )
#
#     async def chat_message(self, event):
#         await self.send({
#             'type': 'websocket.send',
#             'text': event['text']
#         })
#
#     async def websocket_disconnect(self, event):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.chat_room,
#             self.channel_name
#         )
