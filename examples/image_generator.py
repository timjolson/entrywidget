from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.Qt import QApplication
from entryWidget import AutoColorLineEdit, LabelLineEdit, EntryWidget

app = QApplication([])

window = QWidget()
window.setWindowTitle('Window')
layout = QVBoxLayout(window)

autocolor = AutoColorLineEdit(window, startPrompt='QLineEdit')
labeledit = LabelLineEdit(window, label='QLabel', startPrompt='QLineEdit')
entry = EntryWidget(window, label="QLabel", startPrompt='QLineEdit', options=['QComboBox'])
entry._optionList.setMinimumWidth(90)

layout.addWidget(autocolor)
layout.addWidget(labeledit)
layout.addWidget(entry)

window.setLayout(layout)
window.show()
app.exec_()
