import pytest

from entrywidget import EntryWidget
import sys

# Qt stuff
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)

# logging stuff
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# <editor-fold desc="Support Funcs">
def change_label_on_typing(entry_widget):
    entry_widget.setLabel(entry_widget.text())

def change_color_on_option(entry_widget):
    print('change_color to', entry_widget.getSelected())
    entry_widget.setColors((entry_widget.getSelected(), 'black'))
# </editor-fold>


print("\n----------------------- Default")
widget = EntryWidget()
widget.setWindowTitle('Default')
widget.show()
app.exec_()

print("\n----------------------- Standard Usage")
widget = EntryWidget(label='Enter Data:', options=['opt1', 'opt2', 'opt3'], text='Prompt Text')
widget.setWindowTitle('Standard usage')
widget.show()
app.exec_()

print("\n----------------------- Updating Label")
widget = EntryWidget(label='Type here -->', text='type here')
widget.textChanged.connect(lambda: change_label_on_typing(widget))
widget.setWindowTitle('Change Label')
widget.show()
app.exec_()

print("\n----------------------- Select a Color")
widget = EntryWidget(label='pick a color', options=['white', 'red', 'blue', 'orange'])
widget.optionChanged.connect(lambda: change_color_on_option(widget))
widget.setWindowTitle('Select a Color')
widget.show()
app.exec_()
