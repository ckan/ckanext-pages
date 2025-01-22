import datetime
import uuid
import json
from ckan.model import DomainObject
from six import text_type
import sqlalchemy as sa
from sqlalchemy import Column, types
from sqlalchemy.orm import class_mapper
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

pages_table = None

def make_uuid():
    return text_type(uuid.uuid4())


class Page(DomainObject, BaseModel):
    __tablename__ = "ckanext_pages"

    id = Column(types.UnicodeText, primary_key=True, default=make_uuid)
    title_en = Column(types.UnicodeText, default=u'')
    title_ar = Column(types.UnicodeText, default=u'')
    name = Column(types.UnicodeText, default=u'', nullable=False)
    content_en = Column(types.UnicodeText, default=u'')
    content_ar = Column(types.UnicodeText, default=u'')
    image_url = Column(types.UnicodeText, default=u'')
    lang = Column(types.UnicodeText, default=u'')
    order = Column(types.UnicodeText, default=u'')
    private = Column(types.Boolean, default=True)
    group_id = Column(types.UnicodeText, default=None)
    user_id = Column(types.UnicodeText, default=u'')
    publish_date = Column(types.DateTime, default = datetime.datetime.utcnow)
    page_type = Column(types.UnicodeText)
    created = Column(types.DateTime, default=datetime.datetime.utcnow)
    modified = Column(types.DateTime, default=datetime.datetime.utcnow)
    extras = Column(types.UnicodeText, default=u'{}')
    hidden = Column(types.Boolean, default=False)


    @classmethod
    def get(cls, id=None):
        if id:
            return Session.query(cls).filter_by(id=id).first()
        return None

    @classmethod
    def pages(cls, **kw):
        '''Finds a single entity in the register.'''
        order = kw.pop('order', False)
        order_publish_date = kw.pop('order_publish_date', False)

        query = model.Session.query(cls).autoflush(False)
        query = query.filter_by(**kw)
        if order:
            query = query.order_by(sa.cast(cls.order, sa.Integer)).filter(cls.order != '')
        elif order_publish_date:
            query = query.order_by(cls.publish_date.desc()).filter(cls.publish_date != None)  # noqa: E711
        else:
            query = query.order_by(cls.created.desc())
        return query.all()

    def save(self):
        try:
            self.modified = datetime.datetime.utcnow()
            model.Session.add(self)
            model.Session.commit()
            print("Saved page with ID:", self.id)  # Debug: Confirm save
        except Exception as e:
            print("Error during saving:", str(e))  # Debug: Log errors
            raise e


class MainPage(DomainObject, BaseModel):
    __tablename__ = "main_page"

    id = Column(types.Integer, primary_key=True)
    main_title_1_ar = Column(types.UnicodeText, nullable=True)
    main_title_1_en = Column(types.UnicodeText, nullable=True)
    main_title_2_ar = Column(types.UnicodeText, nullable=True)
    main_title_2_en = Column(types.UnicodeText, nullable=True)
    main_brief_en = Column(types.UnicodeText, nullable=True)
    main_brief_ar = Column(types.UnicodeText, nullable=True)

    @classmethod
    def get(cls, **kw):
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw).first()

    @classmethod
    def all(cls):
        query = model.Session.query(cls).order_by(cls.id).autoflush(False)
        return query.all()

class Event(DomainObject, BaseModel):
    __tablename__ = 'events'
    id = Column(types.UnicodeText, primary_key=True, default=make_uuid)
    title_en = Column(types.UnicodeText, default=u'')
    title_ar = Column(types.UnicodeText, default=u'')
    name = Column(types.UnicodeText, default=u'', nullable=False)
    start_date = Column(types.DateTime, nullable=True)
    end_date = Column(types.DateTime, nullable=True)
    created = Column(types.DateTime, default=datetime.datetime.utcnow)
    brief_ar = Column(types.UnicodeText, nullable=True)
    brief_en = Column(types.UnicodeText, nullable=True)
    content_ar = Column(types.UnicodeText, default=u'')
    content_en = Column(types.UnicodeText, default=u'')
    image_url = Column(types.UnicodeText, default=u'')
    lang = Column(types.UnicodeText, default=u'')

    
    @classmethod
    def get(cls, id=None):
        if id:
            return Session.query(cls).filter_by(id=id).first()
        return None

    @classmethod
    def events(cls, **kw):
        order = kw.pop('order', False)
        order_start_date = kw.pop('order_start_date', False)

        query = model.Session.query(cls).autoflush(False)
        query = query.filter_by(**kw)
        if order:
            query = query.order_by(sa.cast(cls.order, sa.Integer)).filter(cls.order != '')
        elif order_start_date:
            query = query.order_by(cls.start_date.desc()).filter(cls.start_date != None)  # noqa: E711
        else:
            query = query.order_by(cls.created.desc())
        return query.all()

    def save(self):
        try:
            self.modified = datetime.datetime.utcnow()
            model.Session.add(self)
            model.Session.commit()
            print("Saved page with ID:", self.id)  # Debug: Confirm save
        except Exception as e:
            print("Error during saving:", str(e))  # Debug: Log errors
            raise e
    


class News(DomainObject, BaseModel):
    __tablename__ = 'news'
    id = Column(types.UnicodeText, primary_key=True, default=make_uuid)
    title_en = Column(types.UnicodeText, default=u'')
    title_ar = Column(types.UnicodeText, default=u'')
    name = Column(types.UnicodeText, default=u'', nullable=False)
    news_date = Column(types.DateTime)
    brief_ar = Column(types.UnicodeText, nullable=True)
    brief_en = Column(types.UnicodeText, nullable=True)
    content_ar = Column(types.UnicodeText, default=u'')
    content_en = Column(types.UnicodeText, default=u'')
    image_url = Column(types.UnicodeText, default=u'')
    lang = Column(types.UnicodeText, default=u'') 
    created = Column(types.DateTime, default=datetime.datetime.utcnow)
    hidden = Column(types.Boolean, default=False)

    

    @classmethod
    def get(cls, id=None):
        if id:
            return Session.query(cls).filter_by(id=id).first()
        return None

    @classmethod
    def news(cls, **kw):
        order = kw.pop('order', False)
        order_news_date = kw.pop('order_news_date', False)

        query = model.Session.query(cls).autoflush(False)
        query = query.filter_by(**kw)
        if order:
            query = query.order_by(sa.cast(cls.order, sa.Integer)).filter(cls.order != '')
        elif order_news_date:
            query = query.order_by(cls.news_date.desc()).filter(cls.news_date != None)  # noqa: E711
        else:
            query = query.order_by(cls.created.desc())
        return query.all()

    def save(self):
        try:
            self.modified = datetime.datetime.utcnow()
            model.Session.add(self)
            model.Session.commit()
            print("Saved page with ID:", self.id)  # Debug: Confirm save
        except Exception as e:
            print("Error during saving:", str(e))  # Debug: Log errors
            raise e
    

def table_dictize(obj, context, **kw):
    '''Get any model object and represent it as a dict'''
    result_dict = {}

    if isinstance(obj, Row):
        fields = obj.keys()
    else:
        ModelClass = obj.__class__
        table = class_mapper(ModelClass).mapped_table
        fields = [field.name for field in table.c]

    for field in fields:
        name = field
        if name in ('current', 'expired_timestamp', 'expired_id'):
            continue
        if name == 'continuity_id':
            continue
        value = getattr(obj, name)
        if name == 'extras' and value:
            result_dict.update(json.loads(value))
        elif value is None:
            result_dict[name] = value
        elif isinstance(value, dict):
            result_dict[name] = value
        elif isinstance(value, int):
            result_dict[name] = value
        elif isinstance(value, datetime.datetime):
            result_dict[name] = value.isoformat()
        elif isinstance(value, list):
            result_dict[name] = value
        else:
            result_dict[name] = text_type(value)

    result_dict.update(kw)

    context['metadata_modified'] = max(result_dict.get('revision_timestamp', ''),
                                       context.get('metadata_modified', ''))

    return result_dict

from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from ckan.plugins.toolkit import BaseModel

import logging
import sqlalchemy as sa
from ckan.common import config

log = logging.getLogger(__name__)


engine = sa.create_engine(config.get('sqlalchemy.url'))
Session = sessionmaker(bind=engine)()
BaseModel.metadata.create_all(engine)

def setup():
    inspector = inspect(engine)
    if not inspector.has_table('ckanext_pages'):
        BaseModel.metadata.tables['ckanext_pages'].create(engine)
        log.debug('pages table created')
    else:
        log.debug('pages table already exists')

        # Ensure the image_url column is of the correct type
        with engine.connect() as conn:
            result = conn.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'ckanext_pages' AND column_name = 'image_url'")
            column = result.fetchone()
            if column and column[1] != 'text':
                conn.execute("ALTER TABLE ckanext_pages ALTER COLUMN image_url TYPE TEXT USING image_url::TEXT")
                log.debug('image_url column type updated to TEXT')



def teardown():
    inspector = inspect(engine)
    if inspector.has_table('ckanext_pages'):
        table = BaseModel.metadata.tables.get('ckanext_pages')
        if table is not None:
            table.drop(engine)
            log.debug('pages table dropped')
        else:
            log.error('pages table not found in metadata')
    else:
        log.debug('pages table does not exist')


