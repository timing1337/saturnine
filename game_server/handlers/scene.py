from game_server.protocol.cmd_id import CmdID
from game_server import HandlerRouter,Connection
from lib.proto import TeamEnterSceneInfo, EnterSceneDoneReq, EnterWorldAreaReq,SceneGetAreaExplorePercentReq,SceneGetAreaExplorePercentRsp, EnterWorldAreaRsp, ScenePlayerLocationNotify, PlayerLocationInfo, VisionType, SceneEntityAppearNotify, SceneTeamAvatar, MpDisplayCurAvatar,AvatarEnterSceneInfo, SceneTeamUpdateNotify, ProtEntityType, AbilitySyncStateInfo, MpLevelEntityInfo,EnterSceneReadyReq,EnterScenePeerNotify,SceneInitFinishReq,MpSettingType,WorldDataNotify,PropValue,HostPlayerNotify,PlayerGameTimeNotify,SceneTimeNotify,SceneDataNotify,WorldPlayerInfoNotify,OnlinePlayerInfo,ScenePlayerInfoNotify,ScenePlayerInfo,PlayerEnterSceneInfoNotify,SceneInitFinishRsp,GetScenePointReq, GetSceneAreaReq,GetScenePointRsp,GetSceneAreaRsp,SceneForceUnlockNotify,SceneInitFinishRsp,EnterSceneDoneRsp,EnterType,PostEnterSceneReq,PostEnterSceneRsp
from lib.retcode import Retcode
from game_server.protocol.reader import BinaryReader
from game_server.resource.enums import PropType
import enet

router = HandlerRouter()

@router(CmdID.EnterSceneReadyReq)
def handle_scene_ready(conn: Connection, msg: EnterSceneReadyReq):
    enter_scene_peer_notify = EnterScenePeerNotify()
    enter_scene_peer_notify.peer_id = 1
    enter_scene_peer_notify.host_peer_id = 1
    enter_scene_peer_notify.dest_scene_id = conn.player.scene_id
    conn.send(enter_scene_peer_notify)

@router(CmdID.SceneInitFinishReq)
def handle_scene_init(conn: Connection, msg: SceneInitFinishReq):

    online_player_info = OnlinePlayerInfo(
        uid=conn.player.uid, 
        nickname=conn.player.name, 
        player_level=conn.player.prop_map[PropType.PROP_PLAYER_LEVEL],
        avatar_id=conn.player.avatar_id,
        mp_setting_type=MpSettingType.MP_SETTING_NO_ENTER,
        cur_player_num_in_world=1,
        world_level=8
    )

    world_data_notify = WorldDataNotify()
    world_data_notify.world_prop_map = {
        1: PropValue(1, ival=8),
        2: PropValue(2, ival=0)
    }

    host_player_notify = HostPlayerNotify()
    host_player_notify.host_uid = conn.player.uid
    host_player_notify.host_peer_id = 1

    player_game_time_notify = PlayerGameTimeNotify()
    player_game_time_notify.game_time = 0
    player_game_time_notify.uid = conn.player.uid

    scene_time_notify = SceneTimeNotify()
    scene_time_notify.scene_id = conn.player.scene_id
    scene_time_notify.scene_time = 0
    scene_time_notify.is_paused = False

    scene_data_notify = SceneDataNotify()
    scene_data_notify.level_config_name_list = ["Level_BigWorld"]

    world_player_info_notify = WorldPlayerInfoNotify()
    world_player_info_notify.player_info_list = [online_player_info]
    world_player_info_notify.player_uid_list = [conn.player.uid]

    scene_player_info_notify = ScenePlayerInfoNotify()
    scene_player_info_notify.player_info_list = [ScenePlayerInfo(
        uid=conn.player.uid, 
        peer_id=1,
        name=conn.player.name,
        is_connected=True,
        scene_id=conn.player.scene_id,
        online_player_info=online_player_info
    )]

    cur_avatar = conn.player.get_cur_avatar()
    scene_team_update_notify = SceneTeamUpdateNotify(scene_team_avatar_list=[], display_cur_avatar_list=[], is_in_mp=False)
    enter_scene_info_notify = PlayerEnterSceneInfoNotify()
    enter_scene_info_notify.cur_avatar_entity_id = cur_avatar.entity_id
    enter_scene_info_notify.team_enter_info = TeamEnterSceneInfo(team_entity_id=conn.player.world.get_next_entity_id(ProtEntityType.PROT_ENTITY_TEAM), team_ability_info=AbilitySyncStateInfo())
    enter_scene_info_notify.mp_level_entity_info = MpLevelEntityInfo(entity_id=conn.player.world.get_next_entity_id(ProtEntityType.PROT_ENTITY_MP_LEVEL), authority_peer_id=1, ability_info=AbilitySyncStateInfo())

    for avatar_guid in conn.player.teams[conn.player.cur_avatar_team_id].avatar_guid_list:
        avatar = conn.player.get_avatar_by_guid(avatar_guid)
        avatar.scene_weapon_info.guid = conn.player.get_next_guid()
        scene_team_avatar = SceneTeamAvatar()
        scene_team_avatar.scene_id = conn.player.scene_id
        scene_team_avatar.player_uid = conn.player.uid
        scene_team_avatar.avatar_guid = avatar.guid
        scene_team_avatar.entity_id = avatar.entity_id
        scene_team_avatar.avatar_info = avatar.avatar_info

        scene_team_update_notify.scene_team_avatar_list.append(scene_team_avatar)
        enter_scene_info_notify.avatar_enter_info.append(AvatarEnterSceneInfo(
            avatar_guid=avatar.guid,
            avatar_entity_id=avatar.entity_id,
            weapon_guid=avatar.scene_weapon_info.guid,
            weapon_entity_id=avatar.scene_weapon_info.entity_id
        ))

    conn.send(world_data_notify)
    conn.send(scene_data_notify)
    conn.send(host_player_notify)
    conn.send(player_game_time_notify)
    conn.send(scene_time_notify)
    conn.send(world_player_info_notify)
    conn.send(scene_player_info_notify)
    conn.send(scene_team_update_notify)
    conn.send(enter_scene_info_notify)

@router(CmdID.GetScenePointReq)
def handle_scene_point(conn: Connection, msg: GetScenePointReq):
    rsp = GetScenePointRsp()
    rsp.scene_id = msg.scene_id
    rsp.unlocked_point_list = []
    rsp.unlock_area_list = []
    for x in range(200):
        rsp.unlock_area_list.append(x)
        rsp.unlocked_point_list.append(x)
    conn.send(rsp)

@router(CmdID.GetSceneAreaReq)
def handle_scene_area(conn: Connection, msg: GetSceneAreaReq):
    rsp = GetSceneAreaRsp()
    rsp.scene_id = msg.scene_id
    rsp.area_id_list = []
    for x in range(200):
        rsp.area_id_list.append(x)
    conn.send(rsp)

@router(CmdID.EnterSceneDoneReq)
def handle_scene_done(conn: Connection, msg: EnterSceneDoneReq):
    cur_avatar = conn.player.get_cur_avatar()
    conn.player.get_cur_avatar().motion = conn.player.pos
    scene_entity_appear_notify = SceneEntityAppearNotify()
    scene_entity_appear_notify.appear_type = VisionType.VISION_NONE
    scene_entity_appear_notify.entity_list = [cur_avatar.get_scene_entity_info(conn.player.uid)]

    scene_player_location_notify = ScenePlayerLocationNotify()
    scene_player_location_notify.scene_id = conn.player.scene_id
    scene_player_location_notify.player_loc_list = [
        PlayerLocationInfo(uid=conn.player.uid, pos=cur_avatar.motion, rot=cur_avatar.rotation)
    ]

    conn.send(scene_entity_appear_notify)
    conn.send(scene_player_location_notify)
    conn.send(EnterSceneDoneRsp(retcode=0))

@router(CmdID.PostEnterSceneReq)
def handle_enter_world(conn: Connection, msg: PostEnterSceneReq):
    conn.send(PostEnterSceneRsp(retcode=0))


@router(CmdID.EnterWorldAreaReq)
def handle_enter_world(conn: Connection, msg: EnterWorldAreaReq):
    rsp = EnterWorldAreaRsp()
    rsp.area_id = msg.area_id
    rsp.area_type = msg.area_type
    conn.send(rsp)

@router(CmdID.SceneGetAreaExplorePercentReq)
def area_explore_percent_handle(conn: Connection, msg: SceneGetAreaExplorePercentReq): 
    rsp = SceneGetAreaExplorePercentRsp()
    rsp.area_id = msg.area_id
    rsp.explore_percent = 100
    conn.send(rsp)