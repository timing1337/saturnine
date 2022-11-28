from game_server.protocol.cmd_id import CmdID
from game_server import HandlerRouter,Connection
from lib.proto import PingReq,PingRsp
import enet

router = HandlerRouter()

@router(CmdID.PingReq)
def handle_ping(conn: Connection, msg: PingReq):
    rsp = PingRsp()
    rsp.client_time = msg.client_time
    rsp.seq = msg.seq
    conn.send(rsp)
