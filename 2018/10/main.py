# -*- coding: utf-8 -*-
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt


class Light:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity


def parse_lights(text):
    lights = []
    for line in text.strip().splitlines():
        light = parse_light(line)
        lights.append(light)
    return lights


def parse_light(line):
    *kvs, __ = line.split('>')
    position, velocity = [parse_xy(kv) for kv in kvs]
    return Light(position, velocity)


def parse_xy(kv):
    __, xy = kv.split('<')
    return np.array(xy.split(','), np.int64)


def create_animation(lights, start_frame, interval):
    for __ in range(start_frame):
        for light in lights:
            light.position += light.velocity

    fig, ax = plt.subplots(figsize=(5, 3))
    x, y = zip(*[light.position for light in lights])
    scat = ax.scatter(x, y)

    def animate(i):
        # if (i - 1) % 100 == 0:
        print(f'animating {i}', flush=True)
        x_lim, y_lim = get_extents(lights)
        ax.set_xlim(x_lim)
        ax.set_ylim(y_lim)
        for light in lights:
            light.position += light.velocity
        scat.set_offsets(tuple(light.position for light in lights))
        return scat,

    return FuncAnimation(fig, animate, interval=interval, frames=1000000,
                         blit=True)


def get_extents(lights):
    print('calculating extents')
    points = tuple(light.position for light in lights)
    xmin, ymin = np.min(points, axis=0)
    xmax, ymax = np.max(points, axis=0)
    return (xmin, xmax), (ymin, ymax)


def part_1(input_):
    lights = parse_lights(input_)
    animation = create_animation(lights, start_frame=0, interval=2000)
    print(animation)
    plt.show()
