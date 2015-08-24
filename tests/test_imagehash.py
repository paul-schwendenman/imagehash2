import unittest
import imagehash
import numpy

class TestImageHash(unittest.TestCase):
    def setUp(self):
        self.black = imagehash.ImageHash(numpy.zeros((3, 2, 2)))
        self.gray = imagehash.ImageHash(numpy.ones((3, 2, 2)))
        self.white = imagehash.ImageHash(numpy.full((3, 2, 2), 255))

    def test_returns_all_zeros_for_black(self):
        self.assertEqual(str(self.black), '000000000000000000000000')

    def test_returns_all_fs_for_white(self):
        self.assertEqual(str(self.white), 'ffffffffffffffffffffffff')

    def test_returns_ones_for_gray(self):
        self.assertEqual(str(self.gray), '010101010101010101010101')

    def test_hex_to_image_returns_same_array(self):
        ones = imagehash.hex_to_hash(str(self.gray))
        self.assertEqual(ones, self.gray)

    def test_two_different_image_hashes_are_unequal(self):
        self.assertNotEqual(self.black, self.white)

    def test_same_image_hashes_are_equal(self):
        self.assertEqual(self.gray, self.gray)

    def test_two_very_different_image_hashes_have_large_difference(self):
        self.assertEqual(self.black - self.white, 255)

    def test_two_barely_different_image_hashes_have_small_difference(self):
        self.assertEqual(self.black - self.gray, 1)

    def test_image_hash_subtraction_is_associative(self):
        self.assertEqual(self.black - self.gray, self.gray - self.black)
