from game_server.protocol.cmd_id import CmdID
from game_server.utils.time import current_milli_time
from game_server import HandlerRouter,Connection
from lib.proto import MarkMapReq, PlayerEnterSceneNotify ,Vector ,EnterType, MarkMapRsp
import enet

router = HandlerRouter()
@router(CmdID.MarkMapReq)
def handle_map_tp(conn: Connection, msg: MarkMapReq):
    if msg.mark:
        player_enter_scene_notify = PlayerEnterSceneNotify()
        player_enter_scene_notify.scene_id = msg.mark.scene_id
        player_enter_scene_notify.pos = Vector(msg.mark.pos.x, 500, msg.mark.pos.z)
        player_enter_scene_notify.scene_begin_time = current_milli_time()
        player_enter_scene_notify.type = EnterType.ENTER_GOTO
        player_enter_scene_notify.enter_scene_token = 1000
        player_enter_scene_notify.world_level = 8
        player_enter_scene_notify.target_uid = conn.player.uid
        conn.send(player_enter_scene_notify)

