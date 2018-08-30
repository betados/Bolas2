# -*- coding: utf-8 -*-

import unittest
from physical_object import PhysicalObject

from vector_2D.vector import Vector

from bola import Bola


class TestBola(unittest.TestCase):
    def test_is_clicked(self):
        bola = Bola((50, 50))
        self.assertTrue(bola.is_clicked(PhysicalObject((51, 52))))
        self.assertFalse(bola.is_clicked(PhysicalObject((60, 52))))
