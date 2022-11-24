# coding: utf-8
# license: GPLv3

import numpy as np

import matplotlib
from matplotlib import pyplot as plt


def calculate_speed(space_objects):
    """Вычисляет модуль скорости планеты.

    Параметры:

    space_objects - список объектов.
    """
    for obj in space_objects:
        if obj.type == "planet":
            V = (obj.Vx  2 + obj.Vy  2) ** 0.5
            return V


def calculate_distance(space_objects):
    """Вычисляет расстояние между звездой и планетой

    Параметры:

    space_objects - список объектов.
    """
    for obj in space_objects:
        if obj.type == "star":
            X = obj.x
            Y = obj.y
        if obj.type == "planet":
            S = ((obj.x - X)  2 + (obj.y - Y)
            2) ** 0.5
            return S


def show_graph(graph_time, graph_speed, graph_S):
    """Выводит графики, описывающие движения планет.

    Параметры:

    graph_time - массив со значениями физического времени от начала отсчёта.

    graph_speed - массив со значениями модуля скорсоти планеты.

    graph_S - массив со значениями расстояния между планетой и звездой.
    """
    f = plt.figure(figsize=(14, 10))
    ax1 = f.add_subplot(221)
    ax1.plot(graph_time, graph_speed)
    ax1.set_xlabel(r"t, c")
    ax1.set_ylabel(r"$V, \frac{m}{c}$")
    ax1.set_title("Скорость от времени")
    ax1.minorticks_on()
    ax1.grid(which='minor', alpha=0.2)
    ax1.grid(which='major', alpha=1)

    ax2 = f.add_subplot(222)
    ax2.plot(graph_time, graph_S)
    ax2.set_xlabel(r"t, c")
    ax2.set_ylabel(r"$S, m $")
    ax2.set_title("Расстояние от времени")
    ax2.minorticks_on()
    ax2.grid(which='minor', alpha=0.2)
    ax2.grid(which='major', alpha=1)

    ax3 = f.add_subplot(223)
    ax3.plot(graph_S, graph_speed)
    ax3.set_xlabel(r"S, m")
    ax3.set_ylabel(r"$V, \frac{m}{c} $")
    ax3.set_title("Скорость от расстояния")
    ax3.minorticks_on()
    ax3.grid(which='minor', alpha=0.2)
    ax3.grid(which='major', alpha=1)

    plt.show()


if name == "__main__":
    print("This module is not for direct call!")
        