from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

import os

class NamedUsersRoomsMixin(BroadcastMixin):
    def __init__(self, *args, **kwargs):
        super(NamedUsersRoomsMixin, self).__init__(*args, **kwargs)
        if 'rooms' not in self.session:
            self.session['rooms'] = set()  # a set of simple strings
            self.session['nickname'] = 'guest123'

    def join(self, room):
        """Lets a user join a room on a specific Namespace."""
        self.socket.rooms.add(self._get_room_name(room))

    def leave(self, room):
        """Lets a user leave a room on a specific Namespace."""
        self.socket.rooms.remove(self._get_room_name(room))

    def _get_room_name(self, room):
        return self.ns_name + '_' + room

    def emit_to_room(self, event, args, room):
        """This is sent to all in the room (in this particular Namespace)"""
        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)
        room_name = self._get_room_name(room)
        for sessid, socket in self.socket.server.sockets.iteritems():
            if not hasattr(socket, 'rooms'):
                continue
            if room_name in socket.rooms:
                socket.send_packet(pkt)

class ChatNamespace(BaseNamespace, NamedUsersRoomsMixin):
    def on_chat(self, msg):
        self.broadcast_event('chat', msg)

    def recv_connect(self):
        self.broadcast_event('user_connect')

    def recv_disconnect(self):
        self.broadcast_event('user_disconnect')
        self.disconnect(silent=True)

    def on_join(self, channel):
        self.join(channel)

    '''
    _registry = {}

    def initialize(self):
        self._registry[id(self)] = self
        self.emit('connect')
        self._nick = None

    def disconnect(self, *args, **kwargs):
        if self._nick:
            self._users.pop(self._nick, None)
            super(ChatNamespace, self).disconnect(*args, **kwargs)

    def on_login(self, nick):
        if self.nick:
            self._broadcast('exit', self.nick)
            self.nick = nick
            self._broadcast('enter', nick)
            self.emit('users',
                [ ns.nick
                  for ns in self._registry.values()
                  if ns.nick is not None ])

    def on_chat(self, message):
        if self.nick:
            self._broadcast('chat', dict(u=self.nick, m=message))
        else:
            self.emit('chat', dict(u='SYSTEM', m='You must first login'))

    def _broadcast(self, event, message):
        for s in self._registry.values():
            s.emit(event, message)
    '''
