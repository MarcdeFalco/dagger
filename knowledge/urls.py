from django.conf.urls import *

import knowledge.views

# place app url patterns here
urlpatterns = patterns('knowledge.views',
    url(r'detail/(?P<pk>\d+)/', knowledge.views.AtomDetail.as_view(),
        name='atom_detail'),
    url(r'bulk/export/', knowledge.views.AtomBulkExport.as_view(), 
        name='atom_bulk_export'),
    url(r'bulk/import/', knowledge.views.AtomBulkImport.as_view(),
        name='atom_bulk_import'),
    url(r'dag', knowledge.views.AtomDAG.as_view(), name='atom_dag'),
    url(r'', knowledge.views.Home.as_view(), name='home'),
    )
