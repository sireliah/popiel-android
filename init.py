
import copy
from settings import LEVEL_WIDTH, LEVEL_HEIGHT


class InitMixin(object):

    """
    Creating entities in the system.
    """

    @staticmethod
    def init_model_m(texture, width, height, start_x, y, layer, init_entity_callback,
                     walkable=False, y_callback=None):
        for x in range(0, 5000, width):
            if y_callback:
                y = y_callback(x)

            element = {
                'position': (x, y, layer),
                'parallax': {'shift': layer},
                'parallax_renderer': {'texture': texture, 'model_key': '%s-4' % texture},
                'physics': {
                    'x': x, 'y': y, 'width': width, 'height': height,
                    'active': False, 'walkable': walkable, 'pawn': False
                },
            }
            init_entity_callback(element, ['position', 'parallax_renderer', 'physics', 'parallax'])

    @staticmethod
    def init_model_serial(texture, width, height, start_x, y, layer, init_entity_callback,
                          walkable=False, y_callback=None):
        for x in range(start_x, LEVEL_WIDTH * (int(layer) + 1), width):
            if y_callback:
                y = y_callback(x)

            element = {
                'position': (x, y, layer),
                'parallax': {'shift': layer},
                'parallax_renderer': {'texture': texture, 'model_key': '%s-4' % texture},
                'physics': {
                    'x': x, 'y': y, 'width': width, 'height': height,
                    'active': False, 'walkable': walkable, 'pawn': False
                },
            }
            init_entity_callback(element, ['position', 'parallax_renderer', 'physics', 'parallax'])

    @staticmethod
    def init_model(texture, x, y, width, height, layer, init_entity_callback,
                   physics_active=False, walkable=False, pawn=False):

        element = {
            'position': (x, y, layer),
            'parallax': {'shift': layer},
            'parallax_renderer': {'texture': texture, 'model_key': '%s-4' % texture},
            'physics': {
                'x': x, 'y': y, 'width': width, 'height': height,
                'active': physics_active, 'walkable': walkable, 'pawn': pawn
            },
        }
        return init_entity_callback(element, ['position', 'parallax_renderer', 'physics', 'parallax'])

    @staticmethod
    def init_model_mouse(texture, x, y, width, height, layer, best_instructions, init_entity_callback):

        element = {
            'position': (x, y, layer),
            'parallax': {'shift': layer},
            'parallax_renderer': {'texture': texture, 'model_key': '%s-4' % texture},
            'physics': {
                'x': x, 'y': y, 'width': width, 'height': height,
                'active': True, 'walkable': False, 'pawn': True,
                'instructions': [], 'best_instructions': copy.copy(list(reversed(best_instructions)))
            },
        }
        return init_entity_callback(element, ['position', 'parallax_renderer', 'physics', 'parallax'])

    @staticmethod
    def init_character(texture, x, y, layer, init_entity_callback):
        element = {
            'position': (x, y, layer),
            'parallax': {'shift': layer},
            'parallax_renderer': {'texture': texture, 'model_key': '%s-4' % texture},
            'physics': {
                'x': x, 'y': y, 'width': 100.0, 'height': 200.0, 'active': True, 'pawn': False
            },
        }
        return init_entity_callback(element, ['position', 'parallax_renderer', 'physics', 'parallax'])
