
from settings import LEVEL_WIDTH, LEVEL_HEIGHT


class InitMixin(object):

    """
    Creating entities in the system.
    """

    @staticmethod
    def init_model_serial(texture, width, height, y, layer, init_entity_callback, walkable=False, y_callback=None):
        for x in range(0, LEVEL_WIDTH * (int(layer) + 1), width):
            if y_callback:
                y = y_callback(x)

            element = {
                'position': (x, y),
                'parallax': {'layer': layer},
                'renderer': {'texture': texture, 'model_key': '%s-4' % texture},
                'physics': {
                    'x': x, 'y': y, 'width': width, 'height': height,
                    'active': False, 'walkable': walkable
                },
            }
            init_entity_callback(element, ['position', 'renderer', 'parallax', 'physics'])

    @staticmethod
    def init_model(texture, x, y, width, height, layer, init_entity_callback, physics_active=False, walkable=False):

        element = {
            'position': (x, y),
            'parallax': {'layer': layer},
            'renderer': {'texture': texture, 'model_key': '%s-4' % texture},
            'physics': {
                'x': x, 'y': y, 'width': width, 'height': height,
                'active': physics_active, 'walkable': walkable
            },
        }
        return init_entity_callback(element, ['position', 'renderer', 'parallax', 'physics'])

    # TODO
    @staticmethod
    def init_character(texture, x, y, layer, init_entity_callback):
        element = {
            'position': (x, y),
            'parallax': {'layer': layer},
            'renderer': {'texture': texture, 'model_key': '%s-4' % texture},
            'physics': {'x': x, 'y': y, 'width': 100.0, 'height': 200.0, 'active': True},
        }
        return init_entity_callback(element, ['position', 'renderer', 'physics'])
