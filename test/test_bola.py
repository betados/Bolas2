# -*- coding: utf-8 -*-

import unittest
from rigidBodies import RigidBody

# from vector_2d import *

from objects import Bola


class TestBola(unittest.TestCase):
    def test_is_clicked(self):
        bola = Bola((50, 50))
        self.assertTrue(bola.is_clicked(RigidBody((51, 52))))
        self.assertFalse(bola.is_clicked(RigidBody((60, 52))))
