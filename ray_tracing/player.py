from .shapes import Triangle


class Player:
    def __init__(self, x, y, w=30, h=30):
        self.tri = Triangle(x, y, w, h)
        self.heading = 90  # North
        self.rays = []

    def draw(self):
        self.tri.draw()
        for ray in self.rays:
            ray.draw()

    def rotate(self, a):
        self.heading += a
        self.tri.rotate(a)

    def move(self, mag):
        self.tri.move(mag, self.heading)
