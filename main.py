
import math

from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window

# import kivent_core
from kivent_core.managers.resource_managers import texture_manager

from init import InitMixin
from game_systems import ParallaxSystem, PhysicsSystem
from settings import LEVEL_WIDTH, LEVEL_HEIGHT


Factory.register('ParallaxSystem', cls=ParallaxSystem)
Factory.register('PhysicsSystem', cls=PhysicsSystem)
texture_manager.load_atlas('data/assets/game_objects.atlas')
texture_manager.load_atlas('data/assets/character_objects.atlas')


class PopielGame(Widget, InitMixin):

    x_scope = NumericProperty(0)
    y_scope = NumericProperty(0)
    character_jump = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gameworld.init_gameworld(
            ['renderer', 'position', 'parallax', 'physics', 'camera1'],
            callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.load_models()
        self.set_state()
        self.init_models()

    def setup_states(self):
        self.gameworld.add_state(
            state_name='main',
            systems_added=['renderer', ],
            systems_removed=[],
            systems_paused=[],
            systems_unpaused=['renderer', 'parallax', 'physics'],
            screenmanager_screen='main'
        )

    def set_state(self):
        self.gameworld.state = 'main'

    def load_models(self):
        model_manager = self.gameworld.model_manager
        model_manager.load_textured_rectangle(
            'vertex_format_4f', 200.0, 100.0, 'ground', 'ground4')
        model_manager.load_textured_rectangle(
            'vertex_format_4f', 200.0, 100.0, 'grass', 'grass4')
        model_manager.load_textured_rectangle(
            'vertex_format_4f', 400.0, 100.0, 'mountains', 'mountains4')
        model_manager.load_textured_rectangle(
            'vertex_format_4f', 100.0, 200.0, 'character1', 'character14')

    def on_touch_down(self, touch):
        (x, y) = touch.pos
        if x > self.size[0] / 2:
            self.x_scope -= 1.0
        elif x < self.size[0] / 2:
            self.x_scope += 1.0

        if touch.is_double_tap:
            self.character_jump = True

    def init_models(self):
        init_entity = self.gameworld.init_entity

        self.init_model('mountains', 400, 100, 185, 1.0, init_entity)
        self.init_model('ground', 100, 100, 100, 4.0, init_entity, y_callback=lambda x: math.degrees(math.sin(x / 4)) + 50)
        self.init_model('grass', 100, 100, 100, 4.0, init_entity, y_callback=lambda x: math.degrees(math.sin(x / 4)) + 150)

        self.init_character('character1', 100, 1000, init_entity)

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
