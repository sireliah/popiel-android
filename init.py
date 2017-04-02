
from settings import LEVEL_WIDTH, LEVEL_HEIGHT


class InitMixin(object):

    @staticmethod
    def init_model(texture, width, height, y, layer, init_entity_callback, y_callback=None):
        for x in range(0, LEVEL_WIDTH * int(layer), width):
            if y_callback:
                y = y_callback(x)

            element = {
                'position': (x, y),
                'parallax': {'layer': layer},
                'renderer': {'texture': texture, 'model_key': '%s4' % texture},
                'physics': {'x': x, 'y': y, 'width': width, 'height': height, 'active': False},

            }
            init_entity_callback(element, ['position', 'renderer', 'parallax', 'physics'])

    @staticmethod
    def init_character(texture, x, y, init_entity_callback):
        element = {
            'position': (x, y),
            'renderer': {'texture': texture, 'model_key': '%s4' % texture},
            'physics': {'x': x, 'y': y, 'width': 100.0, 'height': 200.0, 'active': True},
        }
        init_entity_callback(element, ['position', 'renderer', 'physics'])
