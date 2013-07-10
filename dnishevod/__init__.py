import cocos
from cocos.actions import move_actions
from pyglet.window import key
from utils.key_tracker import KeyTracker


class Hero(cocos.sprite.Sprite):
    def __init__(self):
        super(Hero, self).__init__('assets/hero/img/hero.png', scale=0.2)
        self.is_mode_running = False
        self.velocity = (0, 0)
        self.horizontal_direction = 1
        self.walk_velocity = 120
        self.run_velocity = 180
        self.actions_applied = False

    def move(self, vector):
        self.is_mode_stopped = False

        horizontal_velocity = (
            self.walk_velocity + (self.run_velocity * self.is_mode_running)
        )
        vertical_velocity = self.walk_velocity
        self.velocity = (
            vector[0] * horizontal_velocity,
            vector[1] * vertical_velocity
        )

        if vector[0] and self.horizontal_direction != vector[0]:
            self.horizontal_direction = vector[0]
            self.turn()

        if vector[0] == 0 and vector[1] == 0:
            self.stop()

        if not self.actions_applied:
            self.do(move_actions.Move())
            self.actions_applied = True

    def turn(self):
        self.is_mode_running = False

    def stop(self):
        self.is_mode_running = False
        self.is_mode_stopped = True

    def run(self):
        self.is_mode_running = True


class Level(cocos.layer.Layer):

    def __init__(self):
        super(Level, self).__init__()
        self.is_event_handler = True
        self.hero = Hero()
        self.hero.position = 300, 300
        self.add(self.hero)
        self.keys = set()
        self.keyTracker = KeyTracker()
        self.keyTracker.register_double_key_handler(
            (key.LEFT, key.RIGHT),
            self.on_double_key_pressed
        )

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

    def on_enter(self):
        pass


class Game(object):
    def create_level(self):
        return Level()

    def __init__(self):
        self.level = cocos.scene.Scene(
            self.create_level()
        )

    def run(self):
        cocos.director.director.run(self.level)


cocos.director.director.init()
Game().run()