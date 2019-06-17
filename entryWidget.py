from PyQt5.QtWidgets import QLineEdit, QLabel, QComboBox, QWidget, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import pyqtProperty, Qt, QSize
from copy import copy
from types import MethodType
from qt_utils import loggableQtName
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class _LineEditHelper(QLineEdit):
    """
    QLineEdit subclass, with additional 'error' pyqtProperty with helpers, and defaultColors dict
    for default automatic color scheme.
    """
    defaultColors = {
        'error-readonly': ('orangered', 'white'),
        'error': ('yellow', 'black'),
        'default': ('white', 'black'),
        'blank': ('lightblue', 'black'),
        'disabled': ('#F0F0F0', 'black'),
        'readonly': ('#F0F0F0', 'black')
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._error = False
        self._styleString = ''

    @pyqtProperty(bool)
    def error(self):
        return bool(self._error)

    @error.setter
    def error(self, status):
        """pyqtProperty, bool. Used for automatic formatting.
        Pass any type, such that:
         bool(status) == True for an error
         bool(status) == False for no error

        :param status: any, current error status
            self.hasError() = self.error = bool(self.isError())
        :return: bool(self.isError())
        """
        self._error = status
        if bool(status):
            self.setToolTip('Error:\n' + str(status))
        else:
            self.setToolTip('')
        self.refreshColors()

    def hasError(self):
        """Get error status bool.

        :return: bool, whether the widget has an error
        """
        return self.error

    def getError(self):
        """Get current error value

        :return: any, current error value
        """
        return self._error

    def refreshColors(self):
        """Forces update of widget style.
        Uses self.setStyle(self.style())

        :return:
        """
        self.setStyle(self.style())

    @classmethod
    def _isColorDict(cls, colors):
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
            all(cls._isColorTuple(c) for c in colors.values())
        except AssertionError:
            raise AssertionError('provide a color dict; check help(setAutoColors) for more info')
        return True

    @classmethod
    def _isColorTuple(cls, colors):
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
        assert all(isinstance(c, (str, tuple)) for c in colors), \
            'provide a tuple of color strings, check help(setColor) for more info'
        return True

    def getStyleString(self):
        """Get the widget's current style sheet string.

        :return: string, current style sheet string
        """
        return self._styleString

    def setStyleSheet(self, p_str):
        """QWidget.setStyleSheet(), plus stores the style string in ._styleString

        :param p_str: string, style string (from makeStyleString() for convenience)
        :return:
        """
        self._styleString = p_str
        super().setStyleSheet(p_str)

    def makeStyleString(self, colors=None):
        """Get a styleSheet string built from provided 'colors' or the defaults.

        :param colors: None-> use defaults OR colors dict->use provided colors
        :return: str, use in setStyleSheet()
        """
        if colors is None:
            return self.makeStyleString(AutoColorLineEdit.defaultColors)

        if isinstance(colors, dict) and self._isColorDict(colors):
            _colors = copy(self.defaultColors)
            _colors.update(colors)

            for k, v in _colors.items():
                v0, v1 = v[0], v[1]
                if isinstance(v[0], tuple):
                    v0 = "rgb{}".format(str(v[0])).replace(' ', '')
                if isinstance(v[1], tuple):
                    v1 = "rgb{}".format(str(v[1])).replace(' ', '')
                _colors.update({k:(v0, v1)})

            string = \
                "QLineEdit[error=true] {background-color: " + \
                f"{_colors['error-readonly'][0]}; color: {_colors['error-readonly'][1]}" + ";}\n" + \
                "QLineEdit[error=true][enabled=true][readOnly=false] {background-color: " + \
                f"{_colors['error'][0]}; color: {_colors['error'][1]}" + ";}\n" + \
                "QLineEdit[error=false][enabled=true][readOnly=true] {background-color: " + \
                f"{_colors['readonly'][0]}; color: {_colors['readonly'][1]}" + ";}\n" + \
                "QLineEdit[error=false][enabled=false][readOnly=false] {background-color: " + \
                f"{_colors['disabled'][0]}; color: {_colors['disabled'][1]}" + ";}\n" + \
                "QLineEdit[error=false][enabled=false][readOnly=true] {background-color: " + \
                f"{_colors['disabled'][0]}; color: {_colors['disabled'][1]}" + ";}\n" + \
                "QLineEdit[error=false][enabled=true][readOnly=false] {background-color: " + \
                f"{_colors['default'][0]}; color: {_colors['default'][1]}" + ";}\n" + \
                "QLineEdit[error=false][enabled=true][readOnly=false][text=''] {background-color: " + \
                f"{_colors['blank'][0]}; color: {_colors['blank'][1]};" + "}\n"
        elif isinstance(colors, tuple) and self._isColorTuple(colors):
            v0, v1 = colors[0], colors[1]
            if isinstance(v0, tuple):
                v0 = "rgb{}".format(str(v0)).replace(' ', '')
            if isinstance(v1, tuple):
                v1 = "rgb{}".format(str(v1)).replace(' ', '')

            string = "QLineEdit {background-color: " + str(v0) + "; color: " + str(v1) + ";}\n"
        else:
            raise TypeError('makeStyleString takes a colors dict (see .setAutoColors for format). ' +
                            f'You provided: {colors}')

        # frame on focus
        string += "QLineEdit:focus { border: 2px solid black; }\n"

        return string


class AutoColorLineEdit(QWidget):
    """A QWidget subclass, with delegated functions from a QLineEdit (at ._editBox)
    Change text with obj.setText('new entry text')
    Read text with obj.text()
    Set/unset ReadOnly with obj.setReadOnly(bool)
    Set/unset Enabled with obj.setEnabled(bool)

    Change automatic colors:
        obj.setAutoColors( color_dict )
    Set widget to use stored automatic colors:
        obj.setAutoColors()
    Manually change colors:
        obj.setColors( color_tuple )
    Set widget to use manual colors:
        obj.setColors()

    Extended functionality:
        Attached callbacks will be automatically called upon different events.
        When called, the functions are passed the calling instance.
        Callbacks can be set by __init__ or by set* methods:
            setIsError, setOnError, setOnTextChanged, setOnEditingFinished

        See help(__init__) for more info on callbacks.

    written by Tim Olson - timjolson@user.noreplay.github.com
    """
    name = loggableQtName

    defaultColors = copy(_LineEditHelper.defaultColors)

    defaultArgs = \
        {'objectName': '', 'startPrompt': '', 'colors': defaultColors, 'liveErrorChecking': True,
         'readOnly': False, 'isError': (lambda x: x.hasError()),
         'onError': (lambda x: x.logger.debug('default onError()')),
         'onTextChanged': (lambda x: x.logger.debug('default onTextChanged()')),
         'onEditingFinished': (lambda x: x.logger.debug('default onEditingFinished()'))
         }

    def __init__(self, parent=None, **kwargs):
        """All arguments are optional and must be provided by keyword, except 'parent' which can be positional.

        :param parent: Parent Qt Object (default None for individual widget)
        :param objectName: string, name of object for logging and within Qt
        :param startPrompt: string, starting text for the entry box
        :param colors: dict of tuples of color strings; see help(setAutoColor) for formatting
        :param readOnly: bool, whether the text entry box is editable
        :param liveErrorChecking: bool, whether error checking occurs after every
                text change/keystroke (=True) or only after text editing is
                finished [return/enter/tab pressed, or click out of box] (=False)

        Optional callbacks (upon calling, widget is provided as argument)
        :param isError: function to call that returns an error status
                bool(isError())==True <-> there is an error [can pass numbers or text, etc.]
                bool(isError())==False <-> no error [empty string, empty list, None, etc.]
        :param onError: function to call when bool(isError())==True
        :param onTextChanged: function to call when text entry changes
        :param onEditingFinished: function to call when text editing is finished
        """
        args = AutoColorLineEdit.defaultArgs.copy()
        args.update(kwargs)
        self._inited = False  # flag to prevent a lot of extra work on setup

        super().__init__(parent)
        self.logger = logging.getLogger('.'.join([__name__, self.name]))
        self.logger.addHandler(logging.NullHandler())

        # put QLineEdit in a layout, connect slots, import attrs from _LineEditHelper
        self._setupUI()

        # store backends
        self._manualColors = False  # whether colors are manually set or automatic

        # verify format of 'colors', combine with defaults
        if self._isColorDict(args['colors']):
            _colors = copy(self.defaultColors)
            _colors.update(args['colors'])
            colors = _colors
        else:
            colors = copy(self.defaultColors)
        self._colors = colors

        # store backend
        if args['objectName']:
            self.setObjectName(args['objectName'])
        self._liveErrorChecking = args['liveErrorChecking']

        # attach callbacks
        self.setOnTextChanged(args['onTextChanged'])
        self.setOnEditingFinished(args['onEditingFinished'])
        self.setOnError(args['onError'])
        self.setIsError(args['isError'])

        if self.__class__.__name__ == 'AutoColorLineEdit':
            self._inited = True

        # set the initial text and readOnly
        self.setText(args['startPrompt'], args['readOnly'])

        # update display
        self.setAutoColors(colors)

    def _setupUI(self):
        self.setMinimumSize(QSize(215, 20))
        self.setMaximumSize(QSize(16777215, 20))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self._editBox = _LineEditHelper(self)
        self._editBox.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
        self._editBox.setMinimumSize(QSize(80, 20))
        self._editBox.setMaximumSize(QSize(16777215, 20))
        self._editBox.setClearButtonEnabled(True)
        self.horizontalLayout.addWidget(self._editBox)

        # signals
        self._editBox.textChanged['QString'].connect(self.textChanged)
        self._editBox.editingFinished.connect(self.editingFinished)

        # bring in QLineEdit methods
        for attr in ['setToolTip', 'text', 'setClearButtonEnabled', 'isReadOnly',
                     # 'refreshColors', 'getStyleString', 'makeStyleString',
                     '_isColorDict', '_isColorTuple', 'defaultColors', 'hasError']:
            setattr(self, attr, self._editBox.__getattribute__(attr))

    def getError(self):
        """Get error status.

        :return: any, error status
        """
        return self._editBox.getError()

    def setError(self, status):
        """Set error status. Also set via obj.isError() upon events.
        When bool(error)==True, widget text has an error.

        :param status: any
        :return:
        """
        self.logger.debug(self.name + f'setError(\'{str(status)}\')')

        self._editBox.error = status

        if bool(status):
            self.onError.__self__.onError()

    @property
    def manualColors(self):
        """Property, bool, whether colors are manually set or not.

        :return: bool, whether colors are manually set
        """
        return self._manualColors

    @manualColors.setter
    def manualColors(self, manual):
        """Property, bool, whether colors are manually set or not.

        :param manual: bool, whether colors are manually set or not.
        :return:
        """
        self._manualColors = manual

    def setLiveErrorChecking(self, mode):
        """Error checking mode property.

        :param mode: bool
            True: check for error with every text change
            False: check for error when editing is finished
        :return:
        """
        self.logger.debug(self.name + f'setLiveErrorChecking({str(mode)})')

        self._liveErrorChecking = mode
        if mode is True and self._inited is True:
            self.setError(self.isError.__self__.isError())

    def refreshColors(self):
        """Updates box's colors.
            If obj.manualColors=False, automatic colors are used.

        :return:
        """
        self.logger.debug(self.name + 'refreshColors:' +
                      f' error:\'{str(self.getError())}\' enabled:{str(self.isEnabled())}' +
                      f' readonly:{str(self.isReadOnly())} text:\'{self.text()}\''
                      )

        if self.manualColors is False:
            self._editBox.refreshColors()

    def setColors(self, colors=None):
        """Manually set box's colors. Will remain set until .setAutoColors()

        :param colors: tuple of color strings
            format: (backgroundColor, textColor)
            e.g. ('black', 'white')
                ('#000000', '#FFFFFF')
            if colors==None, uses already stored automatic colors['default']
        :return:
        """
        self.logger.debug(self.name + f'setColors({str(colors)})')
        self.manualColors = True

        if colors is None:
            self.logger.debug(self.name + 'setColors(default)')
            self.setColors(self._colors['default'])
        else:
            self.logger.debug(self.name + 'setColors(makeStyleString)')
            self._editBox.setStyleSheet(self._editBox.makeStyleString(colors))

    def setAutoColors(self, colors=None):
        """Set the automatic colors, changes mode to use them until .setColors()
            if colors==None, uses already stored automatic colors.

        :param colors: dict of tuples of color strings
            format:
            colors={
                'default': X,           # normal editing mode
                'blank': X,             # box is editable but blank
                'disabled': X,          # box is not editable or selectable
                'readonly': X,          # box is not editable
                'error': X,             # box is editable and has an error
                'error-readonly': X     # box is not editable, but has an error
            }
            Where each X is the respective color string tuple matching format:
                (backgroundColor, textColor)
        :return:
        """
        self.logger.debug(self.name + f'setAutoColors({str(colors)})')

        # update self._colors dict with provided colors
        if colors is not None and self._isColorDict(colors):
            _colors = copy(self.defaultColors)
            _colors.update(colors)
            self._colors = _colors

        # set mode to automatic
        self.manualColors = False
        self._editBox.setStyleSheet(self._editBox.makeStyleString(self._colors))

    def setReadOnly(self, readOnly):
        """Set readOnly mode of QLineEdit.

        :param readOnly: bool, True=readOnly, False=editable
        :return:
        """
        self.logger.debug(self.name + f'setReadOnly({str(readOnly)})')

        # change setting
        self._editBox.setReadOnly(readOnly)
        self._editBox.setClearButtonEnabled(not readOnly)

        self.refreshColors()

    def setEnabled(self, status):
        """Set the box disabled or enabled.

        :param status: box's enabled status
            True: selectable (editability dictated by readOnly)
            False: unselectable, uneditable
        :return:
        """
        self.logger.debug(self.name + f'setEnabled({str(status)})')

        if status is False:
            self._editBox.setFocusPolicy(Qt.NoFocus)
            self._editBox.setEnabled(status)
        else:
            self._editBox.setEnabled(status)
            self._editBox.setFocusPolicy(Qt.StrongFocus)

        self.refreshColors()

    def setText(self, text, readOnly=None):
        """Set entry text, and readOnly status of QLineEdit.

        :param text: string, text to put in the box
        :param readOnly: bool, whether box is readonly
            OR None-> do not change readonly mode
        :return:
        """
        self.logger.debug(self.name + f'setText(\'{str(text)}\', {str(readOnly)})')

        # change text
        self._editBox.setText(text)

        # change readonly
        if readOnly is not None:
            self._editBox.setReadOnly(readOnly)

        # run method for text editing finished
        if self._inited:
            self.onEditingFinished.__self__.onEditingFinished()

    def textChanged(self, text):
        """Called when textChanged signal received.
            Updates error status and colors when applicable.
            Runs an attached onTextChanged(self) callback

        :param text: latest text in box
        :return:
        """
        self.logger.debug(self.name + f'textChanged:\'{str(text)}\'')

        # error check and update colors
        if self._inited is True and (self._liveErrorChecking is True or self.text() == ''):
            self.setError(self.isError.__self__.isError())

        self.refreshColors()

        if self._inited:
            self.onTextChanged.__self__.onTextChanged()

    def setOnTextChanged(self, func):
        """Set function to run when box's text changes.

        :param func: MethodType, LambdaType, or FunctionType
            Function to run; is only passed this object.
            e.g. func(self)
        :return:
        """
        self.logger.debug('setOnTextChanged()')

        # change method
        self.onTextChanged = func if isinstance(func, MethodType) else MethodType(func, self)

    def editingFinished(self):
        """Called when editingFinished signal received.
            Updates error status and colors when applicable.
            Runs an attached onEditingFinished(self) callback

        :return:
        """
        self.logger.debug(self.name + 'editingFinished()')

        # error check
        if self._inited is True:
            self.setError(self.isError.__self__.isError())

        # run attached method
        if self._inited:
            self.onEditingFinished.__self__.onEditingFinished()

    def setOnEditingFinished(self, func):
        """Set function to run when box's text editing is finished.

        :param func: MethodType, LambdaType, or FunctionType
            Function to run; is only passed this object.
            e.g. func(self)
        """
        self.logger.debug(self.name + 'setOnEditingFinished()')

        # change method
        self.onEditingFinished = func if isinstance(func, MethodType) else MethodType(func, self)

    def setIsError(self, func):
        """Set function to run to check the box for errors.
            Function should return error status.

        :param func: MethodType, LambdaType, or FunctionType
            Function to run; is only passed this object.
            e.g. func(self)
        :return:
        """
        self.logger.debug(self.name + 'setIsError()')

        # change method
        self.isError = func if isinstance(func, MethodType) else MethodType(func, self)

        # error check
        if self._inited is True:
            self.setError(self.isError.__self__.isError())

    def setOnError(self, func):
        """Set function to run when box has an error.

        :param func: MethodType, LambdaType, or FunctionType
            Function to run; is only passed this object.
            e.g. func(self)
        :return:
        """
        self.logger.debug(self.name + 'setOnError()')

        # change method
        self.onError = func if isinstance(func, MethodType) else MethodType(func, self)

        # error check
        if self._inited is True:
            self.setError(self.isError.__self__.isError())


class LabelLineEdit(AutoColorLineEdit):
    """An AutoColorLineEdit subclass with additional QLabel.
    QLabel:
        Change with obj.setLabel('new text')
        Read with obj.getLabel()

    Extended functionality:
        Attached callbacks can be automatically called upon different events.
        When called, the functions are passed the calling instance.
        Callbacks can be set by __init__ or by set* methods:
            setOnLabelClick

        See help(__init__) for more info on callbacks.

    written by Tim Olson - timjolson@user.noreplay.github.com
    """

    defaultColors = copy(_LineEditHelper.defaultColors)

    def __init__(self, parent=None, label='Label',
                 onLabelClick=lambda x, y: x.logger.debug('default onLabelClick()'),
                 **kwargs):
        """All arguments are optional and must be provided by keyword, except 'parent' which can be positional.

        :param label: string, text for QLabel

        Optional callback:
        :param onLabelClick: function to call when label is clicked (Left or Right button, maybe others too)

        Also accepts all keyword arguments for an AutoColorLineEdit.
        """
        super().__init__(parent, **kwargs)

        # attach custom functions for label and combobox
        self.setOnLabelClick(onLabelClick)

        if self.__class__.__name__ == 'LabelLineEdit':
            self._inited = True

        # set initial values
        self.setLabel(label)

    def _setupUI(self):
        super()._setupUI()

        self._label = QLabel(self)
        self._label.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred))
        self._label.setMinimumSize(QSize(60, 20))
        self._label.setMaximumSize(QSize(80, 20))
        self._label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.horizontalLayout.insertWidget(0, self._label)

    def setOnLabelClick(self, func):
        """Set function to run when box's QLabel is clicked.

        :param func: MethodType, LambdaType, or FunctionType
            Function to run; is passed this object, and the mouseEvent
            e.g. func(self, event)
        :return:
        """
        self.logger.debug('setOnLabelClick()')
        self.onLabelClick = func if isinstance(func, MethodType) else MethodType(func, self)
        self._label.mousePressEvent = self.onLabelClick

    def setLabel(self, text):
        """Set QLabel text

        :param text: str, QLabel text
        :return:
        """
        self.logger.debug(self.name + f'setLabel(\'{str(text)}\')')
        self._label.setText(text)

    def getLabel(self):
        """Get QLabel text

        :return: str, QLabel text
        """
        self.logger.debug(self.name + f'getLabel():\'{self._label.text()}\'')
        return self._label.text()


class EntryWidget(LabelLineEdit):
    """A LabelLineEdit subclass with additional QComboBox.
        QComboBox:
            Set available options with obj.setOptions(['opt1', 'opt2', 'op3'])
            Get available options with obj.getOptions()
            Set current selection with obj.setSelected('opt2')
            Get current selection with obj.getSelected()
            Set/unset ReadOnly with obj.setOptionFixed(bool)

        Extended functionality:
            Attached callbacks can be automatically called upon different events.
            When called, the functions are passed the calling instance.
            Callbacks can be set by __init__ or by set* methods:
                setOnOptionChanged

            See help(__init__) for more info on callbacks.

        written by Tim Olson - timjolson@user.noreplay.github.com
        """

    defaultColors = copy(_LineEditHelper.defaultColors)

    defaultArgs = \
        {'options':list(['opt1', 'opt2']), 'optionFixed':False,
         'onOptionChanged': (lambda x: x.logger.debug('default onOptionChanged()'))
         }

    def __init__(self, parent=None, options=defaultArgs['options'], optionFixed=defaultArgs['optionFixed'],
                 onOptionChanged=defaultArgs['onOptionChanged'], **kwargs):
        """All arguments are optional and must be provided by keyword, except 'parent' which can be positional.

        :param options: list of strings, selectable options in QComboBox
        :param optionFixed: bool, whether the combobox is locked

        Optional callback:
        :param onOptionChanged: function to call when selected option is changed

        Also accepts all keyword arguments for a LabelLineEdit.
        """
        self._inited = False
        self._selectedOption = ''

        super().__init__(parent, **kwargs)

        # set initial values
        self.setOptions(options)
        self.setOptionFixed(optionFixed)

        # attach custom functions for label and combobox
        self.setOnOptionChanged(onOptionChanged)

        if self.__class__.__name__ == 'EntryWidget':
            self._inited = True

        self.setSelected(options[0], optionFixed)

    def _setupUI(self):
        super()._setupUI()

        self._optionList = QComboBox(self)
        self._optionList.setMinimumSize(QSize(0, 20))
        self._optionList.setMaximumSize(QSize(80, 20))
        self._optionList.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.horizontalLayout.insertWidget(2, self._optionList)

        # signals
        self._optionList.currentIndexChanged.connect(self.optionChanged)
        self._optionList.setStyleSheet(
            "QComboBox:focus, QComboBox:on { background-color: white; border: 2px solid black; }"
        )

    def getOptions(self):
        """Get list of QComboBox options.

        :return: [option_strings]
        """
        return self._options

    def setOptions(self, options):
        """Set list of QComboBox options.

        :param options: set, list, or tuple of strings
        :return:
        """
        self.logger.debug(self.name + f'setOptions({str(options)})')
        self._optionList.clear()
        self._optionList.addItems(set(options))
        self._options = options

        selected = options[0]
        i = self._optionList.findText(selected, Qt.MatchFixedString)
        self._optionList.setCurrentIndex(i)
        self._selectedOption = selected

    def setOptionFixed(self, fixed):
        """Set whether the widget's QComboBox is readOnly.

        :param fixed: bool, whether the QComboBox is readOnly
        :return:
        """
        self.logger.debug(self.name + f'setFixedOption({str(fixed)})')

        self._optionList.setEnabled(not fixed)
        self._optionFixed = fixed

    def setEnabled(self, status):
        """Set the widget disabled or enabled.

        :param status: bool, box's enabled status
            True: QLineEdit selectable (editability dictated by readOnly)
                  QComboBox adjustable
            False: QLineEdit not editable or selectable
                   QComboBox not adjustable
        :return:
        """
        super().setEnabled(status)
        self.setOptionFixed(not status)

    def optionChanged(self):
        """Called when option list emits currentIndexChanged signal.
            Updates _selectedOption to the current QComboBox selection.
            Runs attached onOptionChanged(self) callback.

        :return:
        """
        self.logger.debug(self.name + f'optionChanged():\'{self._optionList.currentText()}\'')
        self._selectedOption = self._optionList.currentText()

        if self._inited:
            self.onOptionChanged.__self__.onOptionChanged()

    def getSelected(self):
        """Get current QComboBox selection.

        :return: str, the QComboBox selected string
        """
        self.logger.debug(self.name + f'getSelected():\'{self._selectedOption}\'')
        return self._selectedOption

    def setSelected(self, selected, fixed=None):
        """Set the QComboBox's current selection.
            Calls attached onOptionChanged(self) callback.

        :param selected: string, QComboBox option to set as active selection
        :param fixed: bool, whether to set QComboBox readOnly
                OR None, no change to readOnly
        :return:
        """
        self.logger.debug(self.name + f'setSelected(\'{str(selected)}\')')

        i = self._optionList.findText(selected, Qt.MatchFixedString)
        assert i >= 0, "'" + selected + "' is not in the option list"

        self._optionList.setCurrentIndex(i)
        self._selectedOption = selected
        if fixed is not None:
            self._optionFixed = fixed

        self.refreshColors()

    def setOnOptionChanged(self, func):
        """Set function to run when QComboBox option changes.

        :param func: MethodType, LambdaType, or FunctionType
            Function to run; is only passed this object.
            e.g. func(self)
        :return:
        """
        self.logger.debug(self.name + 'setOnOptionChanged()')
        self.onOptionChanged = func if isinstance(func, MethodType) else MethodType(func, self)


__all__ = ['AutoColorLineEdit', 'LabelLineEdit', 'EntryWidget']
