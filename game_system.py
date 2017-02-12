
from kivent_core.systems.gamesystem import GameSystem


class VelocitySystem2D(GameSystem):

    def update(self, dt):
        entities = self.gameworld.entities
        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                entity = entities[entity_id]
                pos_component = entity.position
                pos_component.x += component.vx * dt
                pos_component.y += component.vy * dt
