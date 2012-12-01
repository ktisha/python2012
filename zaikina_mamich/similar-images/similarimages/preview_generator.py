__author__ = 'ksenia'

import Image

import logging

logger = logging.getLogger('preview_generator')
logger.setLevel(logging.DEBUG)

def generate_preview(image_path, preview_path):
  logger.info('Image path: {0}'.format(image_path))
  image = Image.open(image_path)
  logger.info('Image size: {0}'.format(image.size))

  (max_width, max_height) = (400, 200)
  (real_width, real_height) = image.size

  (coefficient_width, coefficient_height) = (max_width / real_width, max_height / real_height)
  coefficient = coefficient_height if coefficient_width > coefficient_height else coefficient_width

  new_size = (real_width * coefficient, real_height * coefficient)

  preview = image.resize(new_size, Image.ANTIALIAS)

  logger.info('Preview path: {0}'.format(preview_path))
  preview.save(preview_path, "JPEG")
