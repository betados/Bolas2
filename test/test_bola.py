# -*- coding: utf-8 -*-

import unittest
from rigidBodies import Interaction, RoundBody

from objects import Bola


class TestBola(unittest.TestCase):
    def test_is_clicked(self):
        bola = Bola((0, 0, 0), (50, 50))
        self.assertTrue(Interaction.is_clicked(bola, RoundBody((51, 52))))
        self.assertFalse(Interaction.is_clicked(bola, RoundBody((66, 52))))
