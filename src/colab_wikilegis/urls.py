
from django.conf.urls import patterns, url

from .views import ColabWikilegisPluginProxyView

urlpatterns = patterns('',
    url(r'^(?P<path>.*)$', ColabWikilegisPluginProxyView.as_view(),
        name='colab_wikilegis'),
)
