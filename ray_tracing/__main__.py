import colorsys
import math
import random

import pyglet
from pyglet.window import key

from .player import Player
from .ray import Ray
from .shapes import Line, Point2D

LINE_COUNT = 10
FOV = 60

# now the fun begins

def create_quad_vertex_list(x, y, width, height):
    return x, y, x + width, y, x + width, y + height, x, y + height

window = pyglet.window.Window(width=1440, height=600)

player = Player(window.width / 4, window.height / 2)

preview_pane_quad_v_list = create_quad_vertex_list(window.width / 2, 0, window.width / 2, window.height)

preview_pane_quad = pyglet.graphics.vertex_list(
            4, ("v2f", preview_pane_quad_v_list), ("c3B", (0,) * 12))


def random_colour():
    r, g, b = colorsys.hsv_to_rgb(random.random(), 1, 1)
    return (int(r * 255), int(g * 255), int(b * 255))


def random_lines(n):
    lines = []
    for n in range(n):
        line = Line(
            Point2D(
                random.randint(0, window.width / 2),
                random.randint(0, window.height),
            ),
            Point2D(
                random.randint(0, window.width / 2),
                random.randint(0, window.height),
            ),
            colour=random_colour()
        )
        lines.append(line)
    return lines


lines = random_lines(LINE_COUNT)

to_draw = []


movements = {
    "left": False,
    "right": False,
    "up": False,
    "down": False,
    "hide": False,
    "norm": False
}


@window.event
def on_key_press(symbol, mod):
    if symbol == key.LEFT:
        movements["left"] = True
    elif symbol == key.RIGHT:
        movements["right"] = True
    elif symbol == key.UP:
        movements["up"] = True
    elif symbol == key.DOWN:
        movements["down"] = True
    elif symbol == key.H:
        movements["hide"] = not movements["hide"]
    elif symbol == key.N:
        movements["norm"] = not movements["norm"]


@window.event
def on_key_release(symbol, mod):
    if symbol == key.LEFT:
        movements["left"] = False
    elif symbol == key.RIGHT:
        movements["right"] = False
    elif symbol == key.UP:
        movements["up"] = False
    elif symbol == key.DOWN:
        movements["down"] = False


@window.event
def on_draw():

    window.clear()

    if movements["hide"] == False:
        player.draw()
        for line in lines:
            line.draw()

    preview_pane_quad.draw(pyglet.gl.GL_QUADS)

    draw_now = to_draw[:]
    to_draw.clear()

    for d in draw_now:
        d.draw(pyglet.gl.GL_QUADS)


def update_preview_pane():
    each_w = (window.width / 2) / FOV
    for i, sector in enumerate(
        range(int(window.width / 2), window.width, int(each_w))
    ):
        ray = player.rays[::-1][i]

        dist = ray.end.distance(ray.pos)

        colour = (0, 0, 0)

        if ray.u == None:
            brightness = 0
            h = window.height
        elif dist == 0:
            brightness = 1
            h = window.height
        else:
            brightness = (1 / (dist ** 2)) * 3000

            if brightness > 1:
                brightness = 1

            colour = tuple(
                int(channel * brightness) for channel in ray.target_colour
            )

            heading = ray.heading - player.heading

            dist = ray.end.distance(ray.pos)

            if movements["norm"] is True:
                dist *= math.cos(math.radians(heading))

            h = window.height - int(
                (
                    dist
                    / math.sqrt(
                        (window.width / 2) ** 2 + window.height ** 2
                    )
                )
                * window.height
            )

        quads = create_quad_vertex_list(sector, 0, each_w, h)

        quad = pyglet.graphics.vertex_list(
            4, ("v2f", quads), ("c3B", colour * 4)
        )

        to_draw.append(quad)


def physics_update(e):
    if movements["left"] == True:
        player.rotate(6)

    if movements["right"] == True:
        player.rotate(-6)

    if movements["up"] == True:
        player.move(10)

    if movements["down"] == True:
        player.move(-10)

    range_of_rays = range(
        player.heading - int(FOV / 2), player.heading + int(FOV / 2)
    )

    origin_point = Point2D(
        player.tri._tris[1][4], player.tri._tris[1][5]
    )

    rays = []

    for ray in range_of_rays:
        r = Ray(origin_point, ray)
        for line in lines:
            r.test_for_intersection(line)
        rays.append(r)

    player.rays = rays

    update_preview_pane()


pyglet.clock.schedule_interval(physics_update, 1 / 30)

pyglet.app.run()
