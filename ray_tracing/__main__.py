import pyglet
from pyglet.window import key
from .player import Player
from .shapes import Line, Point2D
from .ray import Ray
import random
import math

LINE_COUNT = 10
FOV = 80

# now the fun begins

window = pyglet.window.Window(width=1280, height=600)

player = Player(window.width/4, window.height/2)

def random_lines(n):
    lines = []
    for n in range(n):
        line = Line(
            Point2D(random.randint(0, window.width / 2), random.randint(0, window.height)),
            Point2D(random.randint(0, window.width / 2), random.randint(0, window.height)))
        lines.append(line)
    return lines

lines = random_lines(LINE_COUNT)

to_draw = []


movements = {
    "left": False,
    "right": False,
    "up": False,
    "down": False,
    "hide": False
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

    draw_now = to_draw[:]
    to_draw.clear()

    for d in draw_now:
        d.draw(pyglet.gl.GL_QUADS)

def update_preview_pane():
    each_w = (window.width / 2) / FOV
    for i, sector in enumerate(range(int(window.width / 2), window.width, int(each_w))):
        ray = player.rays[::-1][i]

        if ray.u == None:
            brightness = 0
            h = window.height
        else:
            brightness = int((255 * (1 / (ray.end.distance(ray.pos) ** 2))) * 3000)
            
            if brightness > 255:
                brightness = 255

            h = window.height - int((ray.end.distance(ray.pos) / math.sqrt((window.width / 2) ** 2 + window.height ** 2)) * window.height)

        quads =  create_quad_vertex_list(sector, 0, each_w, h)

        quad = pyglet.graphics.vertex_list(4,
            ('v2f', quads),
            ('c3B', (brightness,) * 12))

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

    range_of_rays = range(player.heading - int(FOV / 2), player.heading + int(FOV / 2))

    origin_point = Point2D(player.tri._tris[1][4], player.tri._tris[1][5])

    rays = []

    for ray in range_of_rays:
        r = Ray(origin_point, ray)
        for line in lines:
            r.test_for_intersection(line)
        rays.append(r)

    player.rays = rays

    update_preview_pane()

def create_quad_vertex_list(x, y, width, height):
    return x, y, x + width, y, x + width, y + height, x, y + height


pyglet.clock.schedule_interval(physics_update,1/30)

pyglet.app.run()