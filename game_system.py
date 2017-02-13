
from kivent_core.systems.gamesystem import GameSystem


class ParallaxSystem(GameSystem):

    def update(self, dt):
        entities = self.gameworld.entities
        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                entity = entities[entity_id]
                pos_component = entity.position
                pos_component.x += self.x_scope * component.layer
                pos_component.y += self.y_scope
