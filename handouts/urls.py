from django.conf.urls import *

import handouts.views

# place app url patterns here
urlpatterns = patterns('handouts.views',
    url(r'detail/(?P<pk>\d+)/tex', handouts.views.TexHandoutDetail.as_view(),
        name='handout_detail_tex'),
    url(r'detail/(?P<pk>\d+)/', handouts.views.HandoutDetail.as_view(),
        name='handout_detail'),
    url(r'dag/(?P<pk>\d+)/json/$', handouts.views.HandoutDAGjson.as_view(),
        name='handout_json'),
    url(r'dag/(?P<pk>\d+)/', handouts.views.HandoutDAG.as_view(), name='handout_dag'),
    url(r'', handouts.views.HandoutList.as_view(),
        name='handout_list'),
    )
