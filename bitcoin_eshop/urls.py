from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'web.views.index'),
    url(r'^order/', 'web.views.order'),
    url(r'^update/', 'web.views.update'),
    url(r'^list/', 'web.views.list_all'),

    # Examples:
    # url(r'^$', 'bitcoin_eshop.views.home', name='home'),
    # url(r'^bitcoin_eshop/', include('bitcoin_eshop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )