__author__ = 'ksenia'

from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config

import logging

from .models import DBSession

def main(global_config, **settings):
  """ This function returns a Pyramid WSGI application.
  """
  logger = logging.getLogger('__init__')
  logger.setLevel(logging.DEBUG)
  logger.info('Application initialization...')

  engine = engine_from_config(settings, 'sqlalchemy.')
  DBSession.configure(bind=engine)

  session_factory = session_factory_from_settings(settings)

  config = Configurator(
    settings=settings,
    session_factory=session_factory
  )

  config.add_subscriber(
    'similarimages.subscribers.add_base_template',
    'pyramid.events.BeforeRender'
  )

  config.add_static_view('static', 'static', cache_max_age=3600)

  config.add_route('home', '/')
  config.add_route('upload', '/upload')
  config.add_route('choose', '/choose')
  config.add_route('result', '/result')

  config.scan()

  logger.info('Application initialization finished.')
  return config.make_wsgi_app()

