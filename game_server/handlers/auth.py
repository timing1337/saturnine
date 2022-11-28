from game_server.protocol.packet import Packet
from game_server.protocol.cmd_id import CmdID
from game_server.encryption import new_key
from game_server import HandlerRouter,Connection
from lib.proto import GetPlayerTokenReq,GetPlayerTokenRsp,PlayerLoginReq,PlayerLoginRsp
import enet

router = HandlerRouter()

@router(CmdID.GetPlayerTokenReq)
def handle_token_req(conn: Connection, msg: GetPlayerTokenReq):
    mt_key = new_key(int(msg.account_uid))
    rsp = GetPlayerTokenRsp()
    rsp.uid = int(msg.account_uid)
    rsp.account_type = msg.account_type
    rsp.account_uid = msg.account_uid
    rsp.token = msg.account_token
    rsp.gm_uid = int(msg.account_uid)
    rsp.secret_key_seed = int(msg.account_uid)
    conn.send(rsp)
    conn.key = mt_key

def handle_login(conn: Connection, msg: PlayerLoginReq):
    
    rsp = PlayerLoginRsp()
    conn.send(rsp)