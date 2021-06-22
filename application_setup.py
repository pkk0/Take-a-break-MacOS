from setuptools import setup
from application import APP_NAME

APP = ['application.py']
APP_VERSION = '1.0'
PY_MODULES = ['global_memory', 'system_wakes_daemon']
DATA_FILES = ['config.INI']
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
        'CFBundleShortVersionString': APP_VERSION,
        'NSHumanReadableCopyright': '© 2021 Piotr \'pkk0\' Uliński'
    },
    'packages': ['rumps'],
}

setup(
    name=APP_NAME,
    app=APP,
    py_modules=PY_MODULES,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
