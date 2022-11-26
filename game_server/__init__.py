from __future__ import annotations
import threading
import enet
from game_server.protocol.packet import Packet
from game_server.protocol.cmd_id import CmdID
from game_server.encryption import xor, mt64
from typing import Callable
import betterproto

class Connection: 

    gameServer: GameServer
    peer: enet.Peer
    key: bytes
    
    def __init__(self, gameServer: GameServer, peer: enet.Peer) -> None:
        self.peer = peer
        self.gameServer = gameServer

    def handle(self, data: bytes):
        print(f'{self.peer.address}: Raw data: {data.hex()}')
        if hasattr(self, 'key'): 
            data = xor(data, self.key)
            print(f'{self.peer.address}: Xored: {data.hex()}')
        packet = Packet()
        packet.parse(data)
        print(f'{self.peer.address}: Received packet: {packet.body} | PacketHead: {packet.head} | Raw: {data.hex()}')
        if handler := self.gameServer.router.get(packet.cmdid):
            handler(self, packet.body)

    def send(self, msg: betterproto.Message):
        packet = bytes(Packet(body=msg))
        print(f'{self.peer.address}: Sending packet: {msg}')
        if hasattr(self, 'key'): 
            packet = xor(packet, self.key)
        self.send_raw(bytes(packet))

    def send_raw(self, data: bytes):
        print(f'{self.peer.address}: Sending raw: {data.hex()}')
        self.peer.send(0, enet.Packet(data))

        
Handler = Callable[[Connection, Packet], None]

class HandlerRouter:
    _handlers: dict[CmdID, HandlerRouter]

    def __init__(self):
        self._handlers = {}

    def add(self, router: HandlerRouter):
        self._handlers |= router._handlers

    def get(self, cmdid: CmdID) -> Handler | None:
        return self._handlers.get(cmdid)

    def __call__(self, cmdid: CmdID):
        def wrapper(handler: HandlerRouter):
            self._handlers[cmdid] = handler
            return handler
        return wrapper

class GameServer:

    router: HandlerRouter = HandlerRouter()
    conns: dict[str, Connection] = {}
    
    def __init__(self, host, port) -> None:
        self.host = enet.Host(enet.Address(host, port), 10, 0, 0, 0)
        self.host.checksum = enet.ENET_CRC32
        self.host.compress_with_range_coder()

    def add(self, router: HandlerRouter):
        self.router.add(router)

    def loop(self) -> None:
        while True:
            event = self.host.service(20)
            if event is not None:
                if event.type == enet.EVENT_TYPE_CONNECT:
                    self.conns[str(event.peer.address)] = Connection(self, event.peer)
                elif event.type == enet.EVENT_TYPE_DISCONNECT:
                    del self.conns[str(event.peer.address)] 
                elif event.type == enet.EVENT_TYPE_RECEIVE:
                    msg = event.packet.data
                    conn = self.conns[str(event.peer.address)]
                    conn.handle(msg)

    def start(self):
        b = threading.Thread(name='gameserver', target=self.loop)
        b.start()