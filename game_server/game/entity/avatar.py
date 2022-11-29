from lib.proto import AvatarInfo, Vector, ProtEntityType, SceneWeaponInfo, SceneAvatarInfo, SceneTeamAvatar
from game_server.game.world import World
from game_server.game.entity.entity import Entity

class AvatarEntity(Entity):

    avatar_info: AvatarInfo
    scene_weapon_info: SceneWeaponInfo
    
    def __init__(self, world: World, avatar_info: AvatarInfo, motion: Vector, rotation: Vector = Vector(0, 0, 0), speed: Vector = Vector(0, 0, 0)) -> None:
        self.avatar_info = avatar_info
        self.entity_id = world.get_next_entity_id(ProtEntityType.PROT_ENTITY_AVATAR)
        self.guid = avatar_info.guid
        self.scene_weapon_info = SceneWeaponInfo()
        self.scene_weapon_info.entity_id = world.get_next_entity_id(ProtEntityType.PROT_ENTITY_WEAPON)
        self.scene_weapon_info.item_id = 11406
        self.scene_weapon_info.level = 90
        self.scene_weapon_info.promote_level = 6
        self.scene_weapon_info.gadget_id = world.get_next_entity_id(ProtEntityType.PROT_ENTITY_GADGET)
        super().__init__(world, motion, rotation, speed)

    def get_scene_entity_info(self, uid: int):
        scene_entity_info = super().get_scene_entity_info()
        scene_entity_info.entity_type = ProtEntityType.PROT_ENTITY_AVATAR
        scene_entity_info.prop_map = self.avatar_info.prop_map
        scene_entity_info.fight_prop_map = self.avatar_info.fight_prop_map
        scene_entity_info.avatar = self.get_scene_avatar_info(uid)
        return scene_entity_info

    def get_scene_avatar_info(self, uid: int): 
        scene_avatar_info = SceneAvatarInfo()
        scene_avatar_info.guid = self.guid
        scene_avatar_info.uid = uid
        scene_avatar_info.inherent_proud_skill_list = self.avatar_info.inherent_proud_skill_list
        scene_avatar_info.proud_skill_extra_level_map = self.avatar_info.proud_skill_extra_level_map
        scene_avatar_info.skill_level_map = self.avatar_info.skill_level_map
        scene_avatar_info.talent_id_list = self.avatar_info.talent_id_list
        scene_avatar_info.core_proud_skill_level = self.avatar_info.core_proud_skill_level
        scene_avatar_info.skill_depot_id = self.avatar_info.skill_depot_id
        scene_avatar_info.avatar_id = self.avatar_info.avatar_id
        scene_avatar_info.peer_id = 1
        scene_avatar_info.equip_id_list = [11406]
        scene_avatar_info.weapon = self.scene_weapon_info
        return scene_avatar_info
