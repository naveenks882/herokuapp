from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()
from . import views


# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', views.index),
    url(r'^getdata/$', views.getdata),
]
