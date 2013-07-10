import cocos
from .utils.debug import DebugMixin
import settings
from cocos.actions import move_actions

PIXELS_PER_METER = getattr(settings, 'PIXELS_PER_METER', 1.0)
WINDOW_HEIGHT = getattr(settings, 'WINDOW_HEIGHT', 100)
WINDOW_WIDTH = getattr(settings, 'WINDOW_WIDTH', 100)


class Hero(cocos.sprite.Sprite, DebugMixin):
    def __init__(self, world, position, parent):
        super(Hero, self).__init__(
            'dnishevod/assets/hero/img/hero.png',
            scale=0.2
        )
        self.is_mode_running = False
        self.force = (0, 0)
        self.horizontal_direction = 1
        self.walk_velocity = 1200
        self.run_velocity = 1800
        self.actions_applied = False
        self.body = world.CreateDynamicBody(
            position=position,
            userData=self,
            mass=50,
        )
        self.body.CreatePolygonFixture(
            box=(0.5, 0.58),
            friction=15
        )
        self.lines = []
        self.drawDebugFixtures(parent)

    def move(self, vector):
        self.is_mode_stopped = False

        horizontal_force = (
            self.walk_velocity + (self.run_velocity * self.is_mode_running)
        )
        self.force = (
            vector[0] * horizontal_force,
            0,
        )
        if vector[0] and self.horizontal_direction != vector[0]:
            self.horizontal_direction = vector[0]
            self.turn()

        if vector[0] == 0 and vector[1] == 0:
            self.stop()

    def turn(self):
        self.is_mode_running = False

    def stop(self):
        self.is_mode_running = False
        self.is_mode_stopped = True

    def run(self):
        self.is_mode_running = True

    def update_position(self):
        self.body.ApplyForceToCenter(self.force, True)
        self.x = self.body.position.x * PIXELS_PER_METER
        self.y = self.body.position.y * PIXELS_PER_METER
        self.updateDebugFixtures()
