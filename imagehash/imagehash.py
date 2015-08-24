from PIL import Image
import numpy


def split_every_n(line, n):
    return [line[i:i+n] for i in range(0, len(line), n)]

class ImageHash(object):
    def __init__(self, array):
        self.array = array

    def __str__(self):
        return ''.join(hex(num)[2:-1].rjust(2, '0') for num in self.array.flatten())

    def __eq__(self, other):
        return numpy.array_equal(self.array.flatten(), other.array.flatten())

    def __sub__(self, other):
        return numpy.absolute(self.array.flatten() - other.array.flatten()).sum()

def average_hash(image, hash_size=8):
    '''Take the average of the image'''
    image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)
    pixels = numpy.array(image.getdata()).reshape((hash_size, hash_size))
    avg = pixels.mean()
    diff = pixels > avg
    return ImageHash(diff)

def color_hash(image, hash_size=8):
    image = image.convert("RGB").resize((hash_size, hash_size), Image.ANTIALIAS)
    pixels = numpy.array(image.getdata()).flatten('F').reshape((3, hash_size, hash_size))
    return ImageHash(pixels)

def covert_hex_to_image_hash(hex_string):
    array = numpy.array([int(num, 16) for num in split_every_n(hex_string, 2)])
    return ImageHash(array)
