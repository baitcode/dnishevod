import cocos
from pyglet.window import key
from ground import Ground
from hero import Hero
import settings
from utils.key_tracker import KeyTracker
import Box2D as b2d

PIXELS_PER_METER = getattr(settings, 'PIXELS_PER_METER', 1)
WINDOW_HEIGHT = getattr(settings, 'WINDOW_HEIGHT', 100)


class Level(cocos.layer.Layer):
    def __init__(self):
        super(Level, self).__init__()

        self.is_event_handler = True
        self.keys = set()
        self.keyTracker = KeyTracker()
        self.keyTracker.register_double_key_handler(
            (key.LEFT, key.RIGHT),
            self.on_double_key_pressed
        )
        self.schedule(self.step)

        gravity = getattr(settings, 'GRAVITY', (0, 0))
        self.vel_iters = 6
        self.pos_iters = 6
        self.world = b2d.b2World(
            gravity=gravity,
            doSleep=True
        )

        self.hero = Hero(self.world, (5, 5), 0.5, 1, self)
        self.ground = Ground(self.world, self)
        self.add(self.hero)

    def on_double_key_pressed(self, symbol):
        self.hero.run()

    def get_direction_method(self):
        return (
            (key.RIGHT in self.keys) - (key.LEFT in self.keys),
            (key.UP in self.keys) - (key.DOWN in self.keys),
        )

    def on_key_press(self, symbol, modifiers):
        self.keyTracker.track(symbol)
        self.keys.add(symbol)
        vector = self.get_direction_method()
        self.hero.move(vector)

    def on_key_release(self, symbol, modifiers):
        self.keys.discard(symbol)
        vector = self.get_direction_method()
        self.hero.move(vector)

    def step(self, tick):
        self.world.Step(tick, self.vel_iters, self.pos_iters)
        self.world.ClearForces()
        self.hero.update_position()


class Game(object):
    def create_level(self):
        return Level()

    def create_debug(self):
        layer = cocos.layer.Layer()
        step = 0
        color = (20, 150, 20, 50)
        while step < settings.WINDOW_WIDTH:
            line = cocos.draw.Line(
                (step, 0), (step, settings.WINDOW_HEIGHT),
                color=color
            )
            layer.add(line)
            step += settings.PIXELS_PER_METER

        step = 0
        while step < settings.WINDOW_HEIGHT:
            line = cocos.draw.Line(
                (0, step),
                (settings.WINDOW_WIDTH, step),
                color=color
            )
            layer.add(line)
            step += settings.PIXELS_PER_METER
        return layer



    def __init__(self):
        cocos.director.director.init(
            width=getattr(settings, 'WINDOW_WIDTH', 100),
            height=getattr(settings, 'WINDOW_HEIGHT', 100)
        )
        self.level = cocos.scene.Scene(
            self.create_debug(),
            self.create_level()
        )

    def run(self):
        cocos.director.director.run(self.level)


