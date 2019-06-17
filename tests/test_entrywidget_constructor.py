import pytest
import sys

# test helpers
from qt_utils.helpers_for_tests import *
from qt_utils.helpers_for_qt_tests import *
from . import *

# color helpers
from qt_utils import getCurrentColor

# Qt stuff
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

# logging stuff
import logging

# logging.basicConfig(stream=sys.stdout, filename='/logs/EntryWidget.log', level=logging.INFO)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = QApplication(sys.argv)

def test_basic_open(qtbot):
    widget = EntryWidget()
    show(locals())


def test_constructor_readOnly(qtbot):
    widget = EntryWidget(readOnly=True)
    show(locals())
    assert widget._editBox.isReadOnly() is True
    assert widget.isReadOnly() is True
    assert widget._optionList.isEnabled() is True
    assert widget._optionFixed is False

    widget = EntryWidget(readOnly=False)
    show(locals())
    assert widget._editBox.isReadOnly() is False
    assert widget.isReadOnly() is False
    assert widget._optionList.isEnabled() is True
    assert widget._optionFixed is False


def test_constructor_options(qtbot):
    widget = EntryWidget(options=test_options_good)
    show(locals())
    assert widget.getOptions() == test_options_good
    assert widget.getSelected() == test_options_good[0]


def test_constructor_optionFixed(qtbot):
    widget = EntryWidget(optionFixed=True)
    show(locals())
    assert widget._optionList.isEnabled() is False
    assert widget._optionFixed is True

    widget = EntryWidget(optionFixed=False)
    show(locals())
    assert widget._optionList.isEnabled() is True
    assert widget._optionFixed is False


def test_constructor_onLabelClick(qtbot):
    widget = EntryWidget(onLabelClick=lock_unlock_option_mouse)
    show(locals())

    qtbot.mouseClick(widget._label, QtCore.Qt.LeftButton)
    assert widget._optionList.isEnabled() is False
    assert widget._optionFixed is True
    qtbot.mouseClick(widget._label, QtCore.Qt.RightButton)
    assert widget._optionList.isEnabled() is True
    assert widget._optionFixed is False


def test_constructor_onOptionChanged(qtbot):
    widget = EntryWidget(options=test_options_colors, onOptionChanged=change_color_on_option)
    show(locals())

    widget.setSelected(test_options_colors[1])
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_options_colors[1]

    widget.setSelected(test_options_colors[0])
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_options_colors[0]

    widget.setSelected(test_options_colors[2])
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_options_colors[2]


def test_embed_widgets(qtbot):
    from PyQt5.QtWidgets import QVBoxLayout, QWidget
    window = QWidget()
    layout = QVBoxLayout(window)
    layout.addWidget(EntryWidget())
    layout.addWidget(EntryWidget())
    window.setLayout(layout)
    show({'qtbot':qtbot, 'widget':window})
