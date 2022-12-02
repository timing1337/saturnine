from game_server.protocol.cmd_id import CmdID
from game_server import HandlerRouter,Connection
from game_server.utils.time import current_milli_time
from lib.retcode import Retcode
from game_server.resource import resources
from lib.proto import SceneTransToPointReq, SceneTransToPointRsp, PlayerEnterSceneNotify, Vector ,EnterType
import enet

router = HandlerRouter()
@router(CmdID.SceneTransToPointReq)
def handle_SceneTransToPoint(conn: Connection, msg: SceneTransToPointReq):
    point_data = resources.binoutput.config_scene[msg.scene_id].points
    
    scene_id = point_data[msg.point_id].tranSceneId
    pos = point_data[msg.point_id].tranPos
    
    conn.send(conn.player.get_teleport_packet(scene_id, pos, EnterType.ENTER_GOTO))

    scene_trans_to_point_rsp = SceneTransToPointRsp()
    scene_trans_to_point_rsp.retcode = 0
    scene_trans_to_point_rsp.scene_id = msg.scene_id
    scene_trans_to_point_rsp.point_id = msg.point_id
    conn.send(scene_trans_to_point_rsp)

    
    
    