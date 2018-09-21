import pytest
from entryWidget import EntryWidget
from generalUtils.helpers_for_tests import *
from entryWidget.utils import getCurrentColor
import sys

# Qt stuff
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

# logging stuff
import logging

# logging.basicConfig(stream=sys.stdout, filename='/logs/EntryWidget.log', level=logging.INFO)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = QApplication(sys.argv)


def test_setReadOnly(qtbot):
    widget = EntryWidget()
    show(locals())
    widget.setReadOnly(True)
    assert widget._editBox.isReadOnly() is True
    assert widget.isReadOnly() is True
    assert widget._optionList.isEnabled() is True
    assert widget._optionFixed is False

    widget.setReadOnly(False)
    assert widget._editBox.isReadOnly() is False
    assert widget.isReadOnly() is False
    assert widget._optionList.isEnabled() is True
    assert widget._optionFixed is False


def test_setEnabled(qtbot):
    widget = EntryWidget()
    show(locals())
    widget.setEnabled(False)
    assert widget._editBox.isEnabled() is False
    assert widget.isReadOnly() is False
    assert widget._optionList.isEnabled() is False
    assert widget._optionFixed is True

    widget.setEnabled(True)
    assert widget._editBox.isEnabled() is True
    assert widget.isReadOnly() is False
    assert widget._optionList.isEnabled() is True
    assert widget._optionFixed is False


def test_setOptions(qtbot):
    widget = EntryWidget()
    show(locals())
    widget.setOptions(test_options_good)
    assert widget.getOptions() == test_options_good
    assert widget.getSelected() == test_options_good[0]


def test_setFixedOption(qtbot):
    widget = EntryWidget()
    show(locals())
    widget.setOptionFixed(True)
    assert widget._optionList.isEnabled() is False
    assert widget._optionFixed is True

    widget = EntryWidget()
    show(locals())
    widget.setOptionFixed(False)
    assert widget._optionList.isEnabled() is True
    assert widget._optionFixed is False


def test_setOnLabelClick(qtbot):
    widget = EntryWidget()
    widget.setOnLabelClick(lock_unlock_option_mouse)
    show(locals())

    qtbot.mouseClick(widget._label, QtCore.Qt.LeftButton)
    assert widget._optionList.isEnabled() is False
    assert widget._optionFixed is True
    qtbot.mouseClick(widget._label, QtCore.Qt.RightButton)
    assert widget._optionList.isEnabled() is True
    assert widget._optionFixed is False


def test_setOnOptionChanged(qtbot):
    widget = EntryWidget(options=test_options_colors)
    show(locals())
    widget.setOnOptionChanged(change_color_on_option)

    widget.setSelected(test_options_colors[1])
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_options_colors[1]

    widget.setSelected(test_options_colors[0])
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_options_colors[0]

    widget.setSelected(test_options_colors[2])
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_options_colors[2]

