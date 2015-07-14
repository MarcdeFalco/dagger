from django.contrib import admin
from knowledge.models import *

from django.http import HttpResponseRedirect

class AtomAdmin(admin.ModelAdmin):
    def response_change(self, request, obj):
        """ if user clicked "edit this page", return back to main site """
        response = super(AtomAdmin, self).response_change(request, obj)

        if (isinstance(response, HttpResponseRedirect) and
                #response['location'] == '../' and
                request.GET.get('source') == 'main'):
            response['location'] = obj.get_absolute_url()

        return response

admin.site.register(Atom, AtomAdmin)
admin.site.register(AtomType)
admin.site.register(AtomRelationshipType)
admin.site.register(AtomRelationship)
admin.site.register(AtomOrphanRelationship)
