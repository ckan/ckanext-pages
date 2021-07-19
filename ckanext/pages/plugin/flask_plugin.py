# -*- coding: utf-8 -*-

import ckan.plugins as p

from ckanext.pages.blueprint import pages as pages_blueprint
import ckanext.pages.cli as cli


class MixinPlugin(p.SingletonPlugin):

    p.implements(p.IBlueprint)
    p.implements(p.IClick)

    def get_blueprint(self):
        return [pages_blueprint]

    def get_commands(self):
        return cli.get_commands()
