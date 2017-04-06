
from operator import attrgetter

from kivent_core.systems.gamesystem import GameSystem

from settings import JUMP_HEIGHT


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
                pos_component.y += self.y_scope * component.layer


class PhysicsSystem(GameSystem):

    """
    Handle collisions and gravity.
    """

    def character_motion(self, entity1):
        render_comp = entity1.renderer

        entity1.position.x -= self.x_scope / 10

        if self.x_scope <= 0:
            render_comp.texture_key = 'character1.1'
        else:
            render_comp.texture_key = 'character1.2'

        if self.character_jump:
            entity1.position.y = entity1.position.y + JUMP_HEIGHT
            self.character_jump = False

    def update_position(self, entity1, entity2):

        if entity1.physics.active and entity2.physics.walkable:

            if entity1.entity_id == self.character_entity_id:
                self.character_motion(entity1)

            # Gravity
            entity1.position.y -= 0.2

            ent2_left_margin = entity2.position.x - entity2.physics.width / 2
            ent2_right_margin = entity2.position.x + entity2.physics.width / 2

            if (entity1.position.y < entity2.position.y) and \
               (entity1.position.x > ent2_left_margin and entity1.position.x < ent2_right_margin):
                entity1.position.y = entity2.position.y

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
