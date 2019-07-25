from qt_utils.designer import WidgetPluginFactory

from entrywidget import AutoColorLineEdit, EntryWidget

AutoColorLineEditPlugin = WidgetPluginFactory(AutoColorLineEdit, toolTip='QLineEdit with automatic colors')
EntryWidgetPlugin = WidgetPluginFactory(EntryWidget, toolTip='AutoColorLineEdit and DictComboBox')
