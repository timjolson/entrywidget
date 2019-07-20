# tester bot
import pytest
# e.g. qtbot.dostuff()

from entrywidget import EntryWidget
import sys

# Qt stuff
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)

# logging stuff
from os.path import abspath, dirname
import logging
localDir = abspath(dirname(__file__))

# logging.basicConfig(stream=sys.stdout, filename=localDir+'/logs/EntryWidget.log', level=logging.INFO)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# <editor-fold desc="Support Funcs">
def show_mouse_click(entry_widget, event):
    if event.button() == QtCore.Qt.LeftButton:
        entry_widget.setText('Left Click')
    elif event.button() == QtCore.Qt.RightButton:
        entry_widget.setText('Right Click')

def lock_unlock_entry_mouse(entry_widget, event):
    print('lock unlock entry')
    if event.button() == QtCore.Qt.LeftButton:
        entry_widget.setReadOnly(True)
    elif event.button() == QtCore.Qt.RightButton:
        entry_widget.setReadOnly(False)
    print('entry on mouse : ' + str(entry_widget._editBox.isEnabled()))

def lock_unlock_option_mouse(entry_widget, event):
    print('lock unlock option')
    if event.button() == QtCore.Qt.LeftButton:
        entry_widget.setOptionFixed(True)
    elif event.button() == QtCore.Qt.RightButton:
        entry_widget.setOptionFixed(False)
    print('option on mouse : ' + str(entry_widget._optionList.isEnabled()))

def change_label_on_typing(entry_widget):
    entry_widget.setLabel(entry_widget.text())

def change_color_on_option(entry_widget):
    print('change_color')
    entry_widget.setColors((entry_widget.getSelected(), 'black'))
# </editor-fold>


# <editor-fold desc="Testing EntryWidget">
print("\n----------------------- Default")
widget = EntryWidget()
widget.show()
app.exec_()

print("\n----------------------- Standard Usage")
widget = EntryWidget(label='Enter Data:', options=['opt1', 'opt2', 'opt3'], startPrompt='Prompt Text')
widget.setWindowTitle('standard mode')
widget.show()
app.exec_()

print("\n----------------------- Label Clicking")
widget = EntryWidget(label='click here', onLabelClick=show_mouse_click)
widget.setWindowTitle('show mouse clicks')
widget.show()
app.exec_()

print("\n----------------------- ReadOnly Entry")
widget = EntryWidget(label='click here', onLabelClick=lock_unlock_entry_mouse)
widget.setWindowTitle('lock entry')
widget.show()
app.exec_()

print("\n----------------------- ReadOnly Option")
widget = EntryWidget(label='click here', onLabelClick=lock_unlock_option_mouse)
widget.setWindowTitle('lock option')
widget.show()
app.exec_()

print("\n----------------------- Updating Label")
widget = EntryWidget(label='Type here -->', startPrompt='type here', onTextChanged=change_label_on_typing)
widget.setWindowTitle('change label')
widget.show()
app.exec_()

print("\n----------------------- Select a Color")
widget = EntryWidget(label='pick a color', options=['red', 'blue', 'orange'], onOptionChanged=change_color_on_option)
widget.show()
app.exec_()
# </editor-fold>
