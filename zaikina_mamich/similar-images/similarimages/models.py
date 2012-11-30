__author__ = 'ksenia'

from sqlalchemy import (
  Column,
  Float,
  Integer,
  Text,
  )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
  scoped_session,
  sessionmaker,
  )

from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Image(Base):
  __tablename__ = 'images'

  id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
  name = Column(Text, unique=True, nullable=False)
  histogram = Column(Text, nullable=False)
  expectation_value = Column(Float, nullable=False)
  dispersion = Column(Float, nullable=False)
  standard_deviation = Column(Float, nullable=False)

  def __init__(self, name, hist, exp_value, dispersion, std_dev):
    self.name = name
    self.histogram = hist
    self.expectation_value = exp_value
    self.dispersion = dispersion
    self.standard_deviation = std_dev

  @classmethod
  def get_by_id(cls, id):
    return DBSession.query(cls).get(id)

  @classmethod
  def get_by_name(cls, name):
    return DBSession.query(cls).filter(cls.name == name).first()

  @classmethod
  def get_all(cls):
    return DBSession.query(cls).all()

  @classmethod
  def get_all_except_one_with_id(cls, id):
    return DBSession.query(cls).filter(cls.id != id)

  @classmethod
  def get_all_except_one_with_name(cls, name):
    return DBSession.query(cls).filter(cls.name != name)
