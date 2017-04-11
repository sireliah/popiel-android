from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.widget import Widget


class ControlPanel(Widget):

    pass


class DebugPanel(Widget):

    fps = StringProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.update_fps)

    def update_fps(self, dt):
        self.fps = '%s' % int(Clock.get_fps())
        Clock.schedule_once(self.update_fps, 0.05)
