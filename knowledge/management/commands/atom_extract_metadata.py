from django.core.management.base import BaseCommand
from knowledge.models import Atom
import docutils
from docutils import nodes, utils
from docutils.core import publish_doctree, publish_from_doctree, Publisher
import pprint
import re

from docutils.parsers.rst import directives, Directive, roles

class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        parser.add_argument('atom_id', type=int)

    def handle(self, *args, **options):
        k = Atom.objects.get(id=int(options['atom_id']))
        doctree = publish_doctree(source=k.text)
        print(doctree.ids)
        class Walker:
            def __init__(self, doc):
                self.document = doc
                self.fields = {}
            def dispatch_visit(self,x):
                #print(x, type(x))
                if isinstance(x, docutils.nodes.field):
                    field_name = x.children[0].rawsource
                    field_value = x.children[1].rawsource
                    self.fields[field_name]=field_value
        w = Walker(doctree)
        doctree.walk(w)
        # the collected fields I wanted
        #pprint.pprint(w.fields)
