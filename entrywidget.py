from PyQt5.QtWidgets import QLineEdit, QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtProperty, pyqtSignal
from PyQt5 import Qt, QtCore
from PyQt5.QtGui import QColor
from copy import copy
from qt_utils import loggableQtName, ErrorMixin
from qt_utils.widgets import DictComboBox
from generalUtils.delegated import delegated
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def _isColorTuple(colors):
    """Assert 'colors' matches the format for a colors tuple.

    :param colors: tuple to check format of
    :return: bool
        False if colors == None
        True if colors == correct format
        Raises AssertionError if incorrect format
    """
    if colors is None:
        return False

    assert isinstance(colors, tuple), \
        'provide a tuple of color strings, check help(setColor) for more info'
    assert len(colors) == 2, \
        'provide a tuple of color strings, check help(setColor) for more info'
    assert all(isinstance(c, (str, tuple, QColor)) for c in colors), \
        'provide a tuple of color strings or QtGui.QColor\'s, check help(setColor) for more info'
    return True


def _isColorDict(colors):
    """Assert 'colors' matches the format for a colors dict.

    :param colors: dict to check format of
    :return: bool
        False if colors=None
        True if colors= correct format
        Raises AssertionError if incorrect format
    """
    if colors is None:
        return False

    # check format
    assert isinstance(colors, dict), \
        'provide a color dict; check help(setAutoColors) for more info'
    try:
        all(_isColorTuple(c) for c in colors.values())
    except AssertionError:
        raise AssertionError('provide a color dict; check help(setAutoColors) for more info')
    return True


class AutoColorLineEdit(QWidget, ErrorMixin):
    """A QLineEdit (in a QHBoxLayout) with error checking options with automatic color updates.
    QLineEdit (.lineEdit):
        Change with obj.setText('new text')
        Read with obj.text()

    signals:
        hasError([]],[object],[str])  # emitted when bool(error status) is True
        errorChanged([],[object],[str])  # emitted when error status changes
        errorCleared  # emitted when bool(error status) is changed to False
        editingFinished([],[str])  # emitted when Enter/Return pressed or focus is changed out of QLineEdit
        textChanged([],[str])  # emitted when text changes at all
        textEdited([],[str])  # emitted when text is changed by user

    All arguments are optional and must be provided by keyword, except 'parent' which can be positional.
    :param parent: Parent Qt Object (default None for individual widget)
    :param errorCheck: callable, returns error status, called with widget as first argument
    :param objectName: str, name of object for logging and within Qt
    :param text: str, starting text
    :param autoColors: dict of tuples of color strings; see help(setAutoColor) for formatting
    :param readOnly: bool, whether the text box is editable
    :param liveErrorChecking: bool, whether error checking occurs
                after every keystroke (=True) or only after text editing is finished (=False)

    written by Tim Olson - timjolson@user.noreplay.github.com
    """
    name = loggableQtName
    editingFinished = pyqtSignal([],[str])
    textChanged = pyqtSignal([],[str])
    textEdited = pyqtSignal([],[str])

    defaultColors = {
        'error-readonly': ('orangered', 'white'),
        'error': ('yellow', 'black'),
        'default': ('white', 'black'),
        'blank': ('lightblue', 'black'),
        'disabled': ('#F0F0F0', 'black'),
        'readonly': ('#F0F0F0', 'black')
    }

    defaultArgs = {
        'autoColors': defaultColors,
        'liveErrorChecking': True,
        'text': '',
        'errorCheck':None,
        'readOnly':False
    }

    # explicitly delegate to QLineEdit
    text, palette = delegated.methods('lineEdit', 'text, palette')
    clear, setClearButtonEnabled, isReadOnly = delegated.methods('lineEdit', 'clear setClearButtonEnabled isReadOnly')
    # mousePressEvent, mouseReleaseEvent = delegated.methods('lineEdit', 'mousePressEvent, mouseReleaseEvent')
    keyPressEvent, keyReleaseEvent = delegated.methods('lineEdit', 'keyPressEvent, keyReleaseEvent')
    # focusInEvent, focusOutEvent = delegated.methods('lineEdit', 'focusInEvent, focusOutEvent')

    # property for designer plugin usage
    edit_text = pyqtProperty(str, lambda s: s.text(), lambda s, p: s.setText(p))

    def __init__(self, parent=None, **kwargs):
        autoColors = kwargs.pop('autoColors', self.defaultArgs['autoColors'])
        self._liveErrorChecking = kwargs.pop('liveErrorChecking', self.defaultArgs['liveErrorChecking'])
        kwargs.setdefault('text', self.defaultArgs['text'])
        kwargs.setdefault('readOnly', self.defaultArgs['readOnly'])

        ec = kwargs.pop('errorCheck', None)

        on = kwargs.pop('objectName', None)
        if on:
            QWidget.__init__(self, parent, objectName=on)
        else:
            QWidget.__init__(self, parent)
        ErrorMixin.__init__(self)
        self._error = False
        self._manualColors = False  # whether colors are manually set or automatic
        self._modified = False

        self.logger = logging.getLogger(self.name)
        self.logger.addHandler(logging.NullHandler())

        # verify format of 'autoColors', combine with defaults
        if _isColorDict(autoColors):
            defcolors = self.defaultColors.copy()
            defcolors.update(autoColors)
            autoColors = defcolors
        elif autoColors is None:
            autoColors = self.defaultColors.copy()
        else:
            raise TypeError(f"Unrecognized format {autoColors}")
        self._autoColors = autoColors

        self.setupUi(kwargs)

        if ec is not None:
            self.errorCheck = lambda: ec(self)
        self.errorChanged.connect(self.refreshColors)
        self._error = self.errorCheck()

        self.refreshColors()

    def setupUi(self, kwargs):
        self.textChanged[str].connect(lambda o: self.textChanged.emit())
        self.textEdited[str].connect(lambda o: self.textEdited.emit())
        self.editingFinished[str].connect(lambda o: self.editingFinished.emit())

        lineEdit = QLineEdit(parent=self, **kwargs)
        lineEdit.editingFinished.connect(self._onEditingFinished)
        lineEdit.textChanged.connect(self._onTextChanged)

        lineEdit.setReadOnly(kwargs['readOnly'])
        lineEdit.setClearButtonEnabled(not kwargs['readOnly'])

        layout = QHBoxLayout(self)
        layout.addWidget(lineEdit)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.lineEdit = lineEdit

    def _onEditingFinished(self):
        if self._modified is False:
            self.logger.log(logging.DEBUG - 1, '_onEditingFinished SKIPPED')
            return
        self.logger.log(logging.DEBUG-1, '_onEditingFinished')

        err = self.errorCheck()
        self._modified = False

        if err != self.getError():
            self.setError(err)
        else:
            self.refreshColors()
        self.editingFinished[str].emit(self.text())

    def _onTextChanged(self, text):
        self.logger.log(logging.DEBUG-1, f"_onTextChanged('{text}')")
        self._modified = True

        if self._liveErrorChecking is True:
            err = self.errorCheck()
            if err != self.getError():
                self.setError(err)
                # self.textChanged[str].emit(text)
                # return
        self.refreshColors()
        self.textChanged[str].emit(text)

    def getStatus(self):
        """Get widget status for color selection.

        :return: str, key for autoColors[key]
        """
        if bool(self._error):
            status = 'error'
            if self.isEnabled() is False or self.isReadOnly() is True:
                status += '-readonly'
        elif self.isEnabled() is False:
            status = 'disabled'
        elif self.isReadOnly() is True:
            status = 'readonly'
        elif self.text() == '':
            status = 'blank'
        else:
            status = 'default'
        return status

    def makeStyleString(self, colors=None):
        """Get a styleSheet string built from provided 'colors' or the defaults.

        :param colors: None-> use defaults
            OR str-> key for autoColors dict
            OR colors dict->use provided colors
            OR colors tuple->use provided colors
        :return: str, use in setStyleSheet()
        """
        self.logger.log(logging.DEBUG-1, f"makeStyleString({colors})")
        if colors is None:
            colors = self._autoColors[self.getStatus()]
        elif isinstance(colors, str):
            colors = self._autoColors[colors]

        if isinstance(colors, tuple) and _isColorTuple(colors):
            v0, v1 = colors[0], colors[1]
            if isinstance(v0, tuple):
                v0 = "rgb{}".format(str(v0[:])).replace(' ', '')
            if isinstance(v1, tuple):
                v1 = "rgb{}".format(str(v1[:])).replace(' ', '')

            string = "QLineEdit {background-color: " + str(v0) + "; color: " + str(v1) + ";}\n"
            # string += "QLineEdit:focus { border: 2px solid black; }\n"
            return string

        else:
            raise TypeError('makeStyleString takes a colors dict (see .setAutoColors for format). ' +
                            f'You provided: {colors}')

    def setStyleSheet(self, styleSheet):
        """Set stylesheet, set color control to manual.

        :param styleSheet: str
        :return:
        """
        self._manualColors = True
        super().setStyleSheet(styleSheet)

    def setLiveErrorChecking(self, mode):
        """Enable or disable liveErrorChecking.

        :param mode: bool
        :return:
        """
        self.logger.log(logging.DEBUG-1, f'setLiveErrorChecking({mode})')
        self._liveErrorChecking = mode

        if mode is True:
            self.setError(self.errorCheck())

    def refreshColors(self):
        """Update widget colors if set to automatic."""
        self.logger.log(logging.DEBUG-1, 'refreshColors:' +
                      f' error:\'{str(self.getError())}\' disabled:{str(not self.isEnabled())}' +
                      f' readonly:{str(self.isReadOnly())} text:\'{self.text()}\''
                      )

        if self._manualColors is False:
            super().setStyleSheet(self.makeStyleString())
            self.style().polish(self)

    def setColors(self, colors=None):
        """Manually set box's colors. Will remain set until .setAutoColors()

        :param colors: str as key for autoColors dict
                    OR tuple of colors eg.:
                        format: (backgroundColor, textColor)
                        e.g. ('black', 'white')
                            ('#000000', '#FFFFFF')
                *if colors is None, uses already stored autoColors['default']
        :return:
        """
        self.logger.debug(f'setColors({str(colors)})')
        self._manualColors = True

        if colors is None:
            self.logger.log(logging.DEBUG-1, 'setColors(default)')
            self.setColors(self._autoColors['default'])
        else:
            self.logger.log(logging.DEBUG-1, 'setColors(makeStyleString)')
            super().setStyleSheet(self.makeStyleString(colors))

    def autoColors(self):
        """Get current color settings dict.
        :return: dict
        """
        return self._autoColors

    def setAutoColors(self, colors=None):
        """Set the automatic colors, changes mode to use them until .setColors()
        If colors is None, uses already stored automatic colors.

        :param colors: dict of tuples of color strings or QColors
            format:
            colors={
                'default': X,           # normal editing mode
                'blank': X,             # box is editable but blank
                'disabled': X,          # box is not editable or selectable
                'readonly': X,          # box is not editable
                'error': X,             # box is editable and has an error
                'error-readonly': X     # box is not editable, but has an error
            }
            Where each X is the respective color tuple matching format:
                (backgroundColor, textColor)
            *all keys are optional, dict will be used to update currently stored autoColors.
        :return:
        """
        self.logger.debug(f'setAutoColors({str(colors)})')

        # update self._autoColors dict with provided colors
        if colors is not None and _isColorDict(colors):
            _colors = copy(self._autoColors)
            _colors.update(colors)
            self._autoColors = _colors

        # set mode to automatic
        self._manualColors = False
        self.refreshColors()

    def setText(self, text):
        self.logger.debug(f"setText('{text}')")
        self.lineEdit.setText(text)
        self.editingFinished[str].emit(text)

    def setReadOnly(self, status):
        """Set the box editable or fixed.

        :param status: box's editable status
            True: uneditable
            False: editable
        :return:
        """
        self.logger.debug(f'setReadOnly({str(status)})')

        self.lineEdit.setReadOnly(status)
        self.lineEdit.setClearButtonEnabled(not status)
        self.refreshColors()

    def setDisabled(self, status):
        """Set the box disabled or enabled.

        :param status: NOT box's enabled status
            True: unselectable, uneditable
            False: selectable (editability dictated by readOnly)
        :return:
        """
        self.setEnabled(not status)

    def setEnabled(self, status):
        """Set the box disabled or enabled.

        :param status: box's enabled status
            True: selectable (editability dictated by readOnly)
            False: unselectable, uneditable
        :return:
        """
        self.logger.debug(f'setEnabled({str(status)})')

        if status is False:
            self.setFocusPolicy(QtCore.Qt.NoFocus)
            QWidget.setEnabled(self, status)
            self.lineEdit.setEnabled(status)
        else:
            QWidget.setEnabled(self, status)
            self.lineEdit.setEnabled(status)
            self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.refreshColors()

    def popArgs(self, kwargs):
        args = self.defaultArgs.copy()
        for k in args:
            if k in kwargs:
                args[k] = kwargs.pop(k)
        return args


class EntryWidget(AutoColorLineEdit):
    """A DictComboBox after an AutoColorLineEdit.
    DictComboBox (.comboBox):
        Set options with obj.setOptions(['opt1', 'opt2', 'op3'])
        Get options with obj.getOptions()
        Set selected with obj.setSelected('opt2')
        Get selected with obj.getSelected()
        Set/unset ReadOnly with obj.setOptionFixed(bool)

    signals:
        optionChanged([], [str])  # emits newly selected option when selection is changed
        optionIndexChanged([], [int])  # emits new selection index when changed
        dataChanged([], [object])  # emits data attached to new selection

    All arguments are optional and must be provided by keyword, except 'parent' which can be positional.
    kwargs listed here will be passed to constructors of AutoColorLineEdit/DictComboBox

    Widget kwargs
    :param parent: Parent Qt Object (default None for individual widget)
    :param errorCheck: callable, returns error status, called with widget as first argument
    :param objectName: str, name of object for logging and within Qt
    :param readOnly: bool, whether the text box is editable

    QLineEdit kwargs
    :param text: str, starting text
    :param autoColors: dict of tuples of color strings; see help(setAutoColor) for formatting
    :param liveErrorChecking: bool, whether error checking occurs
                after every keystroke (=True) or only after text editing is finished (=False)

    DictComboBox kwargs
    :param options: [str, str, ...]
    :param optionFixed: bool, whether option is fixed or can be changed

    written by Tim Olson - timjolson@user.noreplay.github.com
    """
    defaultArgs = AutoColorLineEdit.defaultArgs.copy()
    defaultArgs.update({'options': list(['opt1', 'opt2']), 'optionFixed': False})

    optionChanged = pyqtSignal([],[str])
    optionIndexChanged = pyqtSignal([],[int])
    dataChanged = Qt.pyqtSignal([], [object])

    getSelected, setSelected, setOptionFixed, currentData = \
        delegated.methods('comboBox', 'currentText, setCurrentText, setDisabled, currentData')

    # selected_option = Qt.pyqtProperty(str, lambda s: s.getSelected(), lambda s, p: s.setSelected(p))

    def __init__(self, parent=None, **kwargs):
        # options = kwargs.pop('options', type(self).defaultArgs['options'])
        kwargs.setdefault('options', self.defaultArgs['options'])
        # optionFixed = kwargs.pop('optionFixed', type(self).defaultArgs['optionFixed'])
        kwargs.setdefault('optionFixed', self.defaultArgs['optionFixed'])
        self._isReadOnly = kwargs['readOnly'] if 'readOnly' in kwargs else False

        AutoColorLineEdit.__init__(self, parent, **kwargs)

    def setupUi(self, kwargs):
        self.optionChanged[str].connect(lambda o: self.optionChanged.emit())
        self.optionIndexChanged[int].connect(lambda o: self.optionIndexChanged.emit())
        self.dataChanged[object].connect(lambda o: self.dataChanged.emit())

        options = kwargs.pop('options')
        optionFixed = kwargs.pop('optionFixed')

        AutoColorLineEdit.setupUi(self, kwargs)

        combo = DictComboBox(parent=self, options=options)
        combo.currentTextChanged.connect(self._onOptionChanged)
        # combo.setStyleSheet("DictComboBox:focus, DictComboBox:on { background-color: white; border: 2px solid black; }")
        combo.setDisabled(optionFixed)
        combo.setSizeAdjustPolicy(DictComboBox.AdjustToContents)
        self.layout().insertWidget(1, combo)
        self.comboBox = combo

    def _onOptionChanged(self, text):
        self.setError(self.errorCheck())
        self.optionChanged[str].emit(text)
        self.optionIndexChanged[int].emit(self.comboBox.currentIndex())
        self.dataChanged[object].emit(self.currentData())

    def getOptions(self):
        """Get list of DictComboBox options.

        :return: [option_strings]
        """
        return self.comboBox.allItems()
    options = getOptions

    def setOptions(self, options):
        """Set list of DictComboBox options.

        :param options: iterable of strings
        :return:
        """
        self.logger.debug(f'setOptions({str(options)})')
        self.comboBox.setAllItems(options)

    def optionFixed(self):
        return not self.comboBox.isEnabled()

    def setEnabled(self, status):
        """Set the box disabled or enabled.

        :param status: box's enabled status
            True: selectable (editability dictated by readOnly)
            False: unselectable, uneditable
        :return:
        """
        self.logger.debug(f'setEnabled({str(status)})')
        self.comboBox.setEnabled(status)
        AutoColorLineEdit.setEnabled(self, status)  # QLineEdit, refreshColors()

        self.setReadOnly(not status)

    def setReadOnly(self, status):
        """Set the box editable or fixed.

        :param status: box's editable status
            True: uneditable
            False: editable
        :return:
        """
        self.logger.debug(f'setReadOnly({str(status)})')
        self.setOptionFixed(status)
        AutoColorLineEdit.setReadOnly(self, status)  # QLineEdit, refreshColors()
        self._isReadOnly = status

    def isReadOnly(self):
        return self._isReadOnly


__all__ = ['AutoColorLineEdit', 'EntryWidget']

if __name__ == '__main__':
    from qt_utils.designer import install_plugin_files
    install_plugin_files('entrywidget_designer_plugin.py')
