# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 10:23:13 2017

@author: gruenewa


first try:
    pixelated rendering
    
"""
import math
from math import pi
import numpy as np
from sympy.geometry import Segment, Point, Line
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm 

class raycaster():
    
    def __init__(self, alpha):
        self.alpha = alpha # Angle to optical axis
        self.x = 0 # Distance to optical axis
        
        self.h = math.sqrt(1**2 - (1/2)**2) # distance from point C to edge AB
        
    def vector(self):
        vector = np.array([self.x, self.alpha])
        return vector

    def distance_to_next_wall(self, vector):
        x = vector[0]
        alpha = vector[1]
        distance_to_AB = self.h / math.cos(alpha)
        distance = distance_to_AB
        return distance
        
    def transfermatrix(self, vector):
        d = self.distance_to_next_wall(vector)
        T = np.matrix([[1,-d], [0,1]])
        return T
        
    def mirrormatrix(self):
        return np.matrix([[1,0],[0,-1]]) #wrong, only usefull for mirror perpendicular to the ray
        

    def get_trinangle_points(self):
        A = [0.5, self.h]
        B = [-0.5, self.h]
        C = [0,0]
        return A,B,C
        
    def two_points_from_vector(self, vector):
        x = vector[0]
        alpha = vector[1]
        P1 = [x, 0]
        P2 = [math.tan(alpha)+x, 1]        
        return P1, P2
                
    def intersection_of_vector_with_triangle(self):
        A,B,C = self.get_trinangle_points()
        S_AB = Segment(A,B)
        S_AC = Segment(A,C)
        S_BC = Segment(B,C)
        
        P1, P2 = self.two_points_from_vector(self.vector())
        L_vector = Line(P1, P2)
        
        mirror_point = L_vector.intersection(S_AB)
        return mirror_point
        
        
class raycast3r():
    def __init__(self, startpoint, alpha):
        self.current = Point(startpoint)
        self.direction = Point(math.tan(math.radians(alpha)), 1)
        self.alpha = alpha # indicent angle
        # generate LUT
        A,B,C = self.get_trinangle_points()
        S_AB, S_AC, S_BC = self.generate_triangle(A,B,C)
        self.mirrors = [S_AB, S_AC, S_BC] # trigangle made of mirrors
        
    # hard coded triangle    
    def get_trinangle_points(self):
        h = math.sqrt(1**2 - (1/2)**2) # distance from point C to edge AB
        A = [0.5, h]
        B = [-0.5, h]
        C = [0,0]
        return A,B,C 
        
    def generate_triangle(self, A,B,C):
        S_AB = Segment(A,B)
        S_AC = Segment(A,C)
        S_BC = Segment(B,C)
        return S_AB, S_AC, S_BC        
        
    def cast(self):
        # generate line
        line = Line(self.current, self.direction)
        shortest_ray = None
        intersecting_segment = None
        intersection_point = None
        l = math.inf
        for segment in self.mirrors:
            # intersect line with segments from triangle
            mirror_point = line.intersection(segment)
            if mirror_point != []:
                mirror_point = mirror_point[0]
                ray = Segment(self.current, mirror_point)
                if isinstance(ray, Segment):
                    if ray.length < l:
                        l = ray.length                    
                        shortest_ray = ray 
                        intersecting_segment = segment
                        intersection_point = mirror_point
        
        # calculate angle between ray and segment
        next_ray = None
        if intersecting_segment is not None:
            incidenting_angle = shortest_ray.angle_between(intersecting_segment)
            corrected_incidenting_angle = incidenting_angle % (pi/2)
            print("ray is intersecting with an angle: ", math.degrees(incidenting_angle), "corrected", math.degrees(corrected_incidenting_angle))
            next_ray = shortest_ray.rotate((math.pi/2-corrected_incidenting_angle)*2, pt=intersection_point)
            self.current = next_ray.points[0]
            self.direction = next_ray.points[1]
        return [shortest_ray, next_ray]
        
        
class plot0r():
    
    def __init__(self):
        figsize = (5, 5)
        fig, axes = plt.subplots(1,1, figsize=figsize)    
        ax = axes
#        plt.axis("off")
        plt.axis((-.6,.6, -.1,1.1))
        
        self.ax = ax
#        plt.show()        
        
    def plot_line(self, begin, end, style = "-", color="gray"):
        ax = self.ax
        x, y = zip(begin, end)
        ax.plot(x,y, style, c=color)
#        plt.show()

    

def solve_problem():
#    rc = raycaster(math.radians(-10))
#    T0 = rc.transfermatrix(rc.vector())
#    M1 = rc.mirrormatrix()
#    v0 = rc.vector()
#    print("T0")
#    print(T0)
#    print("M1")
#    print(M1)
#    print("T0*M1")
#    print(T0*M1)
#    v1 = np.array(np.dot((T0*M1),v0))[0]
#    print("v0", v0)
#    print("v1", v1)
#    print(type(v1))
    rc = raycast3r(np.array([0,0]), 10)
#    return
    # plot triangle
    A,B,C = rc.get_trinangle_points()
    pl = plot0r()
    pl.plot_line(A,B)
    pl.plot_line(A,C)
    pl.plot_line(B,C)
    
    # plot first ray
    bounces = 4
    color=iter(cm.viridis(np.linspace(0,1,bounces+bounces)))    
    for i in range(bounces):
        rays = rc.cast()
#        rays = rays[0:1]
        for ray in rays:
            pl.plot_line(ray.points[0], ray.points[1], style = "-", color=next(color))
    
#    rays = rc.cast()    
##    print(rays)
#    for ray in rays:
#        pl.plot_line(ray.points[0], ray.points[1], style = "y-")        
    
#    P1, P2 = rc.two_points_from_vector(v0)
#    Pm1 = rc.intersection_of_vector_with_triangle()
#    Pm1 = [Pm1[0].x, Pm1[0].y]
#    pl.plot_line(P1, Pm1, style = "b-")
    
    # plot second ray
#    P1, P2 = rc.two_points_from_vector(v1)
##    Pm1 = rc.intersection_of_vector_with_triangle()
##    Pm1 = [Pm1[0].x, Pm1[0].y]
#    pl.plot_line(P1, P2, style = "b-")


    
    plt.show()

    
if __name__ == "__main__":    
    import time
    start_time = time.time()         
    solve_problem()  
    print("runtime: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - start_time))