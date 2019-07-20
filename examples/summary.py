from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.Qt import QApplication
import sys

import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from entrywidget import AutoColorLineEdit, LabelLineEdit, EntryWidget, ButtonLineEdit, ButtonEntryWidget


# <editor-fold desc="helper functions, read their doc strings for reference">
def check_error_typed(widget):
    """Returns 'ERROR' if widget.text() == 'error', False otherwise"""
    print('check_error_typed: ', widget.text())
    if widget.text() == 'error':
        return 'ERROR'
    return False

def show_mouse_click(widget):
    """Uses widget.setText() to show if mouse click was Left or Right Click"""
    widget.setText('clicked')

def change_color_on_option(widget):
    """Uses widget.setColors() to change QLineEdit colors to (widget.getSelected(), 'black')"""
    print('change_color to', widget.getSelected())
    widget.setColors((widget.getSelected(), 'black'))

def check_text_matches_option(widget):
    """Compares widget.text() and widget.getSelected(), returns if they are =="""
    return widget.text() == widget.getSelected()

def set_label_to_data(widget):
    """Uses widget.setLabel() to show selected option's data from widget.currentData()"""
    widget.setLabel(widget.currentData())
# </editor-fold>


# start Qt stuff
app = QApplication([])

# main window, there are other ways to make this
window = QWidget()
# put a vertical layout in the window
layout = QVBoxLayout(window)

# QLineEdit that changes color automatically (base for the other widgets shown here)
autocolor = AutoColorLineEdit(window, text='AutoColorLineEdit')
autocolor.errorCheck = lambda: check_error_typed(autocolor)

# AutoColorLineEdit with a QLabel
labeledit = LabelLineEdit(window, label='Label', text='LabelLineEdit', liveErrorChecking=False)
labeledit.errorCheck = lambda: check_error_typed(labeledit)

# AutoColorLineEdit, QLabel, and a QComboBox
entry = EntryWidget(window, label="Label", text='EntryWidget',
                    options={'a':'data A', 'b':'data B', 'c':'data C'})
entry.errorCheck = lambda: check_text_matches_option(entry)
entry.optionChanged.connect(lambda: set_label_to_data(entry))

# AutoColorLineEdit with a QPushButton
buttonedit = ButtonLineEdit(window, label='Click here', text='ButtonLineEdit')
buttonedit.clicked.connect(lambda : show_mouse_click(buttonedit))

# AutoColorLineEdit, QPushButton, and a QComboBox
buttonentry = ButtonEntryWidget(window, label='red',
                                options=['white', 'red', 'blue', 'orange'], text='ButtonEntryWidget')
buttonentry.optionChanged.connect(lambda : change_color_on_option(buttonentry))
buttonentry.clicked.connect(lambda : buttonentry.setSelected('red'))

# add widgets to layout
layout.addWidget(autocolor)
layout.addWidget(labeledit)
layout.addWidget(entry)
layout.addWidget(buttonedit)
layout.addWidget(buttonentry)

# window.setLayout(layout)

# show things
window.show()
app.exec_()
