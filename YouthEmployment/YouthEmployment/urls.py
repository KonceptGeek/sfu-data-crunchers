from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'YouthEmployment.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('youth_employment.urls'))
)
