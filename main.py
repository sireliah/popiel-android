#!/usr/bin/python3

from functools import partial
import math
from random import randint

from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window

# import kivent_core
from kivent_core.managers.resource_managers import texture_manager

from init import InitMixin
from game_systems import PhysicsSystem, ParallaxSystem
from settings import LEVEL_WIDTH, LEVEL_HEIGHT, MOUSE_LIFESPAN


Factory.register('ParallaxSystem', cls=ParallaxSystem)
Factory.register('PhysicsSystem', cls=PhysicsSystem)
texture_manager.load_atlas('data/assets/game_objects.atlas')
texture_manager.load_atlas('data/assets/character_objects.atlas')


class PopielGame(Widget, InitMixin):

    # Scopes determine how whole level is moving together.
    x_scope = NumericProperty(0)
    y_scope = NumericProperty(0)
    character_x = NumericProperty(0)
    character_jump = BooleanProperty(False)
    character_entity_id = NumericProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gameworld.init_gameworld(
            ['renderer', 'position', 'physics', 'camera1'],
            callback=self.init_game)

        Clock.schedule_interval(self.clock_callback, 0.5)
        Clock.schedule_interval(self.generate_mice, 3.0)
        Clock.schedule_interval(self.generate_mice, 4.4)

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
            systems_unpaused=['renderer', 'parallax', 'physics', ],
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
            'mouse1': (200.0, 50.0),
        }

        for model, size in textures.items():
            model_manager.load_textured_rectangle(
                'vertex_format_4f', size[0], size[1], model, '%s-4' % model
            )

    def move(self, direction):
        if direction == 'left':
            self.x_scope += 0.5
        elif direction == 'right':
            self.x_scope -= 0.5

    def jump(self):
        self.character_jump = True

    def init_models(self):
        init_entity = self.gameworld.init_entity
        self.init_model_serial('mountains', 400, 200, 220, 1.05, init_entity)
        self.init_model_serial('mountains', 400, 200, 200, 1.1, init_entity)
        self.init_model('tree1', 1500, 500, 300, 400, 3.0, init_entity)
        self.init_model('mouse1', 2000, 400, 200, 50, 4.0, init_entity, physics_active=True)

        self.character_entity_id = self.init_model('character1.1', 700, 100, 100, 100, 4.0, init_entity, physics_active=True)

        self.gameworld.entity_to_focus = self.character_entity_id
        self.init_model_serial('ground', 200, 100, 200, 4.0, init_entity, y_callback=lambda x: math.degrees(math.sin(x / 4)) + 50)
        self.init_model_serial('grass', 100, 100, 100, 4.0, init_entity, walkable=True, y_callback=lambda x: math.degrees(math.sin(x / 4)) + 150)
        self.init_model('grass', 200, 400, 200, 50, 4.0, init_entity, physics_active=True, walkable=True)

        self.init_model('grass', 700, 400, 200, 50, 4.0, init_entity, physics_active=True, walkable=True)


        self.init_model('tree1', 700, 500, 700, 900, 7.0, init_entity)
        self.init_model('tree1', 2000, 400, 700, 900, 7.0, init_entity)

    def generate_mice(self, dt):
        entity_id = self.init_model('mouse1', randint(1000, 2000), 400, 200, 50, 4.0, self.gameworld.init_entity, physics_active=True)

        # Count down the time to remove mouse entity.
        Clock.schedule_once(partial(self.gameworld.timed_remove_entity, entity_id), MOUSE_LIFESPAN)

    def update(self, dt):
        self.gameworld.update(dt)

    def clock_callback(self, dt):
        if self.x_scope > 0.5:
            self.x_scope -= 0.2
        elif self.x_scope < -0.5:
            self.x_scope += 0.2
        elif self.x_scope < 1.0 and self.x_scope > -1.0:
            self.x_scope = 0
        self.character_jump = False


class PopielApp(App):

    def build(self):
        Window.clearcolor = (0, 0, 0, 1.0)


if __name__ == '__main__':
    PopielApp().run()
