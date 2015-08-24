'''An image hash module'''
from __future__ import absolute_import

from .imagehash import (average_hash, ImageHash, covert_hex_to_image_hash,
                        color_hash)

__all__ = ['average_hash', 'get_pixels']
