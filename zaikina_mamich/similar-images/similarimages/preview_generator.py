__author__ = 'ksenia'

import Image

import logging

logger = logging.getLogger('preview_generator')
logger.setLevel(logging.DEBUG)

def generate_preview(image_path, preview_path):
  logger.info('Image path: {0}'.format(image_path))
  image = Image.open(image_path)
  logger.info('Image size: {0}'.format(image.size))
  size = 400, 200
  image.thumbnail(size, Image.ANTIALIAS)
  logger.info('Preview path: {0}'.format(preview_path))
  image.save(preview_path)