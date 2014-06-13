# -*- coding: utf-8 -*-
import unittest
from mirroring.item import Item


class TestItem(unittest.TestCase):
    def test(self):
        Item.set_base_url('http://www.onlineedge.com.au/')
        item = Item('http://www.onlineedge.com.au/', [])

        Item.set_base_url('http://bash.im/')
        item = Item('http://bash.im/', [])
