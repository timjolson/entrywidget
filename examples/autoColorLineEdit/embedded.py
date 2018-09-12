from entryWidget import AutoColorLineEdit
from PyQt5.Qt import QApplication
import sys
import logging
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTextEdit

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = QApplication(sys.argv)


def detect_error(w):
    return w.text() == 'error'

def announce_error(w):
    print(w.name + 'There is an Error')

def print_entered_text(w):
    print(w.name + "Text is: '"+ w.text() + "'")

def do_whats_typed(w):
    if w.text() == 'auto':
        print(w.name + "Changing to Automatic colors")
        w.setAutoColors()
    if w.text() == 'manual':
        print(w.name + "Changing to Manual colors")
        w.setColors(('black', 'white'))
    if w.text() == 'readonly':
        w.setReadOnly(True)
        print(w.name + 'Entry is ReadOnly')
    if w.text() == 'disable':
        w.setEnabled(False)
        print(w.name + 'Entry is Disabled')
    if w.text() == 'close':
        print(w.name + 'Closing Window')
        w.window().close()


print("----------------------- Default")
widgetDefault = AutoColorLineEdit()
widgetDefault.setObjectName('widgetDefault')

print("----------------------- widget0")
widget0 = AutoColorLineEdit(
    objectName='widget0',  # object name inside Qt, also can be used for logging
    startPrompt='startPrompt',  # box's text on startup
    liveErrorChecking=True,  # whether to run isError() every text change, or only when editing is finished
    isError=detect_error,  # function to run that returns an error status :: bool(isError())==False -> no error
    onError=announce_error,  # function to run when the error status is True
    onTextChanged=print_entered_text,  # function to run each time the text is changed
    onEditingFinished=do_whats_typed,  # function to run when Enter/Tab pressed or widget no longer has Focus
    readOnly=False  # whether the text box is readOnly or not
)
widget0.setToolTip(
    """Typing anything causes:
    error checking (liveErrorChecking=True)
    log the new text (onTextChanged=...)
    
    Typing 'error' causes:
    box to have error (isError=...)
    log the error (onError=...)
    
    Typing 'close', 'readonly', or 'disable' and pressing RETURN/ENTER:
    closes the window ; makes box readonly ; disables box entirely
    (onEditingFinished=...)
    """
)

print("----------------------- widget1")
widget1 = AutoColorLineEdit(
    objectName='widget1',
    isError=detect_error,
    onError=announce_error,
    onEditingFinished=print_entered_text
)
widget1.setToolTip("Typing anything causes error checking (liveErrorChecking=True)\n\nTyping")

print("----------------------- widget2")
widget2 = AutoColorLineEdit(
    objectName='widget 2',
    startPrompt='error',
    isError=detect_error,
    onError=announce_error,
    onEditingFinished=do_whats_typed,
    liveErrorChecking=False
)

print("----------------------- widget3")
widget3 = AutoColorLineEdit(
    startPrompt="custom colors, type 'error' to close",
    isError=detect_error,
    onTextChanged=do_whats_typed,
    onEditingFinished=do_whats_typed,
    liveErrorChecking=False
)
widget3.setColors(('black', 'white'))
widget3.setObjectName('widget 3')

print("----------------------- Make Window")
window = QWidget()
window.setObjectName('main window')
layout = QVBoxLayout(window)
layout.addWidget(widgetDefault)
layout.addWidget(widget0)
layout.addWidget(widget1)
layout.addWidget(widget2)
layout.addWidget(widget3)

info = QTextEdit(
    """Type 'error' to see each box's reaction.
    Type 'auto' to change the box to automatic colors.
    Type 'manual' to change the box to manual colors.
    Type 'fixed' to make the box readonly.
    Type 'disabled' to disable the box.
    Type 'close' to close the window.
    """, window)
info.setReadOnly(True)
layout.addWidget(info)

window.setLayout(layout)
window.show()
app.exec_()
