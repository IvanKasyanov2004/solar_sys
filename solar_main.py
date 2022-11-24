# coding: utf-8
# license: GPLv3

import pygame as pg
from solar_vis import calculate_scale_factor, Drawer
from solar_model import recalculate_space_objects_positions
from solar_input import read_space_objects_data_from_file, write_space_objects_data_to_file
from solar_stats import check_system, calculate_speed, calculate_distance, show_graph
import thorpy
import time
import numpy as np

timer = None

alive = True

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

model_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

time_scale = 100000.0
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""

scale_factor = 1
"""Масштабирование экранных координат по отношению к физическим.

Тип: float

Мера: количество пикселей на один метр."""

graph_time = np.array([])
"""
Массив значений времени для построения графиков
"""

graph_speed = np.array([])
"""
Массив значений скорости спутника в каждый момент времени
"""

graph_S = np.array([])
"""
Массив значений расстояния от планеты до спутника в каждый момент времени
"""


def execution(delta):
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global model_time
    global graph_time
    global graph_speed
    global graph_S
    recalculate_space_objects_positions([dr.obj for dr in space_objects], scale_factor, delta)
    model_time += delta
    if check_system([dr.obj for dr in space_objects]) == True:
        graph_time = np.append(graph_time, model_time)
        graph_speed = np.append(graph_speed, calculate_speed([dr.obj for dr in space_objects]))
        graph_S = np.append(graph_S, calculate_distance([dr.obj for dr in space_objects]))


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True


def pause_execution():
    """
    Останавливает выполнение программы
    """
    global perform_execution
    perform_execution = False


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global alive
    alive = False


def open_file():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global scale_factor
  
    in_filename = "solar_system.txt"
    space_objects = read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.obj.x), abs(obj.obj.y)) for obj in space_objects])
    scale_factor = calculate_scale_factor(max_distance)


def handle_events(events, menu):
    """
    Обрабатывает действия пользователя и вызывает реакцию интерфейса и всей программы на них
    """
    global alive
    for event in events:
        menu.react(event)
        if event.type == pg.QUIT:
            alive = False


def slider_reaction(event):
    """
    Назначение действия для элемента интерфеса slider
    """
    global time_scale
    time_scale = np.exp(5 + event.el.get_value())


def init_ui(screen):
    """
    Отрисовка основного интерфейса программы и назначение действий для каждого элемента интерфейса
    """
    slider = thorpy.SliderX(100, (-10, 10), "Simulation speed")
    slider.user_func = slider_reaction
    button_stop = thorpy.make_button("Quit", func=stop_execution)
    button_pause = thorpy.make_button("Pause", func=pause_execution)
    button_play = thorpy.make_button("Play", func=start_execution)
    timer = thorpy.OneLineText("Seconds passed")

    button_load = thorpy.make_button(text="Load a file", func=open_file)

    box = thorpy.Box(elements=[
        slider,
        button_pause, 
        button_stop, 
        button_play, 
        button_load,
        timer])
    reaction1 = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=slider_reaction,
                                event_args={"id": thorpy.constants.EVENT_SLIDE},
                                params={},
                                reac_name="slider reaction")
    box.add_reaction(reaction1)
    
    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen

    box.set_topleft((0, 0))
    box.blit()
    box.update()
    return menu, box, timer


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """

    global perform_execution
    global timer

    print('Modelling started!')

    pg.init()
    
    width = 900
    height = 750
    screen = pg.display.set_mode((width, height))
    last_time = time.perf_counter()
    drawer = Drawer(screen)
    menu, box, timer = init_ui(screen)
    perform_execution = True

    while alive:
        handle_events(pg.event.get(), menu)
        cur_time = time.perf_counter()
        if perform_execution:
            execution((cur_time - last_time) * time_scale)
            text = "%d seconds passed" % (int(model_time))
            timer.set_text(text)

        last_time = cur_time
        drawer.update(space_objects, box)
        time.sleep(1.0 / 60)

    write_space_objects_data_to_file("output.txt", space_objects)
    if check_system([dr.obj for dr in space_objects]) == True:
        show_graph(graph_time, graph_speed, graph_S)

    print('Modelling finished!')


if __name__ == "__main__":
    main()
