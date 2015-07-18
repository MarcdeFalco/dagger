from django.conf.urls import *

import knowledge.views

# place app url patterns here
urlpatterns = patterns('knowledge.views',
    url(r'detail/(?P<pk>\d+)/', knowledge.views.AtomDetail.as_view(),
        name='atom_detail'),
    url(r'bulk/', knowledge.views.AtomBulkView.as_view(), name='atom_bulk'),
    url(r'', knowledge.views.AtomDAG.as_view(), name='atom_dag'),
    )
