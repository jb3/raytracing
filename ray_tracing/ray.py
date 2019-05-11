import math

from .shapes import Line, Point2D


class Ray:
    def __init__(self, pos, heading):
        self.pos = pos
        self.heading = heading

        self.end = self.recalculate_end_point()

        self.line = Line(self.pos, self.end)

        self.u = None
        self.t = None

        self.target_colour = None

    def __repr__(self):
        return f"Ray(heading={self.heading}, u={self.u}, t={self.t}, distance={self.end.distance(self.pos)})"

    def draw(self):
        self.line.draw()

    def recalculate_end_point(self):
        heading_rads = math.radians(self.heading)

        new_x = self.pos.x + 1000 * math.cos(heading_rads)
        new_y = self.pos.y + 1000 * math.sin(heading_rads)

        return Point2D(new_x, new_y)

    def test_for_intersection(self, line):
        x1 = line.a.x
        y1 = line.a.y
        x2 = line.b.x
        y2 = line.b.y

        x3 = self.pos.x
        y3 = self.pos.y
        x4 = self.end.x
        y4 = self.end.y

        denominator = ((x1 - x2) * (y3 - y4)) - (
            (y1 - y2) * (x3 - x4)
        )

        if denominator == 0:
            return

        t = (
            ((x1 - x3) * (y3 - y4)) - ((y1 - y3) * (x3 - x4))
        ) / denominator
        u = -(
            (((x1 - x2) * (y1 - y3)) - ((y1 - y2) * (x1 - x3)))
            / denominator
        )

        if u < 0:
            return

        if not 0 < t < 1:
            return

        intersection_point = Point2D.from_tuple(
            ((x1 + ((x2 - x1) * t)), (y1 + ((y2 - y1) * t)))
        )

        if self.pos.distance(intersection_point) > self.pos.distance(
            self.end
        ):
            return

        self.u = u
        self.t = t

        self.end = intersection_point
        self.line = Line(self.pos, intersection_point)
        self.target_colour = line.colour
