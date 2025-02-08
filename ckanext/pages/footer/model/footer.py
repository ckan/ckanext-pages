import datetime
import uuid
from ckan.model import DomainObject
from six import text_type
import sqlalchemy as sa
from sqlalchemy import Column, types
from ckan.model import Session


try:
    from sqlalchemy.engine import Row
except ImportError:
    try:
        from sqlalchemy.engine.result import RowProxy as Row
    except ImportError:
        from sqlalchemy.engine.base import RowProxy as Row

from ckan import model
from ckan.model.domain_object import DomainObject

try:
    from ckan.plugins.toolkit import BaseModel
except ImportError:
    # CKAN <= 2.9
    from ckan.model.meta import metadata
    from sqlalchemy.ext.declarative import declarative_base

    BaseModel = declarative_base(metadata=metadata)


def make_uuid():
    return text_type(uuid.uuid4())


class FooterBaseModelForInstances():
    @classmethod
    def filter(cls, **kwargs):
        q = Session.query(cls)
        
        if kwargs:  q = q.filter_by(**kwargs)
        
        return q.order_by(cls.order.asc())

    @classmethod
    def exists(cls, **kwargs):
        return bool(cls.get(**kwargs))

    @classmethod
    def get(cls, **kwargs):
        return cls.filter(**kwargs).first()
    
    @classmethod
    def patch_record(cls, **kwargs):
        record_id = kwargs.get('id')
        
        record = cls.get(id=record_id)
        if record:
            for key, value in kwargs.items():
                if hasattr(cls, key):
                    setattr(record, key, value)

            Session.commit()

        return record


class FooterBaseModelSingleton():
    @classmethod
    def get(cls):
        return Session.query(cls).first()
    
    @classmethod
    def patch_records(cls, **kwargs):
        record = cls.get()
        if record:
            for key, value in kwargs.items():
                if hasattr(cls, key):
                    setattr(record, key, value)

            Session.commit()
        else:
            kwargs = {k:v for k,v in kwargs.items() if hasattr(cls, k) and k != 'id'}
            record = cls(**kwargs)
            record.add()
            record.commit()

        return record



class FooterMain(DomainObject, BaseModel, FooterBaseModelSingleton):
    __tablename__ = 'cms_footer_main'

    DEFAULT_LOGO_EN = '/images/footerlogo-en.png'
    DEFAULT_LOGO_AR = '/images/footerlogo-ar.png'
    DEFAULT_PHONE_NUMBER = '05255242'


    id = Column(types.UnicodeText, primary_key=True, default=make_uuid)
    logo_en = Column(types.UnicodeText, nullable=True, default='')
    logo_ar = Column(types.UnicodeText, nullable=True, default='')
    phone_number  = Column(types.UnicodeText, nullable=True, default='')
    modified = Column(types.DateTime, default=datetime.datetime.utcnow)


class FooterColumnTitles(DomainObject, BaseModel, FooterBaseModelSingleton):
    __tablename__ = 'cms_footer_column_titles'

    DEFAULT_COLUMN2_EN = 'Open Data Policies'
    DEFAULT_COLUMN2_AR = 'سياسة البيانات المفتوحة'
    DEFAULT_COLUMN3_EN = 'Open Data Tools'
    DEFAULT_COLUMN3_AR = 'أدوات البيانات المفتوحة'

    id = Column(types.UnicodeText, primary_key=True, default=make_uuid)
    column2_en = Column(types.UnicodeText, nullable=True, default='')
    column2_ar = Column(types.UnicodeText, nullable=True, default='')
    column3_en  = Column(types.UnicodeText, nullable=True, default='')
    column3_ar  = Column(types.UnicodeText, nullable=True, default='')
    modified = Column(types.DateTime, default=datetime.datetime.utcnow)



class FooterColumnLinks(DomainObject, BaseModel, FooterBaseModelForInstances):
    __tablename__ = 'cms_footer_column_links'

    id = Column(types.UnicodeText, primary_key=True, default=make_uuid)
    
    title_en = Column(types.UnicodeText, nullable=False, default='')
    title_ar = Column(types.UnicodeText, nullable=False, default='')
    link_en = Column(types.UnicodeText, nullable=False, default='')
    link_ar  = Column(types.UnicodeText, nullable=False, default='')
    target  = Column(types.UnicodeText, nullable=False, default='')
    
    order  = Column(types.Integer, nullable=False, default=0)
    column_number  = Column(types.Integer, nullable=False, default=2)

    modified = Column(types.DateTime, default=datetime.datetime.utcnow)
    created = Column(types.DateTime, default=datetime.datetime.utcnow)


class FooterSocialMedia(DomainObject, BaseModel, FooterBaseModelForInstances):
    __tablename__ = 'cms_footer_social_media'

    id = Column(types.UnicodeText, primary_key=True, default=make_uuid)
    
    title_en = Column(types.UnicodeText, nullable=False, default='')
    title_ar = Column(types.UnicodeText, nullable=False, default='')
    link_en = Column(types.UnicodeText, nullable=False, default='')
    link_ar  = Column(types.UnicodeText, nullable=False, default='')
    image_url  = Column(types.UnicodeText, nullable=False, default='')
    
    order  = Column(types.Integer, nullable=False, default=0)
    
    modified = Column(types.DateTime, default=datetime.datetime.utcnow)
    created = Column(types.DateTime, default=datetime.datetime.utcnow)



class FooterBanner(DomainObject, BaseModel, FooterBaseModelForInstances):
    __tablename__ = 'cms_footer_banner'

    id = Column(types.UnicodeText, primary_key=True, default=make_uuid)
    
    title_en = Column(types.UnicodeText, nullable=False, default='')
    title_ar = Column(types.UnicodeText, nullable=False, default='')
    link_en = Column(types.UnicodeText, nullable=False, default='')
    link_ar  = Column(types.UnicodeText, nullable=False, default='')
    image_url  = Column(types.UnicodeText, nullable=False, default='')
    
    order  = Column(types.Integer, nullable=False, default=0)
    
    modified = Column(types.DateTime, default=datetime.datetime.utcnow)
    created = Column(types.DateTime, default=datetime.datetime.utcnow)
