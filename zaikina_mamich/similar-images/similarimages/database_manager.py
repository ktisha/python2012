__author__ = 'ksenia'

import os
import transaction

from .models import (
  Image,
  DBSession
  )

from .preview_generator import generate_preview


class DatabaseManager:
  # Constant for image storing
  # Defines the way of partitioning folders
  __image_distribution_modulo = 10

  @classmethod
  def path_to_image(cls, id, name):
    part = id % cls.__image_distribution_modulo
    return 'static{0}db_images{0}{1}{0}{2}'.format(os.sep, part, name)

  @classmethod
  def path_to_image_preview(cls, id, name):
    part = id % cls.__image_distribution_modulo
    (n, ext) = os.path.splitext(name)
    return 'static{0}db_images{0}{1}{0}{2}{3}{4}'.format(os.sep, part, n, '-small', ext)


  @classmethod
  def __path_to_image(cls, id, name):
    path = 'similarimages{0}{1}'.format(
      os.sep,
      cls.path_to_image(id=id, name=name)
    )
    (dir, _) = os.path.split(path)
    if not os.path.exists(dir):
      os.makedirs(dir)
    return path

  @classmethod
  def __path_to_image_preview(cls, id, name):
    return 'similarimages{0}{1}'.format(
      os.sep,
      cls.path_to_image_preview(id=id, name=name)
    )

  @classmethod
  def __save_image_to_filesystem(cls, id, filename, content):
    img = open(cls.__path_to_image(id=id, name=filename), mode='w')
    img.write(content)
    img.close()

  @classmethod
  def __load_image_from_filesystem(cls, id, filename):
    img = open(cls.__path_to_image(id=id, name=filename))
    content = img.read()
    img.close()
    return content

  @classmethod
  def create_image(cls, filename, content, histogram, exp_value, dispersion, std_dev):
    # Save data to database file
    session = DBSession()
    img = Image(name=filename, hist=histogram, exp_value=exp_value, dispersion=dispersion, std_dev=std_dev)
    session.add(img)
    session.flush()
    transaction.commit()

    # Save file contents to filesystem
    session = DBSession()
    img = Image.get_by_name(filename)
    cls.__save_image_to_filesystem(id=img.id, filename=filename, content=content)

    # Generate preview and save it to filesystem
    generate_preview(
      cls.__path_to_image(id=img.id, name=filename),
      cls.__path_to_image_preview(id=img.id, name=filename)
    )
    return img


  @classmethod
  def __image_to_dictionary(cls, image):
    return {
      'id': image.id,
      'name': image.name,
      'histogram': image.histogram,
      'expectation_value': image.expectation_value,
      'dispersion': image.dispersion,
      'standard_deviation': image.standard_deviation,
      'path': cls.path_to_image(id=image.id, name=image.name),
      'preview': cls.path_to_image_preview(id=image.id, name=image.name)
    }

  @classmethod
  def __image_array_to_dictionary_array(cls, images):
    result = []
    for image in images:
      result.append(cls.__image_to_dictionary(image))
    return result


  @classmethod
  def retrieve_all_images(cls):
    session = DBSession()
    return cls.__image_array_to_dictionary_array(Image.get_all())

  @classmethod
  def retrieve_all_except_one(cls, image_id, image_name):
    if image_id:
      session = DBSession()
      return cls.__image_array_to_dictionary_array(
        Image.get_all_except_one_with_id(image_id)
      )
    if image_name:
      session = DBSession()
      return cls.__image_array_to_dictionary_array(
        Image.get_all_except_one_with_name(image_name)
      )

  @classmethod
  def retrieve_image_by_name(cls, name):
    session = DBSession()
    image = Image.get_by_name(name=name)
    if image:
      return cls.__image_to_dictionary(image)


DBManager = DatabaseManager()