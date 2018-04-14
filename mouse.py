from functools import partial
from random import randint, uniform
from settings import MOUSE_SIGHT
from kivy.clock import Clock


class Mouse(object):

    def mouse_move(self, entity):

        dist_to_character = abs(entity.position.x - self.character_x)

        if len(entity.physics.best_instructions) > 1 and dist_to_character > MOUSE_SIGHT:
            step = entity.physics.best_instructions.pop()
            x_vector = step['x']
            y_vector = step['y']

        else:
            x_vector = self.point_to_character(entity)

            # Jump
            random_int = randint(0, 50000)
            y_vector = 0
            if random_int > 49899:
                y_vector = uniform(0.2, 40.0)

        entity.position.y += y_vector
        entity.position.x += x_vector

        if x_vector < 0:
            entity.parallax_renderer.texture_key = 'mouse1_l'
        else:
            entity.parallax_renderer.texture_key = 'mouse1_r'

        entity.physics.instructions.append({"x": x_vector, "y": y_vector})

        self.save_best_result(entity)

    def point_to_character(self, entity):

        movement_amount = 0.1

        if entity.position.x > self.character_x:
            return -movement_amount - 0.05
        elif entity.position.x < self.character_x:
            return movement_amount + 0.05
        else:
            return 0

    def save_best_result(self, entity):
        result = 1 / entity.position.x * (len(entity.physics.instructions) + 1)

        numer = randint(0, 10000)
        if result > self.best_result['result'] and numer > 9999:

            #Clock.schedule_once(partial(self.save, result, entity.physics.instructions), 1)
            self.save(result, entity.physics.instructions)

    def save(self, result, instructions):
        self.best_result['result'] = result
        self.best_result['instructions'] = instructions
