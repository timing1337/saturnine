from lib.proto import Vector,EnterType,PlayerEnterSceneNotify
from game_server.utils.time import current_milli_time
from game_server.resource.enums import PropType
from game_server.game.world import World
import dataclasses

@dataclasses.dataclass()
class Player:
    uid: int
    name: str
    avatar_id: int = 10000007
    world: World = World()

    scene_id: int = 0
    pos: Vector = dataclasses.field(default_factory=Vector)

    prop_map: dict[PropType, int] = dataclasses.field(default_factory=dict)

    def get_teleport_packet(self, scene_id: int, pos: Vector, enter_type: EnterType = EnterType.ENTER_SELF):
        player_enter_scene_notify = PlayerEnterSceneNotify()
        player_enter_scene_notify.scene_id = scene_id
        player_enter_scene_notify.pos = pos
        player_enter_scene_notify.scene_begin_time = current_milli_time()
        player_enter_scene_notify.type = enter_type
        player_enter_scene_notify.enter_scene_token = 1000
        player_enter_scene_notify.world_level = 8
        player_enter_scene_notify.target_uid = self.uid
        return player_enter_scene_notify
        