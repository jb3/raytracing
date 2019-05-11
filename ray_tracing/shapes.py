import math

import pyglet


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def midpoint(self, other):
        mid_x = (self.x + other.x) / 2
        mid_y = (self.y + other.y) / 2

        return Point2D(mid_x, mid_y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def to_tuple(self):
        return self.x, self.y

    @classmethod
    def from_tuple(cls, points):
        return cls(points[0], points[1])

    def distance(self, other):
        return math.sqrt(
            (other.x - self.x) ** 2 + (other.y - self.y) ** 2
        )


class Triangle:
    def __init__(self, x, y, w, h):
        self.set(x, y, w, h)

    def draw(self):
        pyglet.graphics.vertex_list(3, self._tris).draw(
            pyglet.gl.GL_TRIANGLES
        )

    def set(self, x=None, y=None, w=None, h=None):
        self._x = self._x if x is None else x
        self._y = self._y if y is None else y
        self._w = self._w if w is None else w
        self._h = self._h if h is None else h
        self._tris = (
            "v2f",
            (
                self._x - (self._w / 2),
                self._y,
                self._x + (self._w / 2),
                self._y,
                self._x,
                self._y + self._h,
            ),
        )

    def move(self, magnitude, heading):
        heading_rads = math.radians(heading)

        x_points = self._tris[1][::2]
        y_points = self._tris[1][1::2]

        points = list(
            map(Point2D.from_tuple, zip(x_points, y_points))
        )

        translated = []

        for point in points:
            new_x = point.x + magnitude * math.cos(heading_rads)
            new_y = point.y + magnitude * math.sin(heading_rads)
            translated.append(new_x)
            translated.append(new_y)

        self._tris = ("v2f", tuple(translated))
        bottom_left = translated[0], translated[1]
        bottom_right = translated[2], translated[3]

        new_pos = Point2D.from_tuple(bottom_left).midpoint(
            Point2D.from_tuple(bottom_right)
        )

        self._x = new_pos.x
        self._y = new_pos.y

    def rotate(self, a):
        x_points = self._tris[1][::2]
        y_points = self._tris[1][1::2]

        points = list(
            map(Point2D.from_tuple, zip(x_points, y_points))
        )

        centre_x = sum(x_points) / 3
        centre_y = sum(y_points) / 3
        centre = Point2D(centre_x, centre_y)

        rotated = []
        angle = a * (math.pi / 180)

        for point in points:
            rotated_x = (
                math.cos(angle) * (point.x - centre.x)
                - math.sin(angle) * (point.y - centre.y)
                + centre.x
            )
            rotated_y = (
                math.sin(angle) * (point.x - centre.x)
                + math.cos(angle) * (point.y - centre.y)
                + centre.y
            )
            rotated.append(rotated_x)
            rotated.append(rotated_y)

        self._tris = ("v2f", tuple(rotated))
        bottom_left = rotated[0], rotated[1]
        bottom_right = rotated[2], rotated[3]

        new_pos = Point2D.from_tuple(bottom_left).midpoint(
            Point2D.from_tuple(bottom_right)
        )

        self._x = new_pos.x
        self._y = new_pos.y

    def __repr__(self):
        return f"Triangle(x={self._x}, y={self._y}, w={self._w}, h={self._h})"


class Line:
    def __init__(self, fro, to):
        self.one = fro
        self.two = to

    def __repr__(self):
        return f"Line(from={self.one}, to={self.two})"

    def draw(self):
        pyglet.graphics.draw(
            2,
            pyglet.gl.GL_LINES,
            ("v2f", (self.one.x, self.one.y, self.two.x, self.two.y)),
        )
