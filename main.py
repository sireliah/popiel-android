#!/usr/bin/python3

from functools import partial
import math
from random import randint, uniform

from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, DictProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window

# import kivent_core
from kivent_core.managers.resource_managers import texture_manager

from parallax_module.parallax import ParallaxSystem2D, ParallaxRenderer
from parallax_module.position import PositionShiftSystem2D

from init import InitMixin
from game_systems import PhysicsSystem, ParallaxShiftSystem
from settings import LEVEL_WIDTH, LEVEL_HEIGHT, MOUSE_LIFESPAN, MAX_MICE_NUM, DEBUG


Factory.register('ParallaxShiftSystem', cls=ParallaxShiftSystem)
Factory.register('PhysicsSystem', cls=PhysicsSystem)
texture_manager.load_atlas('data/assets/game_objects.atlas')
texture_manager.load_atlas('data/assets/character_objects.atlas')


class PopielGame(Widget, InitMixin):

    x_scope = NumericProperty(0)
    y_scope = NumericProperty(0)
    character_x = NumericProperty(0)
    character_y = NumericProperty(0)
    character_jump = BooleanProperty(False)
    character_entity_id = NumericProperty(None)
    mice_num = NumericProperty(0)
    best_result = DictProperty({'result': 0, 'instructions': []})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ground_level = 4.0
        self.move_speed = 0.5
        self.gameworld.init_gameworld(
            ['position', 'parallax_renderer', 'physics', 'camera1'],
            callback=self.init_game)

        Clock.schedule_interval(self.clock_callback, 0.1)
        Clock.schedule_interval(self.generate_mice, 3.0)
        Clock.schedule_interval(self.generate_mice, 4.4)

        if DEBUG:
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def init_game(self):
        self.setup_states()
        self.load_models()
        self.set_state()
        self.init_models()

    def setup_states(self):
        self.gameworld.add_state(
            state_name='main',
            systems_added=['position', 'parallax_renderer', 'physics', 'parallax'],
            systems_removed=[],
            systems_paused=[],
            systems_unpaused=['position', 'parallax_renderer', 'physics', 'parallax'],
            screenmanager_screen='main'
        )

    def set_state(self):
        self.gameworld.state = 'main'

    def load_models(self):
        model_manager = self.gameworld.model_manager

        textures = {
            'ground': (200.0, 200.0),
            'grass': (100.0, 100.0),
            'tree1': (700.0, 900.0),
            'mountains': (400.0, 100.0),
            'character1.1': (100.0, 200.0),
            'character1.2': (100.0, 200.0),
            'mouse1_l': (200.0, 50.0),
            'mouse1_r': (200.0, 50.0),
        }

        for model, size in textures.items():
            model_manager.load_textured_rectangle(
                'vertex_format_4f', size[0], size[1], model, '%s-4' % model
            )

    def apply_move(self, direction=None):
        if self.x_scope < 3.0 and self.x_scope > -3.0:
            if direction == 'left':
                self.x_scope += self.move_speed
            elif direction == 'right':
                self.x_scope -= self.move_speed

    def move(self, direction):
        self.apply_move(direction)

    def jump(self):
        self.character_jump = True

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.apply_move('left')
        elif keycode[1] == 'right':
            self.apply_move('right')
        if keycode[1] == 'spacebar':
            self.jump()
        if keycode[1] == 'm':
            self.generate_mice(1.0)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def init_models(self):
        init_entity = self.gameworld.init_entity
        self.init_model_serial('mountains', 400, 200, 220, 0.01, init_entity)
        self.init_model_serial('mountains', 400, 200, 200, 0.04, init_entity)
        self.init_model('tree1', 1500, 500, 300, 400, 0.8, init_entity)

        self.gameworld.entity_to_focus = self.character_entity_id
        self.init_model_serial('ground', 200, 100, 200, self.ground_level,
                               init_entity, y_callback=lambda x: math.degrees(math.sin(x / 4)) + 50)
        self.init_model_serial('grass', 100, 100, 100, self.ground_level,
                               init_entity, walkable=True, y_callback=lambda x: math.degrees(math.sin(x / 4)) + 150)

        self.init_model('grass', 1000, 500, 200, 50, self.ground_level,
                        init_entity, physics_active=True, walkable=True)
        self.init_model('grass', 1400, 500, 200, 50, self.ground_level,
                        init_entity, physics_active=True, walkable=True)

        self.init_model('grass', 600, 500, 200, 50, self.ground_level,
                        init_entity, physics_active=True, walkable=True)

        self.character_entity_id = self.init_model('character1.1', 400, 300, 100, 100,
                                                   self.ground_level, init_entity, physics_active=True)

        self.init_model('tree1', 700, 500, 700, 900, 6.0, init_entity)
        self.init_model('tree1', 2000, 400, 700, 900, 7.0, init_entity)

    def generate_mice(self, dt):
        if self.mice_num < MAX_MICE_NUM:

            best_result = self.best_result['result']
            number = randint(0, 10)
            if number == 10:
                best_instructions = []
                print("Random strategy!")
            else:
                best_instructions = self.best_result['instructions']
                print("Picking this one:", self.best_result['result'])
            entity_id = self.init_model_mouse('mouse1_l', 1900, 400, 200, 50, self.ground_level,
                                        best_instructions,
                                        self.gameworld.init_entity)
            # Count down the time to remove mouse entity.
            Clock.schedule_once(partial(self.remove_mouse, entity_id), MOUSE_LIFESPAN)

            self.mice_num += 1
            print("----------------", self.mice_num)

    def remove_mouse(self, entity_id, dt):
        self.mice_num -= 1
        return self.gameworld.timed_remove_entity(entity_id, dt)

    def update(self, dt):
        self.gameworld.update(dt)

    def clock_callback(self, dt):
        if self.x_scope > 0.2:
            self.x_scope /= 2.0
        elif self.x_scope < -0.2:
            self.x_scope /= 2.0 

        if self.x_scope < 0.2 and self.x_scope > -0.2:
             self.x_scope = 0
        self.character_jump = False


class PopielApp(App):

    def build(self):
        Window.clearcolor = (0, 0, 0, 1.0)


if __name__ == '__main__':
    PopielApp().run()
