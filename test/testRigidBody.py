# -*- coding: utf-8 -*-

import unittest
from vector_2d import *

from rigidBodies import RigidBody


class TestRigidBody(unittest.TestCase):
    def test_init(self):
        po = RigidBody((50, 50))
        self.assertEqual(po.pos(), (50, 50))

    def test_actualize(self):
        po = RigidBody((50, 50))
        po.actualize(1)
        self.assertEqual(po.v, Vector(0, 0))
        po.v = Vector(1, 0)
        po.actualize(1)
        self.assertEqual(po.pos(), (51, 50))
        po.actualize(1)
        self.assertEqual(po.pos(), (52, 50))

    def test_eq(self):
        po = RigidBody()
        po2 = RigidBody()

        self.assertTrue(po != po2)
        self.assertFalse(po == po2)

        self.assertTrue(po == po)
        self.assertFalse(po != po)
