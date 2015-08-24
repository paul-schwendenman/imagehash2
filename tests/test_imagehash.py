import unittest
import imagehash
import numpy

class TestImageHash(unittest.TestCase):
    def setUp(self):
        self.ones = imagehash.ImageHash(numpy.ones((3, 2, 2)))

    def test_returns_string_for_ones(self):
        ones = str(self.ones)
        self.assertEqual(ones, '010101010101010101010101')
