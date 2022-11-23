# coding: utf-8
# license: GPLv3
import random

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить дейстующую силу.

    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if obj.alive == 0:
            continue # мертвые тела не участвуют в движении.
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        X = obj.x - body.x
        Y = obj.y - body.y
        r = (X**2 + Y**2)**0.5
        # обработка аномалий при прохождении одного тела сквозь другое
        G = gravitational_constant  
        N = (G * body.m * obj.m) / (r ** 3)
        body.Fx += N * X
        body.Fy += N * Y
        # Взаимодействие объектов

def move_space_object(body, dt):
    """Перемещает тело в соответствии с действующей на него силой. В случае столкновения скорости тел изменяются

    Параметры:

    **body** — тело, которое нужно переместить.

    **space_objects** - список объектов.

    **scale_factor** - масштабный коэффициент.

    **dt** - шаг по времени.
    """
    ax = body.Fx / body.m
    body.Vx += ax * dt
    body.x += body.Vx * dt
    ay = body.Fy / body.m
    body.Vy += ay * dt
    body.y += body.Vy * dt


def hittest_space_objects(body, space_objects, scale_factor):
    for obj in space_objects:
        if body == obj:
            continue
        X = obj.x - body.x
        Y = obj.y - body.y
        r_obj = obj.R / scale_factor
        r_body = body.R / scale_factor
        if (obj.alive == 1) and (float((X**2 + Y**2)) <= float((r_obj + r_body)**2)):                          
            body.Vx = (body.m * body.Vx + obj.m * obj.Vx) / (body.m + obj.m)
            body.Vy = (body.m * body.Vy + obj.m * obj.Vy) / (body.m + obj.m)
            body.Fx = body.Fy = 0
            body.x = (body.m * body.x + obj.m * obj.x) / (body.m + obj.m)
            body.y = (body.m * body.y + obj.m * obj.y) / (body.m + obj.m)
            body.R = (2 * (body.m + obj.m) / (body.m / body.R ** 3 + obj.m / obj.R ** 3)) ** (1/3)
            body.m = body.m + obj.m
            body.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            obj.alive = 0


def recalculate_space_objects_positions(space_objects, scale_factor, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список объектов, для которых нужно пересчитать координаты.

    **scale_factor** - масштабный коэффициент.

    **dt** — шаг по времени.
    """
    for body in space_objects:
         if body.alive == 1:
            calculate_force(body, space_objects)        
    for body in space_objects:
        if body.alive == 1:
            move_space_object(body, dt)
    for body in space_objects:
        if body.alive == 1:
            hittest_space_objects(body, space_objects, scale_factor)


if __name__ == "__main__":
    print("This module is not for direct call!")
