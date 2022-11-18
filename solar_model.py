# coding: utf-8
# license: GPLv3

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
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        X = body.x - obj.x
        Y = body.y - obj.y
        r = (X**2 + Y**2)**0.5
        r = max(r, body.R)
        # обработка аномалий при прохождении одного тела сквозь другое
        X = obj.x - body.x
        Y = obj.y - body.y
        G = gravitational_constant  
        N = (G * body.m * obj.m) / r ** 3
        body.Fx = N * X
        body.Fy = N * Y
        # Взаимодействие объектов

def move_space_object(body, dt):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """
    old = body.x  # FIXME: Вывести формулы для ускорения, скоростей и координат
    ax = body.Fx / body.m
    body.Vx += ax * dt
    body.x += body.Vx * dt
    ay = body.Fy * body.m
    body.Vy += ay * dt
    body.y += body.Vy * dt


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список объектов, для которых нужно пересчитать координаты.

    **dt** — шаг по времени
    """
    for body in space_objects:
        calculate_force(body, space_objects)
    for body in space_objects:
        move_space_object(body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")
