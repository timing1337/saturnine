from lib.proto import ProtEntityType

class World:
    next_entity_id: int = 0
    next_guid: int = 0

    def get_next_entity_id(self, type: ProtEntityType):
        self.next_entity_id += 1
        return (type << 24) + self.next_entity_id
    
    def get_next_guid(self):
        self.next_guid += 1
        return self.next_guid
