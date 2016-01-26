from django.conf.urls import url
from Portfolio import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^contacts/$', views.contacts),
    url(r'^counter$', views.counter_views),
    url(r'^gallery/$', views.gallery),
    url(r'^gallery/signin$', views.signin),
    url(r'^gallery/signup$', views.signup),
    url(r'^gallery/signout$', views.signout),
    url(r'^gallery/confirm$', views.confirm),
    url(r'^gallery/add_comment', views.add_comment),
    url(r'^gallery/list_comment/(?P<photo_id>\d+)$', views.list_comment),
    url(r'^gallery/edit_comment/(?P<comment_id>\d+)/'
        r'(?P<action>edit|save|delete|rollback)$',
        views.edit_comment),
    url(r'^visits/$', views.visits_view),
    url(r'^history/(?P<user_id>\d+)$', views.history_view),
    url(r'^gallery/like/(?P<photo_id>\d+)$', views.like),
    url(r'^gallery/statistic.xml$', views.statistic),
]
