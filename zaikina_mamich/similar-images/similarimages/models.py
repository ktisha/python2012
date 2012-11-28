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

DBSession = scoped_session(sessionmaker(extension = ZopeTransactionExtension()))
Base = declarative_base()

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, autoincrement = True, nullable = False, primary_key = True)
    name = Column(Text, unique = True, nullable = False)
    histogram = Column(Text, nullable = False)
    expectation_value = Column(Float, nullable = False)
    dispersion = Column(Float, nullable = False)
    standard_deviation = Column(Float, nullable = False) 

    def __init__(self, name, hist, ex_value, disp, std_dev):
        self.name = name
        self.historgam = hist
        self.expectation_value = exp_value
        self.dispersion = disp
        self.standard_deviation = std_dev
