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

def test_setAutoColors(qtbot):
    widget = EntryWidget()
    show(locals())
    widget.setAutoColors(test_color_dict_good)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['blank'][0]
    assert getCurrentColor(widget, 'WindowText')[0][0] ==  test_color_dict_good['blank'][1]
    qtbot.keyClick(widget._editBox, 'a')
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['default'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['default'][1]
    widget.setError(True)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['error'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['error'][1]
    widget.setReadOnly(True)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['error-readonly'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['error-readonly'][1]
    widget.setEnabled(False)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['error-readonly'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['error-readonly'][1]
    widget.setError(False)
    assert getCurrentColor(widget._editBox, 'Window')[1] ==  test_color_dict_good['disabled'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['disabled'][1]
    widget.setEnabled(True)
    widget.setError(True)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['error-readonly'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['error-readonly'][1]
    widget.setError(False)
    widget.setReadOnly(False)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['default'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['default'][1]
    qtbot.keyPress(widget._editBox, QtCore.Qt.Key_Backspace)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['blank'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['blank'][1]
    widget.setReadOnly(True)
    assert getCurrentColor(widget._editBox, 'Window')[1] ==  test_color_dict_good['readonly'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['readonly'][1]

    widget = EntryWidget()
    show(locals())
    widget.setColors(test_color_tuple)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_tuple[0]
    assert widget._manualColors is True
    widget.setAutoColors()
    assert widget._manualColors is False
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict['blank'][0]
    assert getCurrentColor(widget, 'WindowText')[0][0] ==  test_color_dict['blank'][1]
    qtbot.keyClick(widget._editBox, 'a')
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict['default'][0]
    assert getCurrentColor(widget, 'WindowText')[0][0] ==  test_color_dict['default'][1]
    widget.setError(True)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict['error'][0]
    assert getCurrentColor(widget, 'WindowText')[0][0] ==  test_color_dict['error'][1]
    widget.setReadOnly(True)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict['error-readonly'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict['error-readonly'][1]
    widget.setEnabled(False)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict['error-readonly'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict['error-readonly'][1]
    widget.setError(False)
    assert getCurrentColor(widget._editBox, 'Window')[1] ==  test_color_dict['disabled'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict['disabled'][1]
    widget.setEnabled(True)
    widget.setError(True)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict['error-readonly'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict['error-readonly'][1]
    widget.setError(False)
    widget.setReadOnly(False)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict['default'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict['default'][1]
    qtbot.keyPress(widget._editBox, QtCore.Qt.Key_Backspace)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict['blank'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict['blank'][1]
    widget.setReadOnly(True)
    assert getCurrentColor(widget._editBox, 'Window')[1] ==  test_color_dict['readonly'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict['readonly'][1]

    widget = EntryWidget(colors=test_color_dict_good)
    show(locals())
    widget.setColors(test_color_tuple_good)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_tuple_good[0]
    assert widget._manualColors is True
    widget.setAutoColors()
    assert widget._manualColors is False
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['blank'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['blank'][1]
    qtbot.keyClick(widget._editBox, 'a')
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['default'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['default'][1]
    widget.setError(True)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['error'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['error'][1]
    widget.setReadOnly(True)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['error-readonly'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['error-readonly'][1]
    widget.setEnabled(False)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['error-readonly'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['error-readonly'][1]
    widget.setError(False)
    assert getCurrentColor(widget._editBox, 'Window')[1] ==  test_color_dict_good['disabled'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['disabled'][1]
    widget.setEnabled(True)
    widget.setError(True)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['error-readonly'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['error-readonly'][1]
    widget.setError(False)
    widget.setReadOnly(False)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['default'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['default'][1]
    qtbot.keyPress(widget._editBox, QtCore.Qt.Key_Backspace)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['blank'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['blank'][1]
    widget.setReadOnly(True)
    assert getCurrentColor(widget._editBox, 'Window')[1] ==  test_color_dict_good['readonly'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['readonly'][1]

    with pytest.raises(AssertionError):
        widget.setAutoColors(test_color_tuple)
    with pytest.raises(AssertionError):
        widget.setAutoColors(test_color_dict_bad)

def test_setText(qtbot):
    widget = EntryWidget()
    widget.setText(test_strings[1])
    show(locals())
    assert widget.text() == test_strings[1]
    assert widget._editBox.text() == test_strings[1]

    with pytest.raises(AssertionError):
        widget.setText(test_strings[-1])

def test_setReadOnly(qtbot):
    widget = EntryWidget()
    show(locals())
    widget.setReadOnly(True)
    assert widget._editBox.isReadOnly() is True
    assert widget.isReadOnly() is True
    widget.setReadOnly(False)
    assert widget._editBox.isReadOnly() is False
    assert widget.isReadOnly() is False

    with pytest.raises(AssertionError):
        widget.setReadOnly(1)

def test_setColors(qtbot):
    widget = EntryWidget()
    show(locals())
    assert widget._manualColors is False
    widget.setColors(test_color_tuple)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_tuple[0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_tuple[1]
    assert widget._manualColors is True

    widget = EntryWidget()
    show(locals())
    widget.setColors(test_color_tuple_good)
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_tuple_good[0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_tuple_good[1]

    with pytest.raises(AssertionError):
        widget.setColors(test_color_tuple_bad)

def test_setOnTextChanged(qtbot):
    widget = EntryWidget()
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

    with pytest.raises(AssertionError):
        widget = EntryWidget()
        widget.setOnTextChanged(test_strings)

def test_setOnEditingFinished(qtbot):
    widget = EntryWidget(label=test_strings[0])
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

    with pytest.raises(AssertionError):
        widget = EntryWidget()
        widget.setOnEditingFinished(test_strings)

def test_setError(qtbot):
    widget = EntryWidget()
    show(locals())
    widget.setError(True)
    assert widget.getError() == widget.isError() is True
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['error'][0]
    widget.setError(False)
    assert widget.getError() == widget.isError() is False
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['blank'][0]

    widget.setError(True)
    assert widget.getError() == widget.isError() is True
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['error'][0]
    widget.setError(False)
    assert widget.getError() == widget.isError() is False
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['blank'][0]

def test_setIsError(qtbot):
    widget = EntryWidget()
    widget.setIsError(check_error_typed)
    show(locals())

    qtbot.keyClicks(widget._editBox, 'error')
    assert widget.getError()
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['error'][0]
    qtbot.keyPress(widget._editBox, QtCore.Qt.Key_Backspace)
    assert widget.getError() is False
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['default'][0]

    widget = EntryWidget(liveErrorChecking=False)
    widget.setIsError(check_error_typed)
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

    with pytest.raises(AssertionError):
        widget = EntryWidget()
        widget.setIsError(test_strings)

def test_setOnError(qtbot):
    widget = EntryWidget()
    widget.setOnError(set_title_on_error)
    show(locals())

    assert widget.getError() is False
    widget.setError(False)
    assert widget.getError() is False
    widget.setError(True)
    assert widget.windowTitle() == 'ERROR'
    assert widget.getError()

    with pytest.raises(AssertionError):
        widget = EntryWidget()
        widget.setOnError(test_strings)

def test_setLabel(qtbot):
    widget = EntryWidget()
    show(locals())
    widget.setLabel(test_strings[1])
    assert widget.getLabel() == test_strings[1]
    assert widget._label.text() == test_strings[1]

    with pytest.raises(AssertionError):
        widget.setLabel(test_strings[-1])

def test_setOptions(qtbot):
    widget = EntryWidget()
    show(locals())
    widget.setOptions(test_options_good)
    assert widget.getOptions() == test_options_good

    with pytest.raises(AssertionError):
        widget.setOptions(test_options_bad)

    with pytest.raises(AssertionError):
        widget.setOptions(test_strings[0])

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

    with pytest.raises(AssertionError):
        widget.setOptionFixed(1)

def test_setOnLabelClick(qtbot):
    widget = EntryWidget()
    show(locals())
    widget.setOnLabelClick(lock_unlock_entry_mouse)

    qtbot.mouseClick(widget._label, QtCore.Qt.LeftButton)
    assert widget._editBox.isReadOnly() is True
    assert widget.isReadOnly() is True
    qtbot.mouseClick(widget._label, QtCore.Qt.RightButton)
    assert widget._editBox.isReadOnly() is False
    assert widget.isReadOnly() is False

    widget = EntryWidget()
    widget.setOnLabelClick(lock_unlock_option_mouse)
    show(locals())

    qtbot.mouseClick(widget._label, QtCore.Qt.LeftButton)
    assert widget._optionList.isEnabled() is False
    assert widget._optionFixed is True
    qtbot.mouseClick(widget._label, QtCore.Qt.RightButton)
    assert widget._optionList.isEnabled() is True
    assert widget._optionFixed is False

    with pytest.raises(AssertionError):
        widget = EntryWidget()
        widget.setOnLabelClick(test_strings)

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

    with pytest.raises(AssertionError):
        widget = EntryWidget()
        widget.setOnOptionChanged(test_strings)

def test_liveErrorChecking(qtbot):
    widget = EntryWidget()
    widget.setLiveErrorChecking(False)
    widget.setIsError(check_error_typed)
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

    widget = EntryWidget()
    widget.setLiveErrorChecking(True)
    widget.setIsError(check_error_typed)
    show(locals())
    qtbot.keyClicks(widget._editBox, 'error')
    assert widget.getError()
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['error'][0]
    qtbot.keyPress(widget._editBox, QtCore.Qt.Key_Backspace)
    assert widget.getError() is False
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['default'][0]

    with pytest.raises(AssertionError):
        widget.setLiveErrorChecking(1)
