from game_server.protocol.cmd_id import CmdID
from game_server import HandlerRouter,Connection
from game_server.utils.time import current_milli_time
from lib.retcode import Retcode
from game_server.resource import resources
from lib.proto import Vector ,EnterType, DungeonEntryInfoReq, DungeonEntryInfoRsp, DungeonEntryInfo
import enet

router = HandlerRouter()
@router(CmdID.DungeonEntryInfoReq)
def handle_DungeonEntryInfo(conn: Connection, msg: DungeonEntryInfoReq):
    point_data = resources.binoutput.config_scene[3].points
    
    dungeon_entry_info_rsp = DungeonEntryInfoRsp()
    dungeon_entry_info_rsp.point_id = msg.point_id
    
    dungeon_entry_list = []
    
    rec = None
    
    for dungeonId in point_data[msg.point_id].dungeonIds:
        rec = dungeonId
        dungeon_info = DungeonEntryInfo()
        dungeon_info.dungeon_id = dungeonId
        dungeon_info.is_passed = True
        dungeon_info.left_times = current_milli_time()
        dungeon_info.start_time = current_milli_time() + 500
        dungeon_info.end_time = current_milli_time() + 1000
        dungeon_info.max_boss_chest_num = 2
        dungeon_info.boss_chest_num = 19000000
        dungeon_entry_list.append(dungeon_info)
    
    dungeon_entry_info_rsp.dungeon_entry_list = dungeon_entry_list
    dungeon_entry_info_rsp.recommend_dungeon_id = rec
    
    conn.send(dungeon_entry_info_rsp)
    
    
    