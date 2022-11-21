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
        X = obj.x - body.x
        Y = obj.y - body.y
        r = (X**2 + Y**2)**0.5
        # обработка аномалий при прохождении одного тела сквозь другое
        G = gravitational_constant  
        N = (G * body.m * obj.m) / r ** 3
        body.Fx = N * X
        body.Fy = N * Y
        # Взаимодействие объектов

def move_space_object(body, space_objects, scale_factor, dt):
    """Перемещает тело в соответствии с действующей на него силой. В случае столкновения скорости тел изменяются

    Параметры:

    **body** — тело, которое нужно переместить.

    **space_objects** - список объектов.

    **scale_factor** - масштабный коэффициент.

    **dt** - шаг по времени.
    """
    for obj in space_objects:
        if body == obj:
            continue
        X = obj.x - body.x
        Y = obj.y - body.y
        r_obj = obj.R / scale_factor
        r_body = body.R / scale_factor
        if (X**2 + Y**2) <= (r_obj + r_body)**2:
            delta_Vx_body = (2 * obj.m / (obj.m + body.m)) * (((obj.Vx - body.Vx) * X + (obj.Vy - body.Vy) * Y) / (X**2 + Y**2)) * X
            delta_Vy_body = (2 * obj.m / (obj.m + body.m)) * (((obj.Vx - body.Vx) * X + (obj.Vy - body.Vy) * Y) / (X**2 + Y**2)) * Y
            delta_Vx_obj = (2 * body.m / (obj.m + body.m)) * (((body.Vx - obj.Vx) * X + (body.Vy - obj.Vy) * Y) / (X**2 + Y**2)) * X
            delta_Vy_obj = (2 * body.m / (obj.m + body.m)) * (((body.Vx - obj.Vx) * X + (body.Vy - obj.Vy) * Y) / (X**2 + Y**2)) * Y
            body.Vx += delta_Vx_body
            body.Vy += delta_Vy_body
            obj.Vx += delta_Vx_obj
            obj.Vy += delta_Vy_obj

    ax = body.Fx / body.m
    body.Vx += ax * dt
    body.x += body.Vx * dt
    ay = body.Fy * body.m
    body.Vy += ay * dt
    body.y += body.Vy * dt


def recalculate_space_objects_positions(space_objects, scale_factor, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список объектов, для которых нужно пересчитать координаты.

    **scale_factor** - масштабный коэффициент.

    **dt** — шаг по времени.
    """
    for body in space_objects:
        calculate_force(body, space_objects)
    for body in space_objects:
        move_space_object(body, space_objects, scale_factor, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")
