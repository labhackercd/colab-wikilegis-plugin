
from colab.plugins.data import PluginDataImporter


class ColabWikilegisPluginDataImporter(PluginDataImporter):
    app_label = 'colab_wikilegis_plugin'

    def fetch_data(self):
        pass
