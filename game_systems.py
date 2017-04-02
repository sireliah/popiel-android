
from operator import attrgetter

from kivent_core.systems.gamesystem import GameSystem


class ParallaxSystem(GameSystem):

    """
    Drawing parallax effect.
    """

    def update(self, dt):
        entities = self.gameworld.entities
        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                entity = entities[entity_id]
                pos_component = entity.position
                pos_component.x += self.x_scope * component.layer
                pos_component.y += self.y_scope


class PhysicsSystem(GameSystem):

    """
    Handle collisions and gravity.
    """

    def update_position(self, entity1, entity2):
        if entity1.physics.active:
            entity1.position.y -= 0.1

            if (entity1.position.y < entity2.position.y) and \
               (entity1.position.x > entity2.position.x - entity2.physics.width / 2 and entity1.position.x < entity2.position.x + entity2.physics.width / 2):
                entity1.position.y = entity2.position.y
                if self.character_jump:
                    entity1.position.y = entity1.position.y + 200.0
                    self.character_jump = False

    def update(self, dt):
        entities = self.gameworld.entities
        components = self.components

        # TODO: optimize that.
        for component in components:
            entity1 = entities[component.entity_id]
            nearby_components = [c for c in components if component.x > c.width / 2 and component.x < c.x + c.width / 2]
            for component2 in nearby_components:
                entity2 = entities[component2.entity_id]

                if entity1 and entity2 and entity1 != entity2:
                    self.update_position(entity1, entity2)
