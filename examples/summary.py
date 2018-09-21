from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.Qt import QApplication
from PyQt5 import QtCore  # for mouse click events

from entryWidget import AutoColorLineEdit, LabelLineEdit, EntryWidget

# import sys, logging
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)

##################
# helper functions, read their doc strings for reference

def check_error_typed(widget, *args, **kwargs):
    """Returns 'ERROR' if widget.text() == 'error', False otherwise"""
    print('check_error_typed')
    if widget.text() == 'error':
        return 'ERROR'
    return False

def show_mouse_click(widget, event, *args, **kwargs):
    """Uses widget.setText() to show if mouse click was Left or Right Click"""
    if event.button() == QtCore.Qt.LeftButton:
        widget.setText('Left Click')
    elif event.button() == QtCore.Qt.RightButton:
        widget.setText('Right Click')

def change_color_on_option(widget, *args, **kwargs):
    """Uses widget.setColors() to change QLineEdit colors to (widget.getSelected(), 'black')"""
    print('change_color')
    widget.setColors((widget.getSelected(), 'black'))

# end helper functions
##################


# start Qt stuff
app = QApplication([])

# main window, there are other ways to make this
window = QWidget()
# put a vertical layout in the window
layout = QVBoxLayout(window)

# QLineEdit that changes color automatically (base for the other widgets shown here)
autocolor = AutoColorLineEdit(window, startPrompt='AutoColor', isError=check_error_typed)

# AutoColorLineEdit with a QLabel
labeledit = LabelLineEdit(window, label='Click Here', startPrompt='LabelLineEdit', onLabelClick=show_mouse_click)

# AutoColorLineEdit, QLabel, and a QComboBox
entry = EntryWidget(window, label="EntryWidget", startPrompt='pick a color',
                    options=['red', 'blue', 'orange'], onOptionChanged=change_color_on_option)


layout.addWidget(autocolor)
layout.addWidget(labeledit)
layout.addWidget(entry)

window.setLayout(layout)

window.show()
app.exec_()
