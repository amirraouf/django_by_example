from django.conf.urls import url
from . import views
urlpatterns = [
# post views
	url(r'^$',views.home,name='home'),
	url(r'^(?P<slug>[-\w]+)/$', views.post_detail, name = 'post_detail'),
	url(r'^(?P<post_id>\d+)/share/$', views.post_share,name='post_share'),
	url(r'^tag/(?P<tag_slug>[-\w]+)/$',views.home, name='post_list_by_tag'),
]