
from colab.plugins.utils.apps import ColabPluginAppConfig


class WikilegisAppConfig(ColabPluginAppConfig):
    name = 'colab_wikilegis'
    verbose_name = 'Colab Wikilegis Plugin'
    short_name = 'wikilegis'
    namespace = 'wikilegis'
