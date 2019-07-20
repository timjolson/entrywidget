from setuptools import setup, find_packages


setup(
    name='entrywidget',
    version="0.7",
    packages = find_packages(),
    install_requires = ['PyQt5'],
    dependency_links = [
        'https://github.com/timjolson/generalutils.git',
        'https://github.com/timjolson/qt_utils.git',
    ],
    tests_require = ['pytest', 'pytest-qt']
)
