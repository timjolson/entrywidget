import pytest
import sys

# test helpers
from qt_utils.helpers_for_tests import (show, change_color_on_option, check_error_typed)

# dicts/tuples/lists for color testing (from __init__.py)
from . import *
# helpers
from qt_utils import getCurrentColor

# class to test
from entrywidget import EntryWidget

# Qt stuff
from PyQt5.QtWidgets import QApplication

# logging stuff
import logging

# logging.basicConfig(stream=sys.stdout, filename='/logs/EntryWidget.log', level=logging.INFO)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
app = QApplication(sys.argv)


def test_constructor_basic(qtbot):
    widget = EntryWidget()
    show(locals())


def test_constructor_readOnly(qtbot):
    widget = EntryWidget(readOnly=True)
    show(locals())
    assert widget.lineEdit.isReadOnly() is True
    assert widget.isReadOnly() is True
    assert widget.comboBox.isEnabled() is False
    assert widget.optionFixed() is True

    widget = EntryWidget(readOnly=False)
    show(locals())
    assert widget.lineEdit.isReadOnly() is False
    assert widget.isReadOnly() is False
    assert widget.comboBox.isEnabled() is True
    assert widget.optionFixed() is False


def test_constructor_options(qtbot):
    widget = EntryWidget(options=test_options_good)
    show(locals())
    assert widget.getOptions() == {k:k for k in test_options_good}
    assert widget.getSelected() == test_options_good[0]


def test_constructor_optionFixed(qtbot):
    widget = EntryWidget(optionFixed=True)
    show(locals())
    assert widget.comboBox.isEnabled() is False
    assert widget.optionFixed() is True

    widget = EntryWidget(optionFixed=False)
    show(locals())
    assert widget.comboBox.isEnabled() is True
    assert widget.optionFixed() is False


def test_embed_widgets(qtbot):
    from PyQt5.QtWidgets import QVBoxLayout, QWidget
    window = QWidget()
    layout = QVBoxLayout(window)
    layout.addWidget(EntryWidget())
    layout.addWidget(EntryWidget())
    window.setLayout(layout)
    show({'qtbot':qtbot, 'widget':window})


def test_setReadOnly(qtbot):
    widget = EntryWidget()
    show(locals())
    widget.setReadOnly(True)
    assert widget.lineEdit.isReadOnly() is True
    assert widget.isReadOnly() is True
    assert widget.comboBox.isEnabled() is False
    assert widget.optionFixed() is True

    widget.setReadOnly(False)
    assert widget.lineEdit.isReadOnly() is False
    assert widget.isReadOnly() is False
    assert widget.comboBox.isEnabled() is True
    assert widget.optionFixed() is False


def test_setEnabled(qtbot):
    widget = EntryWidget()
    show(locals())
    widget.setEnabled(False)
    assert widget.lineEdit.isEnabled() is False
    assert widget.isReadOnly() is True
    assert widget.comboBox.isEnabled() is False
    assert widget.optionFixed() is True

    widget.setEnabled(True)
    assert widget.lineEdit.isEnabled() is True
    assert widget.isReadOnly() is False
    assert widget.comboBox.isEnabled() is True
    assert widget.optionFixed() is False


def test_setOptions(qtbot):
    widget = EntryWidget()
    show(locals())
    widget.setOptions(test_options_good)
    assert widget.getOptions() == {k:k for k in test_options_good}
    assert widget.getSelected() == test_options_good[0]


def test_setFixedOption(qtbot):
    widget = EntryWidget()
    show(locals())
    widget.setOptionFixed(True)
    assert widget.comboBox.isEnabled() is False
    assert widget.optionFixed() is True

    widget = EntryWidget()
    show(locals())
    widget.setOptionFixed(False)
    assert widget.comboBox.isEnabled() is True
    assert widget.optionFixed() is False


def test_setOnOptionChanged(qtbot):
    widget = EntryWidget(options=test_options_colors)
    show(locals())
    widget.optionChanged.connect(lambda: change_color_on_option(widget))

    widget.setSelected(test_options_colors[1])
    assert getCurrentColor(widget.lineEdit, 'Window')[0][0] == test_options_colors[1]

    widget.setSelected(test_options_colors[0])
    assert getCurrentColor(widget.lineEdit, 'Window')[0][0] == test_options_colors[0]

    widget.setSelected(test_options_colors[2])
    assert getCurrentColor(widget.lineEdit, 'Window')[0][0] == test_options_colors[2]

