from colab.widgets.widget_manager import WidgetManager
from colab_wikilegis.widgets.home_section import WikilegisHomeSectionWidget


WidgetManager.register_widget('home_section', WikilegisHomeSectionWidget())
