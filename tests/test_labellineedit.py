import pytest
import sys

# test helpers
from qt_utils.helpers_for_tests import (show, change_label_on_typing)

# dicts/tuples/lists for color testing (from __init__.py)
from . import *

# class to test
from entrywidget import LabelLineEdit

# Qt stuff
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

# logging stuff
import logging

# logging.basicConfig(stream=sys.stdout, filename='/logs/EntryWidget.log', level=logging.INFO)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
app = QApplication(sys.argv)



def test_constructor_basic(qtbot):
    widget = LabelLineEdit()
    show(locals())


def test_constructor_label(qtbot):
    widget = LabelLineEdit(label=test_strings[1])
    show(locals())
    assert widget.getLabel() == test_strings[1]
    assert widget.label.text() == test_strings[1]


def test_setLabel(qtbot):
    widget = LabelLineEdit()
    show(locals())
    widget.setLabel(test_strings[1])
    assert widget.getLabel() == test_strings[1]
    assert widget.label.text() == test_strings[1]


def test_textChanged(qtbot):
    widget = LabelLineEdit()
    show(locals())
    widget.textChanged.connect(lambda: change_label_on_typing(widget))

    qtbot.keyClick(widget, 'a')
    assert widget.text() == 'a'
    assert widget.text() == 'a'
    assert widget.label.text() == 'a'
    assert widget.getLabel() == 'a'

    qtbot.keyClick(widget, 'b')
    assert widget.text() == 'ab'
    assert widget.text() == 'ab'
    assert widget.label.text() == 'ab'
    assert widget.getLabel() == 'ab'

    widget.setText(test_strings[0])
    assert widget.text() == test_strings[0]
    assert widget.text() == test_strings[0]
    assert widget.label.text() == test_strings[0]
    assert widget.getLabel() == test_strings[0]


def test_editingFinished(qtbot):
    widget = LabelLineEdit(label=test_strings[0])
    show(locals())
    widget.editingFinished.connect(lambda: change_label_on_typing(widget))

    qtbot.keyClick(widget, 'a')
    assert widget.text() == 'a'
    assert widget.text() == 'a'
    assert widget.label.text() == test_strings[0]
    assert widget.getLabel() == test_strings[0]
    qtbot.keyClick(widget, 'b')
    assert widget.text() == 'ab'
    assert widget.text() == 'ab'
    assert widget.label.text() == test_strings[0]
    assert widget.getLabel() == test_strings[0]

    qtbot.keyPress(widget, QtCore.Qt.Key_Return)
    assert widget.text() == 'ab'
    assert widget.text() == 'ab'
    assert widget.label.text() == 'ab'
    assert widget.getLabel() == 'ab'

    widget.setText(test_strings[0])
    assert widget.text() == test_strings[0]
    assert widget.text() == test_strings[0]
    assert widget.label.text() == test_strings[0]
    assert widget.getLabel() == test_strings[0]


def test_embed_widgets(qtbot):
    from PyQt5.QtWidgets import QVBoxLayout, QWidget
    window = QWidget()
    layout = QVBoxLayout(window)
    layout.addWidget(LabelLineEdit())
    layout.addWidget(LabelLineEdit())
    window.setLayout(layout)
    show({'qtbot':qtbot, 'widget':window})
