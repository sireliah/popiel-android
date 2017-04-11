
from kivent_core.systems.gamesystem import GameSystem

from settings import GRAVITY, JUMP_HEIGHT


class ParallaxSystem(GameSystem):

    """
    Drawing parallax effect.
    """

    def update(self, dt):
        entities = self.gameworld.entities
        character_x = 0
        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                entity = entities[entity_id]

                if entity.entity_id == self.character_entity_id:
                    character_x = entity.position.x

                if character_x >= 900 and character_x <= 1600:

                    pos_component = entity.position
                    pos_component.x += self.x_scope * component.layer
                    pos_component.y += self.y_scope * component.layer


class PhysicsSystem(GameSystem):

    """
    Handle collisions and gravity.
    """

    def character_motion(self, entity1):
        render_comp = entity1.renderer

        entity1.position.x -= self.x_scope / 10.0
        self.character_x = entity1.position.x

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

            if 'mouse' in entity1.renderer.texture_key:
                entity1.position.x -= 0.1

            # Gravity
            entity1.position.y -= GRAVITY

            # Whether entity is above a tile.
            ent2_left_margin = entity2.position.x - entity2.physics.width / 2.0
            ent2_right_margin = entity2.position.x + entity2.physics.width / 2.0

            if (entity1.position.x >= ent2_left_margin and entity1.position.x <= ent2_right_margin):

                if entity1.position.y <= entity2.position.y + 100.0:

                    # Collision
                    if entity1.position.y <= entity2.position.y:
                        entity1.position.x = ent2_right_margin

                    # On the top of the object
                    else:
                        entity1.position.y = entity2.position.y + 100.0

    def update(self, dt):
        entities = self.gameworld.entities
        components = self.components

        # TODO: optimize that.
        for component in [c for c in components if c and c.active]:
            entity1 = entities[component.entity_id]
            nearby_components = [
                c for c in components if c and c.walkable
                # and component.x >= c.x - c.width # and component.x <= c.x + c.width
            ]
            for component2 in nearby_components:
                entity2 = entities[component2.entity_id]

                if entity1 and entity2 and entity1 != entity2:
                    self.update_position(entity1, entity2)
