from collections import defaultdict
import time
from pyglet.window import key


class KeyTracker(object):
    def __init__(self, delta=0.2, trackedKeys={key.LEFT, key.RIGHT}):
        super(KeyTracker, self).__init__()
        self.stack = []
        self.delta = delta
        self.handlers = {}
        self.trackedKeys = trackedKeys

    def register_default_double_key_handler(self, handler):
        self.register_double_key_handler('default', handler)

    def register_double_key_handler(self, symbol, handler):
        if isinstance(symbol, tuple):
            for s in symbol:
                self.register_double_key_handler(s, handler)
        else:
            handlers = self.handlers.get(symbol, [])
            handlers.append(handler)
            self.handlers[symbol] = handlers

    def track(self, symbol):
        now = time.time()

        if symbol not in self.trackedKeys:
            return

        self.stack.append((now, symbol))

        lastKeys = defaultdict(int)
        raisedKeys = set()
        for timing, symbol in self.stack[:]:
            if timing > time.time() - self.delta:
                counter = lastKeys[symbol]
                counter += 1
                lastKeys[symbol] = counter
                #TODO: call only once
                if lastKeys[symbol] > 1 and symbol not in raisedKeys:
                    self.__raise_double_key(symbol)
                    raisedKeys.add(symbol)
            else:
                self.stack.pop(0)

    def __call_key_handlers(self, symbol):
        handlers = self.handlers.get(symbol, [])
        if handlers:
            for handler in handlers:
                handler(symbol)

    def __raise_double_key(self, symbol):
        self.__call_key_handlers(symbol)
        self.__call_key_handlers('default')

