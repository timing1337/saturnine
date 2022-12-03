from game_server.protocol.cmd_id import CmdID
from game_server import HandlerRouter,Connection
from game_server.utils.time import current_milli_time
from lib.retcode import Retcode
from game_server.resource import resources
from lib.proto import PersonalSceneJumpReq, PersonalSceneJumpRsp, PlayerEnterSceneNotify, Vector ,EnterType
import enet

router = HandlerRouter()
@router(CmdID.PersonalSceneJumpReq)
def handle_PersonalSceneJump(conn: Connection, msg: PersonalSceneJumpReq):
    point_data = resources.binoutput.config_scene[conn.player.scene_id].points
        
    scene_id = point_data[msg.point_id].tranSceneId
    pos = point_data[msg.point_id].tranPos
    
    conn.player.pos = pos
    
    player_enter_scene_notify = PlayerEnterSceneNotify()
    player_enter_scene_notify.scene_id = scene_id
    player_enter_scene_notify.pos = pos
    player_enter_scene_notify.scene_begin_time = current_milli_time()
    player_enter_scene_notify.type = EnterType.ENTER_JUMP
    player_enter_scene_notify.enter_scene_token = 1000
    player_enter_scene_notify.world_level = 8
    player_enter_scene_notify.target_uid = conn.player.uid
    player_enter_scene_notify.prev_scene_id = conn.player.scene_id
    player_enter_scene_notify.prev_pos = conn.player.pos    
    conn.send(player_enter_scene_notify)
    
    conn.player.scene_id = scene_id
        
    personal_scene_jump = PersonalSceneJumpRsp()
    personal_scene_jump.retcode = 0
    personal_scene_jump.dest_scene_id = scene_id
    personal_scene_jump.dest_pos = pos
    conn.send(personal_scene_jump)
    
    
    