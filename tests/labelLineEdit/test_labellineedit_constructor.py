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

def test_constructor_start_prompt(qtbot):
    widget = LabelLineEdit(startPrompt=test_strings[1])
    show(locals())
    assert widget.text() == test_strings[1]
    assert widget._editBox.text() == test_strings[1]


def test_constructor_readOnly(qtbot):
    widget = LabelLineEdit(readOnly=True)
    show(locals())
    assert widget._editBox.isReadOnly() is True
    assert widget.isReadOnly() is True

    widget = LabelLineEdit(readOnly=False)
    show(locals())
    assert widget._editBox.isReadOnly() is False
    assert widget.isReadOnly() is False


def test_constructor_colors(qtbot):
    widget = LabelLineEdit(colors=test_color_dict)
    show(locals())

    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict['blank'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict['blank'][1]

    widget = LabelLineEdit(colors=test_color_dict_good)
    show(locals())

    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['blank'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['blank'][1]

    with pytest.raises(AssertionError):
        widget = LabelLineEdit(colors=test_color_dict_bad)

    with pytest.raises(AssertionError):
        widget = LabelLineEdit(colors=test_color_tuple)

def test_constructor_onTextChanged(qtbot):
    widget = LabelLineEdit(onTextChanged=change_label_on_typing)
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
    widget = LabelLineEdit(label=test_strings[0], onEditingFinished=change_label_on_typing)
    show(locals())
    assert widget.getLabel() == test_strings[0]

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
    widget = LabelLineEdit(isError=check_error_typed)
    show(locals())

    qtbot.keyClicks(widget._editBox, 'error')
    assert widget.getError()
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['error'][0]
    qtbot.keyPress(widget._editBox, QtCore.Qt.Key_Backspace)
    assert widget.getError() is False
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['default'][0]

    widget = LabelLineEdit(isError=check_error_typed, liveErrorChecking=False)
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
    widget = LabelLineEdit(onError=set_title_on_error)
    show(locals())

    assert widget.getError() is False
    widget.setError(False)
    assert widget.getError() is False
    widget.setError(True)
    assert widget.windowTitle() == 'ERROR'


def test_constructor_label(qtbot):
    widget = LabelLineEdit(label=test_strings[1])
    show(locals())
    assert widget.getLabel() == test_strings[1]

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
