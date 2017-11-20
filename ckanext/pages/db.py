import datetime
import uuid
import json

import sqlalchemy as sa
from sqlalchemy.orm import class_mapper
try:
    from sqlalchemy.engine.result import RowProxy
except:
    from sqlalchemy.engine.base import RowProxy

pages_table = None
Page = None


def make_uuid():
    return unicode(uuid.uuid4())


def init_db(model):
    class _Page(model.DomainObject):

        @classmethod
        def get(cls, **kw):
            '''Finds a single entity in the register.'''
            query = model.Session.query(cls).autoflush(False)
            return query.filter_by(**kw).first()

        @classmethod
        def pages(cls, **kw):
            '''Finds a single entity in the register.'''
            order = kw.pop('order', False)
            order_publish_date = kw.pop('order_publish_date', False)

            query = model.Session.query(cls).autoflush(False)
            query = query.filter_by(**kw)
            if order:
                query = query.order_by(cls.order).filter(cls.order != '')
            elif order_publish_date:
                query = query.order_by(cls.publish_date.desc()).filter(cls.publish_date != None)
            else:
                query = query.order_by(cls.created.desc())
            return query.all()

    global Page
    Page = _Page
    # We will just try to create the table.  If it already exists we get an
    # error but we can just skip it and carry on.
    sql = '''
                CREATE TABLE ckanext_pages (
                    id text NOT NULL,
                    title text,
                    name text,
                    content text,
                    lang text,
                    "order" text,
                    private boolean,
                    group_id text,
                    user_id text NOT NULL,
                    created timestamp without time zone,
                    modified timestamp without time zone
                );
    '''
    conn = model.Session.connection()
    try:
        conn.execute(sql)
    except sa.exc.ProgrammingError:
        pass
    model.Session.commit()

    sql_upgrade_01 = (
        "ALTER TABLE ckanext_pages add column publish_date timestamp;",
        "ALTER TABLE ckanext_pages add column page_type Text;",
        "UPDATE ckanext_pages set page_type = 'page';",
    )

    conn = model.Session.connection()
    try:
        for statement in sql_upgrade_01:
            conn.execute(statement)
    except sa.exc.ProgrammingError:
        pass
    model.Session.commit()

    sql_upgrade_02 = ('ALTER TABLE ckanext_pages add column extras Text;',
                      "UPDATE ckanext_pages set extras = '{}';")

    conn = model.Session.connection()
    try:
        for statement in sql_upgrade_02:
            conn.execute(statement)
    except sa.exc.ProgrammingError:
        pass
    model.Session.commit()

    sql_upgrade_03 = ('ALTER TABLE ckanext_pages add column image_url Text;',)

    conn = model.Session.connection()
    try:
        for statement in sql_upgrade_03:
            conn.execute(statement)
    except sa.exc.ProgrammingError as e:
        pass
    model.Session.commit()

    types = sa.types
    global pages_table
    pages_table = sa.Table('ckanext_pages', model.meta.metadata,
        sa.Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
        sa.Column('title', types.UnicodeText, default=u''),
        sa.Column('name', types.UnicodeText, default=u''),
        sa.Column('content', types.UnicodeText, default=u''),
        sa.Column('lang', types.UnicodeText, default=u''),
        sa.Column('order', types.UnicodeText, default=u''),
        sa.Column('private',types.Boolean,default=True),
        sa.Column('group_id', types.UnicodeText, default=None),
        sa.Column('user_id', types.UnicodeText, default=u''),
        sa.Column('publish_date', types.DateTime),
        sa.Column('page_type', types.DateTime),
        sa.Column('created', types.DateTime, default=datetime.datetime.utcnow),
        sa.Column('modified', types.DateTime, default=datetime.datetime.utcnow),
        sa.Column('extras', types.UnicodeText, default=u'{}'),
        sa.Column('image_url', types.UnicodeText, default=None),
        extend_existing=True
    )

    model.meta.mapper(
        Page,
        pages_table,
    )


def table_dictize(obj, context, **kw):
    '''Get any model object and represent it as a dict'''
    result_dict = {}

    if isinstance(obj, RowProxy):
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
            result_dict[name] = unicode(value)

    result_dict.update(kw)

    ##HACK For optimisation to get metadata_modified created faster.

    context['metadata_modified'] = max(result_dict.get('revision_timestamp', ''),
                                       context.get('metadata_modified', ''))

    return result_dict
