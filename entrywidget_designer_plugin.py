from qt_utils.designer import WidgetPluginFactory

from entrywidget import \
    AutoColorLineEdit, EntryWidget, LabelLineEdit, ButtonLineEdit, ButtonEntryWidget

AutoColorLineEditPlugin = WidgetPluginFactory(AutoColorLineEdit, toolTip='QLineEdit with automatic colors')
LabelLineEditPlugin = WidgetPluginFactory(LabelLineEdit, toolTip='QLabel and AutoColorLineEdit')
ButtonLabelLineEditPlugin = WidgetPluginFactory(ButtonLineEdit, toolTip='QPushButton and AutoColorLineEdit')
EntryWidgetPlugin = WidgetPluginFactory(EntryWidget, toolTip='LabelLineEdit and QComboBox')
ButtonEntryWidgetPlugin = WidgetPluginFactory(ButtonEntryWidget, toolTip='ButtonLineEdit and QComboBox')

