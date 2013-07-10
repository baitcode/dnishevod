from .. import settings
from cocos.draw import Line

PIXELS_PER_METER = getattr(settings, 'PIXELS_PER_METER', 1.0)
WINDOW_HEIGHT = getattr(settings, 'WINDOW_HEIGHT', 100)
WINDOW_WIDTH = getattr(settings, 'WINDOW_WIDTH', 100)


class DebugMixin(object):
    def drawDebugFixtures(self, parent):
        for fixture in self.body:
            shape = fixture.shape
            vertices = shape.vertices
            ppm = PIXELS_PER_METER
            vertices = [(self.body.transform * v) * ppm for v in vertices]
            for i in range(-1, len(vertices) - 1):
                line = Line(vertices[i], vertices[i + 1], (255, 255, 255, 255))
                self.lines.append(line)
                parent.add(line)

    def updateDebugFixtures(self):
        for fixture in self.body:
            shape = fixture.shape
            vertices = shape.vertices
            ppm = PIXELS_PER_METER
            vertices = [(self.body.transform * v) * ppm for v in vertices]
            for i in range(-1, len(vertices) - 1):
                self.lines[i + 1].start = vertices[i]
                self.lines[i + 1].end = vertices[i + 1]
