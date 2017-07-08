
from kivent_core.systems.gamesystem import GameSystem

from settings import GRAVITY, JUMP_HEIGHT

from mouse import Mouse


class ParallaxShiftSystem(GameSystem):

    """
    Drawing parallax effect.
    """
    def update(self, dt):
        entities = self.gameworld.entities
        gameview = self.gameworld.system_manager['camera1']
        for component in self.components:
            if component is not None:
                entity_id = component.entity_id
                entity = entities[entity_id]

                entity.position.shift = (gameview.camera_pos[0] + 0.001) * entity.parallax.shift


class PhysicsSystem(GameSystem, Mouse):

    """
    Handle collisions and gravity.
    """

    def character_motion(self, entity1):
        render_comp = entity1.parallax_renderer

        entity1.position.x -= self.x_scope / 10.0
        self.character_x = entity1.position.x
        self.character_y = entity1.position.y

        if self.x_scope <= 0:
            render_comp.texture_key = 'character1.1'
        else:
            render_comp.texture_key = 'character1.2'

        if self.character_jump:
            entity1.position.y = entity1.position.y + JUMP_HEIGHT
            self.character_jump = False

        gameview = self.gameworld.system_manager['camera1']

        gameview.camera_pos[0] = (-entity1.position.x + 1000) / 5

    def update_position(self, entity1, entity2):

        if entity1.physics.active and entity2.physics.walkable:

            if entity1.entity_id == self.character_entity_id:
                self.character_motion(entity1)

            if 'mouse' in entity1.parallax_renderer.texture_key:
                self.mouse_move(entity1)

            # Gravity
            entity1.position.y -= GRAVITY

            # Whether entity is above a tile.
            ent2_left_margin = entity2.position.x - entity2.physics.width / 2.0
            ent2_right_margin = entity2.position.x + entity2.physics.width / 2.0

            if (entity1.position.x >= ent2_left_margin and entity1.position.x <= ent2_right_margin):

                if entity1.position.y <= entity2.position.y + 100.0:

                    # Collision
                    if entity1.position.y < entity2.position.y:
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
