from django.conf.urls import *

import handouts.views

# place app url patterns here
urlpatterns = patterns('handouts.views',
    url(r'detail/(?P<pk>\d+)/', handouts.views.HandoutDetail.as_view(),
        name='handout_detail'),
    url(r'dag/(?P<pk>\d+)/', handouts.views.HandoutDAG.as_view(), name='handout_dag'),
    url(r'', handouts.views.HandoutList.as_view(),
        name='handout_list'),
    )
