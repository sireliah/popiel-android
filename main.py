
from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window

import kivent_core
from kivent_core.managers.resource_managers import texture_manager

from game_system import VelocitySystem2D


Factory.register('VelocitySystem2D', cls=VelocitySystem2D)
texture_manager.load_atlas('data/assets/game_objects.atlas')


class PopielGame(Widget):

    level_width = 1000
    level_height = 600

    x_scope = 0
    y_scope = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gameworld.init_gameworld(
            ['renderer', 'position', 'velocity', 'camera1'], callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.load_models()
        self.set_state()
        self.draw_models()

    def setup_states(self):
        self.gameworld.add_state(
            state_name='main',
            systems_added=['renderer',],
            systems_removed=[],
            systems_paused=[],
            systems_unpaused=['renderer', 'velocity', ],
            screenmanager_screen='main'
        )

    def set_state(self):
        self.gameworld.state = 'main'

    def load_models(self):
        model_manager = self.gameworld.model_manager
        model_manager.load_textured_rectangle(
            'vertex_format_4f', 200.0, 100.0, 'grass', 'grass4')

    def on_touch_move(self, touch):
        (x, y) = touch.pos
        if x > 500:
            print('prawo')
            self.x_scope += 10
        elif x < 500:
            print('lewo')
            self.x_scope -= 10
        self.draw_models()

    def draw_models(self):
        game_view = self.gameworld.system_manager['camera1']
        x, y = int(-game_view.camera_pos[0]), int(-game_view.camera_pos[1])
        w, h = int(game_view.size[0] + x), int(game_view.size[1] + y)
        init_entity = self.gameworld.init_entity
        for pos in range(0, self.level_width, 200):
            element = {
                'position': (pos+self.x_scope, 100),
                'renderer': {'texture': 'grass', 'model_key': 'grass4'},
            }

            init_entity(element, ['position', 'renderer'])

    def update(self, dt):
        self.gameworld.update(dt)


class PopielApp(App):

    def build(self):
        Window.clearcolor = (0, 0, 0, 1.0)


if __name__ == '__main__':
    PopielApp().run()

