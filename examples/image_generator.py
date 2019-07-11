from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.Qt import QApplication
from entryWidget import AutoColorLineEdit, LabelLineEdit, EntryWidget, ButtonLineEdit, ButtonEntryWidget

app = QApplication([])

window = QWidget()
window.setWindowTitle('EntryWidget examples')
layout = QVBoxLayout(window)

autocolor = AutoColorLineEdit(window, text='AutoColorLineEdit')
labeledit = LabelLineEdit(window, label='QLabel', text='AutoColorLineEdit')
buttonlineedit = ButtonLineEdit(window, label='QPushButton', text='AutoColorLineEdit')
entry = EntryWidget(window, label="QLabel", text='AutoColorLineEdit', options=['QComboBox'])
buttonentry = ButtonEntryWidget(window, label="QPushButton", text='AutoColorLineEdit', options=['QComboBox'])


layout.addWidget(autocolor)
layout.addWidget(labeledit)
layout.addWidget(buttonlineedit)
layout.addWidget(entry)
layout.addWidget(buttonentry)

window.setLayout(layout)
window.show()
app.exec_()
