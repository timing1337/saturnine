from game_server.protocol.packet import Packet
from game_server.protocol.cmd_id import CmdID
from game_server.encryption import new_key
from game_server import HandlerRouter,Connection
from lib.proto import GetPlayerTokenReq,GetPlayerTokenRsp,PlayerLoginReq,PlayerLoginRsp,OpenStateUpdateNotify,StoreWeightLimitNotify,StoreType,PlayerStoreNotify,Vector,PlayerDataNotify,PropValue
from game_server.game.player import Player
from game_server.utils.time import current_milli_time
from game_server.resource.enums import PropType
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
    conn.player = Player(uid=rsp.uid, name="saturnine")
    conn.player.prop_map = {
        PropType.PROP_IS_SPRING_AUTO_USE: 1,
        PropType.PROP_SPRING_AUTO_USE_PERCENT: 50,
        PropType.PROP_IS_FLYABLE: 1,
        PropType.PROP_IS_TRANSFERABLE: 1,
        PropType.PROP_CUR_PERSIST_STAMINA: 24000,
        PropType.PROP_MAX_STAMINA: 24000,
        PropType.PROP_PLAYER_LEVEL: 60,
        PropType.PROP_PLAYER_EXP: 0,
    }

@router(CmdID.PlayerLoginReq)
def handle_login(conn: Connection, msg: PlayerLoginReq):
    conn.player.scene_id = 3
    conn.player.pos = Vector(0, 100, 0)
    open_state = OpenStateUpdateNotify()
    open_state.open_state_map = {}
    for x in range(600):
        open_state.open_state_map[x] = 1
    
    store_weight_limit = StoreWeightLimitNotify()
    store_weight_limit.store_type = StoreType.STORE_PACK
    store_weight_limit.weight_limit = 10000

    player_store_notify = PlayerStoreNotify()
    player_store_notify.weight_limit = 10000
    player_store_notify.store_type = StoreType.STORE_PACK
    player_store_notify.item_list = []

    player_data_notify = PlayerDataNotify()
    player_data_notify.nick_name = conn.player.name
    player_data_notify.server_time = current_milli_time()
    player_data_notify.is_first_login_today = False
    player_data_notify.region_id = 1
    player_data_notify.prop_map = {}
    
    for prop, value in conn.player.prop_map.items():
        #dont ask me please
        player_data_notify.prop_map[prop._value_] = PropValue(type=prop._value_, val=value, ival=value)

    rsp = PlayerLoginRsp()
    rsp.game_biz = "hk4e"
    rsp.is_use_ability_hash = False
    rsp.is_new_player = False
    rsp.target_uid = conn.player.uid
    
    conn.send(open_state)
    conn.send(store_weight_limit)
    conn.send(player_store_notify)
    conn.send(player_data_notify)
    conn.send(conn.player.get_teleport_packet(conn.player.scene_id, conn.player.pos))
    conn.send(rsp)