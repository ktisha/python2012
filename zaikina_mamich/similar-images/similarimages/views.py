__author__ = 'ksenia'

import os

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

import formencode

from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from pyramid.url import route_path

from .models import (
  DBSession,
  Image,
  )

from .database_manager import DBManager

import logging

logger = logging.getLogger('models')
logger.setLevel(logging.DEBUG)


@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
  return {
    'page_name': 'Home'
  }


class PictureUploadSchema(formencode.Schema):
  allow_extra_fields = True
  picture = formencode.validators.FieldStorageUploadConverter(not_empty=True)


@view_config(route_name='upload', renderer='templates/upload.pt')
def upload_view(request):
  form = Form(request, schema=PictureUploadSchema)

  if 'form_submitted' in request.POST:
    if form.validate():
      field = request.POST.get('picture')
      filename = field.filename
      content = field.value

      (_, extension) = os.path.splitext(filename)
      extension.lower()
      if extension == 'jpeg' and extension == 'jpg':


        # Should be searched
        image = DBManager.retrieve_image_by_name(filename)

        # If found then do nothing
        # Otherwise it should be processed and saved to database
        if image is None:
          # Call of processing function
          # Parameter: content
          # Returned dictionary:
          #   'histogram' (string)
          #   'expectation_value' (float)
          #   'dispersion' (float)
          #   'standard_deviation' (float)

          image_parameters = {
            'histogram': '',
            'expectation_value': 0.0,
            'dispersion': 0.0,
            'standard_deviation': 0.0
          }

          # image_parameters = image_processing_module.process_image(content)

          image = DBManager.create_image(
            filename=filename,
            content=content,
            histogram=image_parameters['histogram'],
            exp_value=image_parameters['expectation_value'],
            dispersion=image_parameters['dispersion'],
            std_dev=image_parameters['standard_deviation']
          )

        request.session['image'] = image
        return HTTPFound(location=route_path('result', request))

  return {
    'form': FormRenderer(form),
    'page_name': 'Upload'
  }


@view_config(route_name='choose', renderer='templates/choose.pt')
def choose_view(request):
  return {
    'page_name': 'Choose'
  }


@view_config(route_name='result', renderer='templates/result.pt')
def result_view(request):
  image = request.session['image']
  if not image:
    return HTTPFound(location=route_path('home'))



  return {
    'page_name': 'Result'
  }