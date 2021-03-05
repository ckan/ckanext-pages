# -*- coding: utf-8 -*-

import ckan.plugins as p

from ckanext.pages.blueprint import pages as pages_blueprint


class MixinPlugin(p.SingletonPlugin):

    p.implements(p.IBlueprint)

    def get_blueprint(self):
        return [pages_blueprint]
