


from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^upload_ranks/$', views.rank.as_view()),
    url(r'^get_ranks/(?P<pk>\d+)$', views.ranks.as_view()),
    url(r'^get_ranks/$', views.rank.as_view()),


]