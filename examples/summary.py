from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.Qt import QApplication
import sys

import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from entrywidget import AutoColorLineEdit, EntryWidget


# <editor-fold desc="helper functions, read their doc strings for reference">
def check_error_typed(widget):
    """Returns 'ERROR' if widget.text() == 'error', False otherwise"""
    print('check_error_typed: ', widget.text())
    if widget.text() == 'error':
        return 'ERROR'
    return False

def change_color_on_option(widget):
    """Uses widget.setManualColors() to change QLineEdit colors to (widget.getSelected(), 'black')"""
    print('change_color to', widget.getSelected())
    widget.setManualColors((widget.getSelected(), 'black'))

def check_text_matches_option(widget):
    """Compares widget.text() and widget.getSelected(), returns if they are =="""
    return widget.text() == widget.getSelected()

def print_whatever(*args):
    """Prints whatever comes in"""
    print('print_whatever:', args)
# </editor-fold>


# start Qt stuff
app = QApplication([])

# main window, there are other ways to make this
window = QWidget()
# put a vertical layout in the window
layout = QVBoxLayout(window)

# QLineEdit that changes color automatically
autocolor = AutoColorLineEdit(window, text='AutoColorLineEdit', errorCheck=check_error_typed)
autocolor.hasError.connect(lambda: print('!! ERROR !!'))
autocolor.errorCleared.connect(lambda: print(':) NO MORE ERROR :)'))

# AutoColorLineEdit and a DictComboBox
entry = EntryWidget(window, text='EntryWidget',
                    options={'a':'data A', 'b':'data B', 'c':'data C'},
                    errorCheck=check_text_matches_option)
entry.optionChanged[str].connect(print_whatever)
entry.dataChanged[object].connect(print_whatever)

# add widgets to layout
layout.addWidget(autocolor)
layout.addWidget(entry)

# show things
window.show()
app.exec_()
