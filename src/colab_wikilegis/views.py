
from colab.plugins.views import ColabProxyView


class ColabWikilegisPluginProxyView(ColabProxyView):
    app_label = 'colab_wikilegis'
    diazo_theme_template = 'proxy/wikilegis.html'

    def get_proxy_request_headers(self, request):
        headers = super(ColabWikilegisPluginProxyView,
                        self).get_proxy_request_headers(request)

        if request.user.is_authenticated():
            headers["Auth-user"] = request.user.username

        return headers
