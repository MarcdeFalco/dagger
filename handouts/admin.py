from django.contrib import admin
from handouts.models import *

# Register your models here.
admin.site.register(Handout)
admin.site.register(Paragraph)
admin.site.register(ParagraphContainsAtoms)
