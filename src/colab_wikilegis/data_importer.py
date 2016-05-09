
from colab.plugins.data import PluginDataImporter


class ColabWikilegisPluginDataImporter(PluginDataImporter):
    app_label = 'colab_wikilegis'

    def fetch_data(self):
        pass
