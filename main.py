
from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window

import kivent_core
from kivent_core.managers.resource_managers import texture_manager

from game_system import ParallaxSystem


Factory.register('ParallaxSystem', cls=ParallaxSystem)
texture_manager.load_atlas('data/assets/game_objects.atlas')


class PopielGame(Widget):

    level_width = 1000
    level_height = 600
    x_scope = NumericProperty(0)
    y_scope = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gameworld.init_gameworld(
            ['renderer', 'position', 'parallax', 'camera1'],
            callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.load_models()
        self.set_state()
        self.draw_models()

    def setup_states(self):
        self.gameworld.add_state(
            state_name='main',
            systems_added=['renderer', ],
            systems_removed=[],
            systems_paused=[],
            systems_unpaused=['renderer', 'parallax', ],
            screenmanager_screen='main'
        )

    def set_state(self):
        self.gameworld.state = 'main'

    def load_models(self):
        model_manager = self.gameworld.model_manager
        model_manager.load_textured_rectangle(
            'vertex_format_4f', 200.0, 100.0, 'grass', 'grass4')
        model_manager.load_textured_rectangle(
            'vertex_format_4f', 400.0, 100.0, 'mountains', 'mountains4')

    def on_touch_down(self, touch):
        (x, y) = touch.pos
        if x > 500:
            print('prawo')
            self.x_scope += 1
        elif x < 500:
            print('lewo')
            self.x_scope -= 1

    def draw_models(self):
        init_entity = self.gameworld.init_entity
        for pos in range(0, self.level_width, 400):
            element = {
                'position': (pos, 185),
                'parallax': {'layer': 1.0},
                'renderer': {'texture': 'mountains', 'model_key': 'mountains4'},
            }

            init_entity(element, ['position', 'renderer', 'parallax'])

        for pos in range(0, self.level_width*2, 200):
            element = {
                'position': (pos, 100),
                'parallax': {'layer': 4.0},
                'renderer': {'texture': 'grass', 'model_key': 'grass4'},
            }

            init_entity(element, ['position', 'renderer', 'parallax'])

    def update(self, dt):
        self.gameworld.update(dt)


class DebugPanel(Widget):

    fps = StringProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.update_fps)

    def update_fps(self, dt):
        self.fps = "%s" % int(Clock.get_fps())
        Clock.schedule_once(self.update_fps, 0.05)


class PopielApp(App):

    def build(self):
        Window.clearcolor = (0, 0, 0, 1.0)


if __name__ == '__main__':
    PopielApp().run()
