from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'request/$', views.SongRequest.as_view(), name='api-task-complete'),
    url(r'check/$', views.CheckRequest.as_view(), name='api-task-check'),
    url(r'stop/$', views.StopRequest.as_view(), name='api-task-stop'),

]