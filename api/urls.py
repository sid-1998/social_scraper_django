from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^codechef/$', views.codechef, name='codechef'),
    url(r'^delCodechef/$', views.delCodechef, name='delCodechef'),
    url(r'^delQuora/$', views.delQuora, name='delQuora'),
    url(r'^stats/$', views.stats, name='stats'),
    url(r'^quora/$', views.quora, name='quora'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]
