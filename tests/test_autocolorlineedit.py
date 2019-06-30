import pytest
import sys

# test helpers
from qt_utils.helpers_for_tests import (set_title_on_error, change_title_on_typing,
                                        change_color_on_option, change_label_on_typing,
                                        check_error_typed, do_whats_typed, show)

# dicts/tuples/lists for color testing (from __init__.py)
from . import *
# helpers
from qt_utils.colors import findColor, colorList
from qt_utils import getCurrentColor

# class to test
from entryWidget import AutoColorLineEdit

# Qt stuff
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

# logging stuff
import logging

# logging.basicConfig(stream=sys.stdout, filename='/logs/AutoColorLineEdit.log', level=logging.INFO)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
testlogger = logging.getLogger('testLogger')
app = QApplication(sys.argv)


def test_constructor_basic(qtbot):
    widget = AutoColorLineEdit()
    show(locals())


def test_constructor_text(qtbot):
    widget = AutoColorLineEdit(text=test_strings[1])
    show(locals())
    assert widget.text() == test_strings[1]


def test_constructor_readOnly(qtbot):
    widget = AutoColorLineEdit(readOnly=True)
    show(locals())
    assert widget.isReadOnly() is True

    widget = AutoColorLineEdit(readOnly=False)
    show(locals())
    assert widget.isReadOnly() is False


def test_constructor_colors(qtbot):
    widget = AutoColorLineEdit(autoColors=test_color_dict)
    show(locals())

    assert getCurrentColor(widget, 'Window').names[0] ==  test_color_dict['blank'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] ==  test_color_dict['blank'][1]
    assert widget._manualColors is False

    widget = AutoColorLineEdit(autoColors=test_color_dict_good)
    show(locals())
    assert getCurrentColor(widget, 'Window').names[0] ==  test_color_dict_good['blank'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] ==  test_color_dict_good['blank'][1]
    assert widget._manualColors is False

    with pytest.raises(AssertionError):
        widget = AutoColorLineEdit(autoColors=test_color_dict_bad)

    with pytest.raises(AssertionError):
        widget = AutoColorLineEdit(autoColors=test_color_tuple)


def test_setText(qtbot):
    widget = AutoColorLineEdit()
    widget.setText(test_strings[1])
    show(locals())
    assert widget.text() == test_strings[1]


def test_setReadOnly(qtbot):
    widget = AutoColorLineEdit(objectName='readonly1')
    show(locals())
    widget.setReadOnly(True)
    assert widget.isReadOnly() is True

    widget = AutoColorLineEdit(objectName='readonly2')
    show(locals())
    widget.setReadOnly(False)
    assert widget.isReadOnly() is False


def test_setError(qtbot):
    widget = AutoColorLineEdit()
    show(locals())
    widget.setError(True)
    assert widget.getError() is True
    assert getCurrentColor(widget, 'Window').names[0] == widget.defaultColors['error'][0]
    widget.setError(False)
    assert widget.getError() is False
    assert getCurrentColor(widget, 'Window').names[0] == widget.defaultColors['blank'][0]


def test_textChanged(qtbot):
    widget = AutoColorLineEdit()
    widget.textChanged.connect(lambda t: change_title_on_typing(widget))
    show(locals())
    assert getCurrentColor(widget, 'Window').names[0] == widget._autoColors['blank'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == widget._autoColors['blank'][1]

    qtbot.keyClick(widget, 'a')
    assert widget.text() == 'a'
    assert widget.windowTitle() == 'a'
    assert getCurrentColor(widget, 'Window').names[0] == widget._autoColors['default'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == widget._autoColors['default'][1]

    qtbot.keyClick(widget, 'b')
    assert widget.text() == 'ab'
    assert widget.windowTitle() == 'ab'


def test_editingFinished(qtbot):
    widget = AutoColorLineEdit()
    widget.editingFinished.connect(lambda: change_title_on_typing(widget))
    show(locals())
    assert getCurrentColor(widget, 'Window').names[0] == widget._autoColors['blank'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == widget._autoColors['blank'][1]

    qtbot.keyClick(widget, 'a')
    assert widget.text() == 'a'
    assert widget.windowTitle() == ''
    assert getCurrentColor(widget, 'Window').names[0] == widget._autoColors['default'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == widget._autoColors['default'][1]

    qtbot.keyClick(widget, 'b')
    assert widget.text() == 'ab'
    assert widget.windowTitle() == ''

    qtbot.keyPress(widget, QtCore.Qt.Key_Return)
    assert widget.text() == 'ab'
    assert widget.windowTitle() == 'ab'


def test_errorCheck_live(qtbot):
    widget = AutoColorLineEdit()
    widget.errorCheck = lambda: check_error_typed(widget)
    show(locals())
    testlogger.debug('typing...')
    qtbot.keyClicks(widget, 'erro')
    assert widget.getError() is False
    qtbot.keyClicks(widget, 'r')
    testlogger.debug('finished typing...')
    assert widget.getError() == 'ERROR'
    assert getCurrentColor(widget, 'Window').names[0] == widget.defaultColors['error'][0]
    qtbot.keyPress(widget, QtCore.Qt.Key_Backspace)
    assert widget.getError() is False
    assert getCurrentColor(widget, 'Window').names[0] == widget.defaultColors['default'][0]


def test_errorCheck(qtbot):
    widget = AutoColorLineEdit(liveErrorChecking=False)
    widget.errorCheck = lambda: check_error_typed(widget)
    show(locals())
    testlogger.debug('typing...')
    qtbot.keyClicks(widget, 'erro')
    assert widget.getError() is False
    qtbot.keyClicks(widget, 'r')
    testlogger.debug('finished typing...')
    assert widget.getError() is False
    qtbot.keyPress(widget, QtCore.Qt.Key_Return)
    assert widget.getError() == 'ERROR'
    assert getCurrentColor(widget, 'Window').names[0] == widget.defaultColors['error'][0]
    qtbot.keyPress(widget, QtCore.Qt.Key_Backspace)
    assert widget.getError() == 'ERROR'
    qtbot.keyPress(widget, QtCore.Qt.Key_Return)
    assert widget.getError() is False
    assert getCurrentColor(widget, 'Window').names[0] == widget.defaultColors['default'][0]


def test_hasError(qtbot):
    widget = AutoColorLineEdit()
    widget.hasError.connect(lambda e: set_title_on_error(widget))
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
    assert getCurrentColor(widget, 'Window')[2] == (240, 248, 255)

    fails = []

    for C in colorList:
        if C == colorList[-1]:
            continue
        testlogger.debug(f"C: {C}")
        clist = C.names + [C.hex, C.rgb]
        testlogger.debug(f"clist: {clist}")
        for c in clist:
            testlogger.debug('c: ' + str(c))
            testlogger.debug(f"found: {findColor(c)}")
            widget.setColors((c, c))
            testlogger.debug(f"currentColor: {getCurrentColor(widget, 'Window')}")
            if not getCurrentColor(widget, 'Window').names[0] in clist:
                testlogger.debug('*****************Color Failed')
                assert False


def test_embed_widgets(qtbot):
    from PyQt5.QtWidgets import QVBoxLayout, QWidget
    window = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(AutoColorLineEdit())
    layout.addWidget(AutoColorLineEdit())
    window.setLayout(layout)
    show({'qtbot':qtbot, 'widget':window})


def test_styleSheet(qtbot):
    widget = AutoColorLineEdit()
    show(locals())

    string = widget.makeStyleString(('black', 'white'))
    widget.setStyleSheet(string)
    assert string == widget.styleSheet()

    widget = AutoColorLineEdit(text='text')
    show(locals())
    string = widget.makeStyleString(('blue','red'))

    assert getCurrentColor(widget, 'WindowText').names[0] == 'black'
    assert getCurrentColor(widget, 'Background').names[0] == 'white'

    widget.setStyleSheet(string)
    assert getCurrentColor(widget, 'WindowText').names[0] == 'red'
    assert getCurrentColor(widget, 'Background').names[0] == 'blue'

    assert string == widget.styleSheet()

    widget.setText('a')
    assert getCurrentColor(widget, 'Background').names[0] == 'blue'


def test_setAutoColors(qtbot):
    widget = AutoColorLineEdit()
    show(locals())
    widget.setAutoColors(test_color_dict_good)

# check colors when blank, enabled
    assert getCurrentColor(widget, 'Window').names[0] ==  test_color_dict_good['blank'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] ==  test_color_dict_good['blank'][1]
# with error
    widget.setError(True)
    assert getCurrentColor(widget, 'Window').names[0] == test_color_dict_good['error'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['error'][1]
# error & readonly
    widget.setReadOnly(True)
    assert getCurrentColor(widget, 'Window').names[0] == test_color_dict_good['error-readonly'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['error-readonly'][1]
# readonly
    widget.setError(False)
    assert getCurrentColor(widget, 'Window')[1] == test_color_dict_good['readonly'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['readonly'][1]
# regular
    widget.setReadOnly(False)
    assert getCurrentColor(widget, 'Window').names[0] == test_color_dict_good['blank'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['blank'][1]


# check colors when blank, disabled
    widget.setEnabled(False)
    assert getCurrentColor(widget, 'Window')[1] ==  test_color_dict_good['disabled'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] ==  test_color_dict_good['disabled'][1]
# with error
    widget.setError(True)
    assert getCurrentColor(widget, 'Window').names[0] == test_color_dict_good['error-readonly'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['error-readonly'][1]
# error & readonly
    widget.setReadOnly(True)
    assert getCurrentColor(widget, 'Window').names[0] == test_color_dict_good['error-readonly'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['error-readonly'][1]
# readonly
    widget.setError(False)
    assert getCurrentColor(widget, 'Window')[1] == test_color_dict_good['disabled'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['disabled'][1]
# regular
    widget.setReadOnly(False)
    assert getCurrentColor(widget, 'Window')[1] == test_color_dict_good['disabled'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['disabled'][1]


    widget.setReadOnly(False)
    widget.setEnabled(True)
    qtbot.keyClick(widget, 'a')
# check colors when not blank, enabled
    assert getCurrentColor(widget, 'Window').names[0] == test_color_dict_good['default'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['default'][1]
# with error
    widget.setError(True)
    assert getCurrentColor(widget, 'Window').names[0] == test_color_dict_good['error'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['error'][1]
# error & readonly
    widget.setReadOnly(True)
    assert getCurrentColor(widget, 'Window').names[0] == test_color_dict_good['error-readonly'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['error-readonly'][1]
# readonly
    widget.setError(False)
    assert getCurrentColor(widget, 'Window')[1] == test_color_dict_good['readonly'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['readonly'][1]
# regular
    widget.setReadOnly(False)
    assert getCurrentColor(widget, 'Window').names[0] == test_color_dict_good['default'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['default'][1]


# check colors when not blank, disabled
    widget.setEnabled(False)
    assert getCurrentColor(widget, 'Window')[1] == test_color_dict_good['disabled'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['disabled'][1]
# with error
    widget.setError(True)
    assert getCurrentColor(widget, 'Window').names[0] == test_color_dict_good['error-readonly'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['error-readonly'][1]
# error & readonly
    widget.setReadOnly(True)
    assert getCurrentColor(widget, 'Window').names[0] == test_color_dict_good['error-readonly'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['error-readonly'][1]
# readonly
    widget.setError(False)
    assert getCurrentColor(widget, 'Window')[1] == test_color_dict_good['disabled'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['disabled'][1]
# regular
    widget.setReadOnly(False)
    assert getCurrentColor(widget, 'Window')[1] == test_color_dict_good['disabled'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict_good['disabled'][1]


# check auto colors after manual colors
    widget = AutoColorLineEdit()
    show(locals())
    widget.setColors(test_color_tuple)
    assert getCurrentColor(widget, 'Window').names[0] == test_color_tuple[0]
    assert widget._manualColors is True
    widget.setAutoColors()
    assert widget._manualColors is False
    assert getCurrentColor(widget, 'Window').names[0] == test_color_dict['blank'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict['blank'][1]
    qtbot.keyClick(widget, 'a')
    assert getCurrentColor(widget, 'Window').names[0] == test_color_dict['default'][0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_dict['default'][1]

    with pytest.raises(AssertionError):
        widget.setAutoColors(test_color_tuple)
    with pytest.raises(AssertionError):
        widget.setAutoColors(test_color_dict_bad)


def test_setColors(qtbot):
    widget = AutoColorLineEdit()
    show(locals())
    assert widget._manualColors is False

    widget.setColors(test_color_tuple)
    assert getCurrentColor(widget, 'Window').names[0] == test_color_tuple[0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_tuple[1]
    assert widget._manualColors is True

    widget.setColors(test_color_tuple_good)
    assert getCurrentColor(widget, 'Window').names[0] == test_color_tuple_good[0]
    assert getCurrentColor(widget, 'WindowText').names[0] == test_color_tuple_good[1]
    assert widget._manualColors is True

    with pytest.raises(AssertionError):
        widget.setColors(test_color_tuple_bad)

