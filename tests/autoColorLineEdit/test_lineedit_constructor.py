import pytest
from generalUtils.helpers_for_tests import *
from entryWidget.utils import findColor, getCurrentColor
from entryWidget import AutoColorLineEdit
import sys

# Qt stuff
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

# logging stuff
import logging

# logging.basicConfig(stream=sys.stdout, filename='/logs/AutoColorLineEdit.log', level=logging.INFO)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = QApplication(sys.argv)

def test_basic_open(qtbot):
    widget = AutoColorLineEdit()
    show(locals())

def test_constructor_start_prompt(qtbot):
    widget = AutoColorLineEdit(startPrompt=test_strings[1])
    show(locals())
    assert widget.text() == test_strings[1]
    assert widget._editBox.text() == test_strings[1]
    assert widget.text == widget._editBox.text


def test_constructor_readOnly(qtbot):
    widget = AutoColorLineEdit(readOnly=True)
    show(locals())
    assert widget.isReadOnly() is True
    assert widget._editBox.isReadOnly() is True

    widget = AutoColorLineEdit(readOnly=False)
    show(locals())
    assert widget.isReadOnly() is False
    assert widget._editBox.isReadOnly() is False


def test_constructor_colors(qtbot):
    widget = AutoColorLineEdit(colors=test_color_dict)
    show(locals())

    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict['blank'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict['blank'][1]
    assert widget._manualColors is False

    widget = AutoColorLineEdit(colors=test_color_dict_good)
    show(locals())
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  test_color_dict_good['blank'][0]
    assert getCurrentColor(widget._editBox, 'WindowText')[0][0] ==  test_color_dict_good['blank'][1]
    assert widget._manualColors is False

    with pytest.raises(AssertionError):
        widget = AutoColorLineEdit(colors=test_color_dict_bad)

    with pytest.raises(AssertionError):
        widget = AutoColorLineEdit(colors=test_color_tuple)

def test_constructor_onTextChanged(qtbot):
    widget = AutoColorLineEdit(onTextChanged=lambda w:change_title_on_typing(w))
    show(locals())

    qtbot.keyClick(widget._editBox, 'a')
    assert widget.text() == 'a'
    assert widget.windowTitle() == 'a'

    qtbot.keyClick(widget._editBox, 'b')
    assert widget.text() == 'ab'
    assert widget.windowTitle() == 'ab'


def test_constructor_onEditingFinished(qtbot):
    widget = AutoColorLineEdit(onEditingFinished=change_title_on_typing)
    show(locals())

    qtbot.keyClick(widget._editBox, 'a')
    assert widget.text() == 'a'
    assert widget.windowTitle() == ''
    qtbot.keyClick(widget._editBox, 'b')
    assert widget.text() == 'ab'
    assert widget.windowTitle() == ''

    qtbot.keyPress(widget._editBox, QtCore.Qt.Key_Return)
    assert widget.text() == 'ab'
    assert widget.windowTitle() == 'ab'


def test_constructor_isError(qtbot):
    widget = AutoColorLineEdit(isError=check_error_typed)
    show(locals())
    qtbot.keyClicks(widget._editBox, 'error')
    assert widget.getError()
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['error'][0]
    qtbot.keyPress(widget._editBox, QtCore.Qt.Key_Backspace)
    assert widget.getError() is False
    assert getCurrentColor(widget._editBox, 'Window')[0][0] ==  widget.defaultColors['default'][0]

    widget = AutoColorLineEdit(isError=check_error_typed, liveErrorChecking=False)
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
    widget = AutoColorLineEdit(onError=set_title_on_error)
    show(locals())

    assert widget.getError() is False
    widget.setError(False)
    assert widget.getError() is False
    widget.setError(True)
    assert widget.windowTitle() == 'ERROR'

def test_all_colors(qtbot):
    widget = AutoColorLineEdit()
    show(locals())

    widget.setColors(((240, 248, 255), 'black'))
    assert getCurrentColor(widget._editBox, 'Window')[2] == (240, 248, 255)

    fails = []

    for C in colorList:
        if C == colorList[-1]:
            continue
        logging.debug(C)
        clist = C[0] + list((C[1], C[2]))
        logging.debug(clist)
        for c in clist:
            logging.debug('c: ' + str(c))
            logging.debug(findColor(c))
            widget.setColors((c, c))
            logging.debug(getCurrentColor(widget._editBox, 'Window'))
            if not getCurrentColor(widget._editBox, 'Window')[0][0] in clist:
                fails.append([C, c, getCurrentColor(widget, 'Window')])
    logging.debug('*****************')
    for f in fails:
        logging.debug(f)
    assert not fails

def test_embed_widgets(qtbot):
    from PyQt5.QtWidgets import QVBoxLayout, QWidget
    window = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(AutoColorLineEdit())
    layout.addWidget(AutoColorLineEdit())
    window.setLayout(layout)
    show({'qtbot':qtbot, 'widget':window})

def test_style_string(qtbot):
    widget = AutoColorLineEdit()
    show(locals())

    string = widget._editBox.makeStyleString(('black', 'white'))
    widget._editBox.setStyleSheet(string)
    assert string == widget._editBox.getStyleString()

    widget = AutoColorLineEdit()
    show(locals())
    string = widget._editBox.makeStyleString({
            'default':('black','white'),
            'blank':('red','white'),
         })

    assert getCurrentColor(widget._editBox, 'Background')[0][0] == AutoColorLineEdit.defaultColors['blank'][0]

    widget._editBox.setStyleSheet(string)
    assert getCurrentColor(widget._editBox, 'Background')[0][0] == 'red'

    assert string == widget._editBox.getStyleString()

    widget.setText('a')
    assert getCurrentColor(widget._editBox, 'Background')[0][0] == 'black'
