from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
	#��ʵ��û��д
    url(r'^$', 'web.views.home', name='home'),
	#�����ϴ�ͼƬ
    url(r'^upload/$', 'recognizer.views.upload', name='upload'),
	url(r'^register/$', 'recognizer.views.user_register', name="register"),
	url(r'^login/$', 'recognizer.views.user_login', name='login'),
	url(r'^logout/$', 'recognizer.views.user_logout', name='logout'),
	# url(r'^web/', include('web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)