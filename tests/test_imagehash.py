import unittest
import imagehash
import numpy

class TestImageHash(unittest.TestCase):
    def setUp(self):
        self.ones = imagehash.ImageHash(numpy.ones((3, 2, 2)))

    def test_returns_string_for_ones(self):
        ones = str(self.ones)
        self.assertEqual(ones, '010101010101010101010101')

    def test_hex_to_image_returns_same_array(self):
        ones = imagehash.covert_hex_to_image_hash(str(self.ones))
        self.assertEqual(ones, self.ones)

    def test_two_different_image_hashes_are_unequal(self):
        twos = imagehash.covert_hex_to_image_hash('020202020202020202020202')
        self.assertNotEqual(twos, self.ones)

    def test_same_image_hashes_are_equal(self):
        self.assertEqual(self.ones, self.ones)
