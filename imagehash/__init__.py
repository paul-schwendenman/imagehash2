'''An image hash module'''
from __future__ import absolute_import

from .imagehash import (grayscale_hash, ImageHash, hex_to_hash, color_hash)

__all__ = ['color_hash', 'grayscale_hash', 'hex_to_hash', 'ImageHash']
