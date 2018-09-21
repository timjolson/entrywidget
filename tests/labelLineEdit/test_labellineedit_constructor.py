import pytest
from generalUtils.helpers_for_tests import *
from entryWidget import LabelLineEdit
from entryWidget.utils import getCurrentColor
import sys

# Qt stuff
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

# logging stuff
import logging

# logging.basicConfig(stream=sys.stdout, filename='/logs/LabelLineEdit.log', level=logging.INFO)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = QApplication(sys.argv)

def test_basic_open(qtbot):
    widget = LabelLineEdit()
    show(locals())


def test_constructor_label(qtbot):
    widget = LabelLineEdit(label=test_strings[1])
    show(locals())
    assert widget.getLabel() == test_strings[1]
    assert widget._label.text() == test_strings[1]


def test_constructor_onLabelClick(qtbot):
    widget = LabelLineEdit(onLabelClick=lock_unlock_entry_mouse)
    show(locals())

    qtbot.mouseClick(widget._label, QtCore.Qt.LeftButton)
    assert widget._editBox.isReadOnly() is True
    assert widget.isReadOnly() is True
    qtbot.mouseClick(widget._label, QtCore.Qt.RightButton)
    assert widget._editBox.isReadOnly() is False
    assert widget.isReadOnly() is False


def test_embed_widgets(qtbot):
    from PyQt5.QtWidgets import QVBoxLayout, QWidget
    window = QWidget()
    layout = QVBoxLayout(window)
    layout.addWidget(LabelLineEdit())
    layout.addWidget(LabelLineEdit())
    window.setLayout(layout)
    show({'qtbot':qtbot, 'widget':window})
