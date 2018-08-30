# -*- coding: utf-8 -*-

import unittest
from vector_2D.vector import Vector

from physical_object import PhysicalObject


class TestPhysicalObject(unittest.TestCase):
    def test_init(self):
        po = PhysicalObject((50, 50))
        self.assertEqual(po.pos(), (50, 50))

    def test_actualize(self):
        po = PhysicalObject((50, 50))
        po.actualize(1)
        self.assertEqual(po.v, Vector(0, 0))
        po.v = Vector(1, 0)
        po.actualize(1)
        self.assertEqual(po.pos(), (51, 50))
        po.actualize(1)
        self.assertEqual(po.pos(), (52, 50))
