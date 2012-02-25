from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", "facts.views.index", name="home"),
    url(r"^dongs/", include(admin.site.urls)),
    url(r"^sms", "facts.views.add_number", name="addNumber"),
    url(r"^call", "facts.views.tell_fact", name="tellFact"),

)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
