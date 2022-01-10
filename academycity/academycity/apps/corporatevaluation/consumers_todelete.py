import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Thread, Whiteboard, WhiteboardData
from ..courses.models import Section, CourseSchedule
from ..core.utils import log_debug, clear_log_debug


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

        # if (self.channel_name != sender_channel_name) or (type == "chat_message"):
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



# import asyncio
# import json
# from django.contrib.auth import get_user_model
# from channels.consumer import AsyncConsumer
# from channels.db import database_sync_to_async
# # from .models import Thread, Whiteboard, WhiteboardData
# from ..courses.models import Section, CourseSchedule
# from ..core.utils import log_debug, clear_log_debug
# from tda import auth
# from tda.streaming import StreamClient
from ..core.OptionsAmeriTrade import BaseTDAmeriTrade






# class OptionsConsumer(AsyncConsumer, BaseTDAmeriTrade):
#     def __init__(self, scope):
#         super().__init__(scope)
#         clear_log_debug()
#         self.chat_room = None
#         log_debug("init_OptionsConsumer")
#         # -- AmeriTrade --
#
#     async def order_book_handler(self, msg):
#         # print(json.dumps(msg, indent=4))
#         response_ = {
#             'msg': msg,
#             'type': 'msg',
#             'sender_channel_name': self.channel_name
#         }
#         await self.channel_layer.group_send(
#             self.chat_room,
#             {
#                 'type': 'chat_message',
#                 'text': json.dumps(response_)
#             })
#
#     def activate_streaming(self, dic):
#         dic = eval(dic)
#         ticker_ = dic['ticker']
#         log_debug(ticker_)
#         asyncio.run(self.read_stream(add_func='add_options_book_handler', func="self.order_book_handler",
#                                      subs_func="options_book_subs", tickers=ticker_))
#
#     async def websocket_connect(self, event):
#         # print("connected", event)
#         log_debug("connected_OptionsConsumer")
#         await self.send({
#             'type': 'websocket.accept'
#         })
#
#         self.chat_room = self.scope['url_route']['kwargs']['group']
#         me = self.scope['user']
#         log_debug(self.chat_room)
#
#         await self.channel_layer.group_add(
#             self.chat_room,
#             self.channel_name
#         )
#         response_ = {
#             'msg': 'onconnect',
#             'username': me.username,
#             'type': 'connected',
#             'sender_channel_name': self.channel_name
#         }
#         log_debug("before await self.channel_layer.group_send")
#         await self.channel_layer.group_send(
#             self.chat_room,
#             {
#                 'type': 'chat_message',
#                 'text': json.dumps(response_)
#             })
#         log_debug("after await self.channel_layer.group_send")
#
#     async def websocket_receive(self, event, white=None):
#         data = event.get("text", None)
#         if data is not None:
#             text_data = json.loads(data)
#             msg = text_data.get("message")
#             type_ = text_data.get("type")
#             user = self.scope['user']
#
#             user_call_id = ""
#             try:
#                 user_call_id = text_data.get("user_call_id")
#             except Exception as ex:
#                 pass
#
#             # print('---type---')
#             # print(type)
#             # print('----type----')
#             # print('---msg---')
#             # print(msg)
#             # print('---msg---')
#
#             # if type_ == "wm":
#             #     await self.record_whiteboard_movment(msg)
#
#             response_ = {
#                 'msg': msg,
#                 'username': user.username,
#                 'user_id': user.id,
#                 'user_call_id': user_call_id,
#                 'type': type_,
#                 'sender_channel_name': self.channel_name
#             }
#
#             # print(response_)
#
#             await self.channel_layer.group_send(
#                 self.chat_room,
#                 {
#                     'type': 'chat_message',
#                     'text': json.dumps(response_)
#                 })
#
#     async def chat_message(self, event):
#         log_debug("before chat_message")
#         await asyncio.sleep(1)
#         await self.send({
#             'type': 'websocket.send',
#             'text': event['text']
#         })
#         log_debug("after chat_message")
#
#     async def websocket_disconnect(self, event):
#         await self.channel_layer.group_discard(
#             self.chat_room,
#             self.channel_name
#         )
