# -*- coding: utf-8 -*-
from rigidBodies import *
import time


def kronos(func):
    """
        Decorator to measure your function's execution time
    """

    def wrapper(*args, **kwargs):
        t = time.time()
        result = func(*args, **kwargs)
        print 'Execution time of ' + func.__module__ + '.' + func.__name__ + ': ', time.time() - t
        return result

    return wrapper


class Interaction(object):
    @staticmethod
    def check_collision(obj1, obj2):
        if id(obj1) != id(obj2):
            if isinstance(obj1, RoundBody) and isinstance(obj2, LineObject):
                Interaction.manage_round_line_collision(obj1, obj2)
                return

            if isinstance(obj1, RoundBody) and isinstance(obj2, RoundBody):
                overlap = ((obj1.radio + obj2.radio) - abs(obj1.pos - obj2.pos))
                if overlap > 0:
                    obj1.append_force((obj1.pos - obj2.pos).unit() * overlap * obj1.k)
                    return

            if isinstance(obj1, RoundBody) and isinstance(obj2, RectBody):
                for line in obj2.lines:
                    overlap, normal = Interaction.manage_round_line_collision(obj1, line)
                    if overlap and overlap > 0:
                        distance = obj1.pos - obj2.pos - normal * (obj1.radio - overlap)
                        obj2.append_force(distance, -normal * overlap * obj1.k)
                        return

            if isinstance(obj1, RectBody) and isinstance(obj2, RectBody):
                for point in obj1.points:
                    overlap = min([distance_point_segment(point, line) for line in obj2.lines])
                    if overlap < 2:
                        print 'RECT COLLISION'

    @staticmethod
    def manage_round_line_collision(round_obj, obj2):
        overlap = round_obj.radio - distance_point_segment(round_obj.pos, obj2.points)
        if overlap > 0:
            normal = (obj2.points[0] - obj2.points[1]).normal()
            round_obj.append_force(
                # FIXME solo una cara es rebotante y esa dependa de orden de los puntos al crear
                normal * overlap * round_obj.k)
            return overlap, normal
        return None, None

    @staticmethod
    def is_clicked(obj, mouse):
        if isinstance(obj, RoundBody):
            return abs(obj.pos - mouse.pos) <= obj.radio

        if isinstance(obj, RectBody):
            return Interaction.point_is_inside_closed_lines(mouse.pos, obj.lines)

    @staticmethod
    def is_inside_rect(rect, pos):
        return rect[0] < pos.x < rect[0] + rect[2] and rect[1] < pos.y < rect[1] + rect[3]

    @staticmethod
    @kronos
    def point_is_inside_closed_lines(point, lines_list):
        """
            This function is slow. Use it carefully
        """
        # FIXME no funciona perfecto todasl as veces
        times = 0
        # FIXME sería bueno saber el ancho de la pantalla para el range
        for i in range(800):
            for line in lines_list:
                if distance_point_segment(point + Vector(i, 0), line) < 1:
                    times += 1
        # print times
        # I divide it cause, when crossing each line, two points are at less than one of distance
        if (times / 2) % 2 != 0:
            return True
        else:
            return False
