# coding: utf-8
# license: GPLv3

import numpy as np

import matplotlib
from matplotlib import pyplot as plt

def calculate_speed(space_objects):
    for obj in space_objects:
        if obj.type == "planet":
            V = (obj.Vx ** 2 + obj.Vy ** 2) ** 0.5
            return V
        
def calculate_distance(space_objects):
    for obj in space_objects:
        if obj.type == "star":
            X = obj.x
            Y = obj.y
        if obj.type == "planet":
            S = ((obj.x - X) ** 2 + (obj.y - Y) ** 2) ** 0.5
            return S
        
def show_graph(graph_time, graph_speed, graph_S):
    plt.subplot(2,2,1)
    plt.plot(graph_time, graph_speed, label = "speed (time)")
    plt.xlabel(r"t, c")
    plt.ylabel(r"$V, \frac{m}{c} $")
    plt.title("$График скорости от времени$")
    plt.minorticks_on()
    plt.grid(which = 'minor', alpha = 0.2)

    plt.subplot(2,2,2)
    plt.plot(graph_time, graph_S, label = "S (time)")

    plt.subplot(2,2,3)
    plt.plot(graph_S, graph_speed)

    plt.show()

            
if __name__ == "__main__":
    print("This module is not for direct call!")

        