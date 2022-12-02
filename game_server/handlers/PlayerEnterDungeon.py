from game_server.protocol.cmd_id import CmdID
from game_server import HandlerRouter,Connection
from game_server.utils.time import current_milli_time
from lib.retcode import Retcode
from game_server.resource import resources
from lib.proto import PlayerEnterDungeonReq, PlayerEnterDungeonRsp, PlayerEnterSceneNotify, Vector ,EnterType
import enet

router = HandlerRouter()
@router(CmdID.PlayerEnterDungeonReq)
def handle_PlayerEnterDungeonReq(conn: Connection, msg: PlayerEnterDungeonReq):
    dungeon_data = resources.excels.dungeon_data[msg.dungeon_id]
    point_data = resources.binoutput.config_scene[3].points
    
    scene_id = dungeon_data.dungeon_id
    pos = point_data[msg.point_id].tranPos
    
    conn.send(conn.player.get_teleport_packet(scene_id, pos, EnterType.ENTER_DUNGEON))

    player_enter_dungeon = PlayerEnterDungeonRsp()
    player_enter_dungeon.retcode = 0
    player_enter_dungeon.point_id = msg.point_id
    player_enter_dungeon.dungeon_id = msg.dungeon_id
    conn.send(player_enter_dungeon)

    
    
    