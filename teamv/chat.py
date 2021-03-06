from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from datetime import datetime

import gevent
import os, time, json

class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    nicknames = []

    def on_chat(self, msg):
        current_time = time.strftime("%H:%M:%S")

        self.emit_to_room(self.room, 'chat', '{0}: {1}'.format(self.socket.session['nickname'], msg.lstrip()))
        with open('teamv/templates/logs/log_{0}.log'.format(self.room), 'a') as f:
            f.write('({0}) {1}: {2}\n'.format(current_time, self.socket.session['nickname'], msg.lstrip()))
    
    def on_join(self, room):
        self.room = room
        self.join(room)

    def on_nickname(self, nickname):

        current_time = time.strftime("%H:%M:%S")
        self.nicknames.append(nickname)
        self.nicknames.sort();

        self.socket.session['nickname'] = nickname
        self.emit_to_room(self.room, 'user_connect', nickname)
        with open('teamv/templates/logs/log_{0}.log'.format(self.room), 'a') as f:
            f.write('({0}) {1} connected\n'.format(current_time, nickname))
        return json.dumps(self.nicknames)

    def on_end(self):
        self.emit_to_room(self.room, 'end')

    def recv_disconnect(self):
        current_time = time.strftime("%H:%M:%S")

        nickname = self.socket.session['nickname']
        self.emit_to_room(self.room, 'user_disconnect', nickname)
        self.nicknames.remove(nickname)
        with open('teamv/templates/logs/log_{0}.log'.format(self.room), 'a') as f:
            f.write('({0}) {1} disconnected\n'.format(current_time, nickname))
        self.disconnect(silent=True)





