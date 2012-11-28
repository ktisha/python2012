from pyramid.view import view_config

import formencode

from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer


from .models import (
  DBSession,
  Image,
  )

@view_config(route_name = 'home', renderer = 'templates/home.pt')
def home_view(request):
  return {
    'page_name' : 'Home'
  }

class PictureUploadSchema(formencode.Schema):
  allow_extra_fields = True
  picture = formencode.validators.FieldStorageUploadConverter(not_empty = True)


@view_config(route_name = 'upload', renderer = 'templates/upload.pt')
def upload_view(request):
  form = Form(request, schema = PictureUploadSchema)
  
  if 'form_submitted' in request.POST:
    if form.validate():
      field = request.POST.get('picture')
      filename = field.filename
      content = field.value
      
      # Should be searched
      
      # Should be saved if not found
      
      # Should be processed if not found
  
  return {
    'form': FormRenderer(form),
    'page_name' : 'Upload'
  }
