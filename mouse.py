
from random import randint, uniform


class Mouse(object):

    def mouse_move(self, entity):
        move_vector = self.point_to_character(entity)
        entity.position.x += move_vector

        if move_vector < 0:
            entity.parallax_renderer.texture_key = 'mouse1_l'
        else:
            entity.parallax_renderer.texture_key = 'mouse1_r'

        random_int = randint(0, 10000)
        if random_int > 9999:
            entity.position.y += uniform(0.2, 10.0)

    def point_to_character(self, entity):

        movement_amount = 0.1

        if entity.position.x > self.character_x:
            return -movement_amount - 0.05
        elif entity.position.x < self.character_x:
            return movement_amount + 0.05
        else:
            return 0
