import pytest
from generalUtils.helpers_for_tests import *
from entryWidget import EntryWidget
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

def test_basic_open(qtbot):
    widget = EntryWidget()
    show(locals())

def test_constructor_start_prompt(qtbot):
    widget = EntryWidget(startPrompt=test_strings[1])
    show(locals())
    assert widget.text() == test_strings[1]
    assert widget._editBox.text() == test_strings[1]


def test_constructor_readOnly(qtbot):
    widget = EntryWidget(readOnly=True)
    show(locals())
    assert widget._editBox.isReadOnly() is True
    assert widget.isReadOnly() is True

    widget = EntryWidget(readOnly=False)
    show(locals())
    assert widget._editBox.isReadOnly() is False
    assert widget.isReadOnly() is False


def test_constructor_colors(qtbot):
    widget = EntryWidget(colors=test_color_dict)
    show(locals())

    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict['blank'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict['blank'][1]

    widget = EntryWidget(colors=test_color_dict_good)
    show(locals())

    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['blank'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['blank'][1]

    with pytest.raises(AssertionError):
        widget = EntryWidget(colors=test_color_dict_bad)

    with pytest.raises(AssertionError):
        widget = EntryWidget(colors=test_color_tuple)

def test_constructor_onTextChanged(qtbot):
    widget = EntryWidget(onTextChanged=change_label_on_typing)
    show(locals())

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


def test_constructor_onEditingFinished(qtbot):
    widget = EntryWidget(onEditingFinished=change_label_on_typing)
    widget.setLabel(test_strings[0])
    show(locals())

    qtbot.keyClick(widget._editBox, 'a')
    assert widget._editBox.text() == 'a'
    assert widget.text() == 'a'
    assert widget.getLabel() == test_strings[0]
    assert widget._label.text() == test_strings[0]

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


def test_constructor_isError(qtbot):
    widget = EntryWidget(isError=check_error_typed)
    show(locals())

    qtbot.keyClicks(widget._editBox, 'error')
    assert widget.getError()
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['error'][0]
    qtbot.keyPress(widget._editBox, QtCore.Qt.Key_Backspace)
    assert widget.getError() is False
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['default'][0]

    widget = EntryWidget(isError=check_error_typed, liveErrorChecking=False)
    show(locals())
    qtbot.keyClicks(widget._editBox, 'error')
    assert widget.getError() is False
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['default'][0]
    qtbot.keyPress(widget._editBox, QtCore.Qt.Key_Return)
    assert widget.getError()
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['error'][0]
    qtbot.keyPress(widget._editBox, QtCore.Qt.Key_Backspace)
    assert widget.getError()
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['error'][0]
    qtbot.keyPress(widget._editBox, QtCore.Qt.Key_Return)
    assert widget.getError() is False
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['default'][0]


def test_constructor_onError(qtbot):
    widget = EntryWidget(onError=set_title_on_error)
    show(locals())

    assert widget.getError() is False
    widget.setError(False)
    assert widget.getError() is False
    widget.setError(True)
    assert widget.windowTitle() == 'ERROR'


def test_constructor_label(qtbot):
    widget = EntryWidget(label=test_strings[1])
    show(locals())
    assert widget.getLabel() == test_strings[1]
    assert widget._label.text() == test_strings[1]


def test_constructor_options(qtbot):
    widget = EntryWidget(options=test_options_good)
    show(locals())
    assert widget.getOptions() == test_options_good


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
    widget = EntryWidget(onLabelClick=lock_unlock_entry_mouse)
    show(locals())

    qtbot.mouseClick(widget._label, QtCore.Qt.LeftButton)
    assert widget._editBox.isReadOnly() is True
    assert widget.isReadOnly() is True
    qtbot.mouseClick(widget._label, QtCore.Qt.RightButton)
    assert widget._editBox.isReadOnly() is False
    assert widget.isReadOnly() is False

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
