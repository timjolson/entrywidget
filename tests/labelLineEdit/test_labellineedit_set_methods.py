import pytest
from entryWidget import LabelLineEdit
from generalUtils.helpers_for_tests import *
from generalUtils import getCurrentColor
import sys

# Qt stuff
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

# logging stuff
import logging

# logging.basicConfig(stream=sys.stdout, filename='/logs/LabelLineEdit.log', level=logging.INFO)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = QApplication(sys.argv)


def test_setLabel(qtbot):
    widget = LabelLineEdit()
    show(locals())
    widget.setLabel(test_strings[1])
    assert widget.getLabel() == test_strings[1]
    assert widget._label.text() == test_strings[1]


def test_setOnLabelClick(qtbot):
    widget = LabelLineEdit()
    show(locals())
    widget.setOnLabelClick(lock_unlock_entry_mouse)

    qtbot.mouseClick(widget._label, QtCore.Qt.LeftButton)
    assert widget._editBox.isReadOnly() is True
    assert widget.isReadOnly() is True
    qtbot.mouseClick(widget._label, QtCore.Qt.RightButton)
    assert widget._editBox.isReadOnly() is False
    assert widget.isReadOnly() is False


def test_setOnTextChanged(qtbot):
    widget = LabelLineEdit()
    show(locals())
    widget.setOnTextChanged(change_label_on_typing)

    qtbot.keyClick(widget._editBox, 'a')
    assert widget._editBox.text() == 'a'
    assert widget.text() == 'a'
    assert widget._label.text() == 'a'
    assert widget.getLabel() == 'a'

    qtbot.keyClick(widget._editBox, 'b')
    assert widget._editBox.text() == 'ab'
    assert widget.text() == 'ab'
    assert widget._label.text() == 'ab'
    assert widget.getLabel() == 'ab'

    widget.setText(test_strings[0])
    assert widget._editBox.text() == test_strings[0]
    assert widget.text() == test_strings[0]
    assert widget._label.text() == test_strings[0]
    assert widget.getLabel() == test_strings[0]


def test_setOnEditingFinished(qtbot):
    widget = LabelLineEdit(label=test_strings[0])
    show(locals())
    widget.setOnEditingFinished(change_label_on_typing)

    qtbot.keyClick(widget._editBox, 'a')
    assert widget._editBox.text() == 'a'
    assert widget.text() == 'a'
    assert widget._label.text() == test_strings[0]
    assert widget.getLabel() == test_strings[0]
    qtbot.keyClick(widget._editBox, 'b')
    assert widget._editBox.text() == 'ab'
    assert widget.text() == 'ab'
    assert widget._label.text() == test_strings[0]
    assert widget.getLabel() == test_strings[0]

    qtbot.keyPress(widget._editBox, QtCore.Qt.Key_Return)
    assert widget._editBox.text() == 'ab'
    assert widget.text() == 'ab'
    assert widget._label.text() == 'ab'
    assert widget.getLabel() == 'ab'

    widget.setText(test_strings[0])
    assert widget._editBox.text() == test_strings[0]
    assert widget.text() == test_strings[0]
    assert widget._label.text() == test_strings[0]
    assert widget.getLabel() == test_strings[0]

