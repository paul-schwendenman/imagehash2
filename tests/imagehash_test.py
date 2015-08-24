import unittest
import imagehash
import numpy
from PIL import Image

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

class TestHashes(unittest.TestCase):
    def setUp(self):
        self.black = Image.new('RGB', (600, 400))
        self.white = Image.new('RGB', (600, 400), color='white')
        self.red = Image.new('RGB', (600, 400), color='red')
        self.blue = Image.new('RGB', (600, 400), color='blue')
        self.green = Image.new('RGB', (600, 400), color='green')
        self.yellow = Image.new('RGB', (600, 400), color='yellow')

class TestColorHash(TestHashes):
    def test_white_returns_all_fs(self):
        self.assertEqual(str(imagehash.color_hash(self.white, 2)), 'ffffffffffffffffffffffff')

    def test_black_returns_all_zeros(self):
        self.assertEqual(str(imagehash.color_hash(self.black, 2)), '000000000000000000000000')

    def test_blue_returns_blue(self):
        self.assertEqual(str(imagehash.color_hash(self.blue, 2)), '0000000000000000ffffffff')

    def test_red_returns_red(self):
        self.assertEqual(str(imagehash.color_hash(self.red, 2)), 'ffffffff0000000000000000')

    def test_green_returns_green(self):
        self.assertEqual(str(imagehash.color_hash(self.green, 2)), '000000008080808000000000')

    def test_yellow_returns_yellow(self):
        self.assertEqual(str(imagehash.color_hash(self.yellow, 2)), 'ffffffffffffffff00000000')

class TestGrayScaleHash(TestHashes):
    def test_white_returns_all_fs(self):
        self.assertEqual(str(imagehash.grayscale_hash(self.white, 2)), 'ffffffff')

    def test_black_returns_all_zeros(self):
        self.assertEqual(str(imagehash.grayscale_hash(self.black, 2)), '00000000')

    def test_blue_returns_all_blue(self):
        self.assertEqual(str(imagehash.grayscale_hash(self.blue, 2)), '1d1d1d1d')

    def test_red_returns_all_red(self):
        self.assertEqual(str(imagehash.grayscale_hash(self.red, 2)), '4c4c4c4c')

    def test_green_returns_all_green(self):
        self.assertEqual(str(imagehash.grayscale_hash(self.green, 2)), '4b4b4b4b')

    def test_yellow_returns_all_yellow(self):
        self.assertEqual(str(imagehash.grayscale_hash(self.yellow, 2)), 'e1e1e1e1')
