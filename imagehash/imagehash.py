from PIL import Image
import numpy

def average_hash(image, hash_size):
    '''Take the average of the image'''
    image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)
    pixels = numpy.array(image.getdata()).reshape((hash_size, hash_size))
    avg = pixels.mean()
    diff = pixels > avg
    return diff
