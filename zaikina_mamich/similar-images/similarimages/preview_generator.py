__author__ = 'ksenia'

import Image

import logging

logger = logging.getLogger('preview_generator')
logger.setLevel(logging.DEBUG)

def generate_preview(image_path, preview_path):
  logger.info('generate_preview() entered')
  logger.debug('Image path: {0}'.format(image_path))
  logger.debug('Preview path: {0}'.format(preview_path))

  image = Image.open(image_path)
  logger.debug('Image size: {0}'.format(image.size))

  (max_width, max_height) = (400, 200)
  logger.debug('Max preview size: w {0}, h {1}'.format(max_width, max_height))
  (real_width, real_height) = image.size

  (coefficient_width, coefficient_height) = (float(max_width) / real_width, float(max_height) / real_height)
  logger.debug('Coefficients: w {0}, h {1}'.format(coefficient_width, coefficient_height))
  coefficient = coefficient_height if coefficient_width > coefficient_height else coefficient_width

  logger.debug('Coefficient: {0}'.format(coefficient))
  new_size = (int(real_width * coefficient), int(real_height * coefficient))

  logger.info('Preview size: {0}'.format(new_size))

  preview = image.resize(new_size, Image.ANTIALIAS)

  preview.save(preview_path, "JPEG")
  logger.info('generate_preview() exited')
