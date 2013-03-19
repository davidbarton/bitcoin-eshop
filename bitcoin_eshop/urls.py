from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'web.views.index'),
    url(r'^order/', 'web.views.order'),
    url(r'^checkout/', 'web.views.checkout'),
    url(r'^add/', 'web.views.add'),

    # Examples:
    # url(r'^$', 'bitcoin_eshop.views.home', name='home'),
    # url(r'^bitcoin_eshop/', include('bitcoin_eshop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
