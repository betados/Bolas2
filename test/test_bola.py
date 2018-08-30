# -*- coding: utf-8 -*-

import unittest

from vector_2D.vector import Vector

from bola import Bola


class TestBola(unittest.TestCase):
    def test_is_clicked(self):
        bola = Bola((640, 480), (50, 50))
        self.assertTrue(bola.is_clicked(Vector(51, 52)))
        self.assertFalse(bola.is_clicked(Vector(60, 52)))
