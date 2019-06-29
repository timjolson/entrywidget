from PyQt5.QtWidgets import QLineEdit, QLabel, QComboBox, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtProperty, Qt, pyqtSignal
from PyQt5.QtGui import QColor
from copy import copy
from qt_utils import loggableQtName, ErrorMixin
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
    """A QLineEdit (in a QHBoxLayout) with error checking options linked to automatic color updates.
    QLineEdit (.lineEdit):
        Change with obj.setText('new text')
        Read with obj.text()

    All arguments are optional and must be provided by keyword, except 'parent' which can be positional.

    :param parent: Parent Qt Object (default None for individual widget)
    :param objectName: str, name of object for logging and within Qt
    :param text: str, starting text
    :param autoColors: dict of tuples of color strings; see help(setAutoColor) for formatting
    :param readOnly: bool, whether the text box is editable
    :param liveErrorChecking: bool, whether error checking occurs
                after every keystroke (=True) or only after text editing is finished (=False)

    written by Tim Olson - timjolson@user.noreplay.github.com
    """
    name = loggableQtName
    editingFinished = pyqtSignal()
    textChanged = pyqtSignal(str)
    textEdited = pyqtSignal(str)

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
        'text': ''
    }
    text, palette = delegated.methods('lineEdit', 'text, palette')
    clear, setClearButtonEnabled, isReadOnly = delegated.methods('lineEdit', 'clear setClearButtonEnabled isReadOnly')
    mousePressEvent, mouseReleaseEvent = delegated.methods('lineEdit', 'mousePressEvent, mouseReleaseEvent')
    keyPressEvent, keyReleaseEvent = delegated.methods('lineEdit', 'keyPressEvent, keyReleaseEvent')
    focusInEvent, focusOutEvent = delegated.methods('lineEdit', 'focusInEvent, focusOutEvent')

    def __init__(self, parent=None, **kwargs):
        autoColors = kwargs.pop('autoColors', type(self).defaultArgs['autoColors'])
        liveErrorChecking = kwargs.pop('liveErrorChecking', type(self).defaultArgs['liveErrorChecking'])
        self._setupText = kwargs.pop('text', type(self).defaultArgs['text'])
        self._setupReadOnly = kwargs.pop('readOnly', False)

        QWidget.__init__(self, parent, **kwargs)
        ErrorMixin.__init__(self)
        self._error = False
        self._manualColors = False  # whether colors are manually set or automatic
        self._liveErrorChecking = liveErrorChecking
        self._modified = False

        self.logger = logging.getLogger(self.name)
        self.logger.addHandler(logging.NullHandler())

        # verify format of 'autoColors', combine with defaults
        if _isColorDict(autoColors):
            defcolors = type(self).defaultColors.copy()
            defcolors.update(autoColors)
            autoColors = defcolors
        elif autoColors is None:
            autoColors = type(self).defaultColors.copy()
        else:
            raise TypeError(f"Unrecognized format {autoColors}")
        self._autoColors = autoColors

        self.setupUi()

        self.errorChanged.connect(lambda e: self.refreshColors())
        self._error = self.errorCheck()
        self.refreshColors()

    def setupUi(self):
        lineEdit = QLineEdit(parent=self, text=self._setupText, readOnly=self._setupReadOnly)
        lineEdit.editingFinished.connect(self._onEditingFinished)
        lineEdit.textChanged.connect(self._onTextChanged)
        lineEdit.setClearButtonEnabled(not self._setupReadOnly)

        layout = QHBoxLayout(self)
        layout.addWidget(lineEdit)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.lineEdit = lineEdit

        del self._setupText, self._setupReadOnly

    def _onEditingFinished(self):
        if self._modified is False:
            return
        self.logger.debug('_onEditingFinished')

        err = self.errorCheck()
        self._modified = False

        if err != self.getError():
            self.setError(err)
        else:
            self.refreshColors()
        self.editingFinished.emit()

    def _onTextChanged(self, text):
        self.logger.debug(f"_onTextChanged('{text}')")
        self._modified = True

        if self._liveErrorChecking is True:
            err = self.errorCheck()
            if err != self.getError():
                self.setError(err)
                self.textChanged.emit(text)
                return
        self.refreshColors()
        self.textChanged.emit(text)

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
        self.logger.debug(f"makeStyleString({colors})")
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
            string += "QLineEdit:focus { border: 2px solid black; }\n"
            return string

        else:
            raise TypeError('makeStyleString takes a colors dict (see .setAutoColors for format). ' +
                            f'You provided: {colors}')

    def setStyleSheet(self, styleSheet):
        self._manualColors = True
        super().setStyleSheet(styleSheet)

    def setLiveErrorChecking(self, mode):
        """Enable or disable liveErrorChecking.

        :param mode: bool
        :return:
        """
        self.logger.debug(f'setLiveErrorChecking({mode})')
        if mode != self._liveErrorChecking:
            self._liveErrorChecking = mode

        if mode is True:
            self.logger.debug('errorCheck')
            self.setError(self.errorCheck())

    def refreshColors(self):
        """Update widget colors if set to automatic."""
        self.logger.debug('refreshColors:' +
                      f' error:\'{str(self.getError())}\' disabled:{str(not self.isEnabled())}' +
                      f' readonly:{str(self.isReadOnly())} text:\'{self.text()}\''
                      )

        if self._manualColors is False:
            super().setStyleSheet(self.makeStyleString())

    def setColors(self, colors=None):
        """Manually set box's colors. Will remain set until .setAutoColors()

        :param colors: str as key for autoColors dict
                    OR tuple of colors eg.:
            format: (backgroundColor, textColor)
            e.g. ('black', 'white')
                ('#000000', '#FFFFFF')
            if colors is None, uses already stored autoColors['default']
        :return:
        """
        self.logger.debug(f'setColors({str(colors)})')
        self._manualColors = True

        if colors is None:
            self.logger.debug('setColors(default)')
            self.setColors(self._autoColors['default'])
        else:
            self.logger.debug('setColors(makeStyleString)')
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
            Keys are optional, dict will be used to update currently stored autoColors.
        :return:
        """
        self.logger.debug(f'setAutoColors({str(colors)})')

        # update self._autoColors dict with provided colors
        if colors is not None and _isColorDict(colors):
            _colors = copy(self.defaultColors)
            _colors.update(colors)
            self._autoColors = _colors

        # set mode to automatic
        self._manualColors = False
        self.refreshColors()

    def setText(self, text):
        self.lineEdit.setText(text)
        self._modified = True
        self.editingFinished.emit()

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
            self.setFocusPolicy(Qt.NoFocus)
            QWidget.setEnabled(self, status)
            self.lineEdit.setEnabled(status)
        else:
            QWidget.setEnabled(self, status)
            self.lineEdit.setEnabled(status)
            self.setFocusPolicy(Qt.StrongFocus)

        self.refreshColors()


class LabelLineEdit(AutoColorLineEdit):
    """A QLabel next to an AutoColorLineEdit.
    QLabel (.label):
        Change with obj.setLabel('new text')
        Read with obj.getLabel()

    All arguments are optional and must be provided by keyword, except 'parent' which can be positional.
    kwargs listed here will be passed to constructors of QLineEdit/QLabel

    Widget kwargs
    :param parent: Parent Qt Object (default None for individual widget)
    :param objectName: str, name of object for logging and within Qt
    :param readOnly: bool, whether the text box is editable

    QLineEdit kwargs
    :param text: str, starting text
    :param autoColors: dict of tuples of color strings; see help(setAutoColor) for formatting
    :param liveErrorChecking: bool, whether error checking occurs
                after every keystroke (=True) or only after text editing is finished (=False)

    QLabel kwargs
    :param label: str, label text

    written by Tim Olson - timjolson@user.noreplay.github.com
    """
    defaultArgs = AutoColorLineEdit.defaultArgs.copy()
    defaultArgs.update(label='Label')

    def __init__(self, parent=None, **kwargs):
        self._setupLabelText = kwargs.pop('label', type(self).defaultArgs['label'])
        AutoColorLineEdit.__init__(self, parent, **kwargs)

    def setupUi(self):
        AutoColorLineEdit.setupUi(self)  # QLineEdit, layout
        label = QLabel(parent=self, text=self._setupLabelText)
        self.layout().insertWidget(0, label)
        self.label = label
        # self.label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        del self._setupLabelText

    def setLabel(self, text):
        """Set QLabel text

        :param text: str, QLabel text
        :return:
        """
        self.logger.debug(f'setLabel(\'{str(text)}\')')
        self.label.setText(text)

    def getLabel(self):
        """Get QLabel text

        :return: str, QLabel text
        """
        self.logger.debug(f'getLabel(): \'{self.label.text()}\'')
        return self.label.text()


class EntryWidget(LabelLineEdit):
    """A QComboBox after a LabelLineEdit.
    QComboBox (.comboBox):
        Set options with obj.setOptions(['opt1', 'opt2', 'op3'])
        Get options with obj.getOptions()
        Set selected with obj.setSelected('opt2')
        Get selected with obj.getSelected()
        Set/unset ReadOnly with obj.setOptionFixed(bool)

    All arguments are optional and must be provided by keyword, except 'parent' which can be positional.
    kwargs listed here will be passed to constructors of QLineEdit/QLabel/QComboBox

    Widget kwargs
    :param parent: Parent Qt Object (default None for individual widget)
    :param objectName: str, name of object for logging and within Qt
    :param readOnly: bool, whether the text box is editable

    QLineEdit kwargs
    :param text: str, starting text
    :param autoColors: dict of tuples of color strings; see help(setAutoColor) for formatting
    :param liveErrorChecking: bool, whether error checking occurs
                after every keystroke (=True) or only after text editing is finished (=False)

    QLabel kwargs
    :param label: str, label text

    QComboBox kwargs
    :param options: [str, str, ...]
    :param optionFixed: bool, whether option is fixed or can be changed

    written by Tim Olson - timjolson@user.noreplay.github.com
    """
    defaultArgs = LabelLineEdit.defaultArgs.copy()
    defaultArgs.update({'options': list(['opt1', 'opt2']), 'optionFixed': False})
    optionChanged = pyqtSignal(str)
    optionIndexChanged = pyqtSignal(int)

    getSelected, setSelected, setOptionFixed = \
        delegated.methods('comboBox', 'currentText, setCurrentText, setDisabled')

    def __init__(self, parent=None, **kwargs):
        options = kwargs.pop('options', type(self).defaultArgs['options'])
        self._setupOptionFixed = kwargs.pop('optionFixed', type(self).defaultArgs['optionFixed'])
        self._selectedOption = ''
        self._options = options

        LabelLineEdit.__init__(self, parent, **kwargs)

    def setupUi(self):
        LabelLineEdit.setupUi(self)  # QLineEdit, layout, QLabel
        combo = QComboBox(self)
        combo.currentTextChanged.connect(self.optionChanged.emit)
        combo.currentTextChanged.connect(self._onOptionChanged)
        combo.currentIndexChanged.connect(self.optionIndexChanged.emit)
        combo.setStyleSheet("QComboBox:focus, QComboBox:on { background-color: white; border: 2px solid black; }")
        combo.addItems(self._options)
        combo.setDisabled(self._setupOptionFixed)
        combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.layout().insertWidget(2, combo)
        self.comboBox = combo

        del self._setupOptionFixed

    def _onOptionChanged(self, text):
        self.setError(self.errorCheck())

    def getOptions(self):
        """Get list of QComboBox options.

        :return: [option_strings]
        """
        return self._options.copy()
    options = getOptions

    def setOptions(self, options):
        """Set list of QComboBox options.

        :param options: iterable of strings
        :return:
        """
        self.logger.debug(self.name + f'setOptions({str(options)})')
        self.comboBox.clear()

        # ordered set
        options = {o:None for o in options}
        options = list(options.keys())

        self.comboBox.addItems(options)
        # self.comboBox.setCurrentIndex(0)
        self._options = options
        # i = self._optionList.findText(selected, Qt.MatchFixedString)

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
        LabelLineEdit.setEnabled(self, status)  # QLineEdit, refreshColors()
        self.label.setEnabled(status)

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
        LabelLineEdit.setReadOnly(self, status)  # QLineEdit, refreshColors()


class ButtonLineEdit(LabelLineEdit):
    """A QPushButton next to an AutoColorLineEdit.
    QPushButton (.label):
        Change with obj.setLabel('new text')
        Read with obj.getLabel()

    All arguments are optional and must be provided by keyword, except 'parent' which can be positional.
    kwargs listed here will be passed to constructors of QLineEdit/QLabel

    Widget kwargs
    :param parent: Parent Qt Object (default None for individual widget)
    :param objectName: str, name of object for logging and within Qt
    :param readOnly: bool, whether the text box is editable

    QLineEdit kwargs
    :param text: str, starting text
    :param autoColors: dict of tuples of color strings; see help(setAutoColor) for formatting
    :param liveErrorChecking: bool, whether error checking occurs
                after every keystroke (=True) or only after text editing is finished (=False)

    QPushButton kwargs
    :param label: str, label text

    written by Tim Olson - timjolson@user.noreplay.github.com
    """
    clicked = pyqtSignal()

    def setupUi(self):
        AutoColorLineEdit.setupUi(self)  # QLineEdit, layout
        label = QPushButton(parent=self, text=self._setupLabelText)
        label.clicked.connect(self.clicked.emit)
        self.layout().insertWidget(0, self.label)
        self.label = label

        # self.label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        del self._setupLabelText


class ButtonEntryWidget(ButtonLineEdit):
    """A QComboBox after a ButtonLineEdit.
    QComboBox (.comboBox):
        Set options with obj.setOptions(['opt1', 'opt2', 'op3'])
        Get options with obj.getOptions()
        Set selected with obj.setSelected('opt2')
        Get selected with obj.getSelected()
        Set/unset ReadOnly with obj.setOptionFixed(bool)

    All arguments are optional and must be provided by keyword, except 'parent' which can be positional.
    kwargs listed here will be passed to constructors of QLineEdit/QLabel/QComboBox

    Widget kwargs
    :param parent: Parent Qt Object (default None for individual widget)
    :param objectName: str, name of object for logging and within Qt
    :param readOnly: bool, whether the text box is editable

    QLineEdit kwargs
    :param text: str, starting text
    :param autoColors: dict of tuples of color strings; see help(setAutoColor) for formatting
    :param liveErrorChecking: bool, whether error checking occurs
                after every keystroke (=True) or only after text editing is finished (=False)

    QPushButton kwargs
    :param label: str, label text

    QComboBox kwargs
    :param options: [str, str, ...]
    :param optionFixed: bool, whether option is fixed or can be changed

    written by Tim Olson - timjolson@user.noreplay.github.com
    """
    def setupUi(self):
        ButtonLineEdit.setupUi(self)  # QLineEdit, layout, QPushButton
        combo = QComboBox(self)
        combo.currentTextChanged.connect(self.optionChanged.emit)
        combo.currentTextChanged.connect(self._onOptionChanged)
        combo.currentIndexChanged.connect(self.optionIndexChanged.emit)
        combo.setStyleSheet("QComboBox:focus, QComboBox:on { background-color: white; border: 2px solid black; }")
        combo.addItems(self._options)
        combo.setDisabled(self._setupOptionFixed)
        combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.layout().insertWidget(2, combo)
        self.comboBox = combo

        del self._setupOptionFixed


__all__ = ['AutoColorLineEdit', 'LabelLineEdit', 'EntryWidget', 'ButtonLineEdit', 'ButtonEntryWidget']
