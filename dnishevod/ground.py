from . import settings
from .utils.debug import DebugMixin

PIXELS_PER_METER = getattr(settings, 'PIXELS_PER_METER', 1.0)
WINDOW_HEIGHT = getattr(settings, 'WINDOW_HEIGHT', 100)
WINDOW_WIDTH = getattr(settings, 'WINDOW_WIDTH', 100)


class Ground(DebugMixin):
    def __init__(self, world, parent):
        super(Ground, self).__init__()
        h_pos = float(WINDOW_WIDTH) / 2 / PIXELS_PER_METER

        self.body = world.CreateStaticBody(
            position=(h_pos, 0),
            userData=self,
            mass=50
        )
        self.body.CreatePolygonFixture(
            box=(
                float(WINDOW_WIDTH) / PIXELS_PER_METER,
                1
            )
        )
        self.lines = []
        self.drawDebugFixtures(parent)

    def update_position(self):
        self.x = self.body.position.x * PIXELS_PER_METER
        self.y = self.body.position.y * PIXELS_PER_METER
        self.updateDebugFixtures()

