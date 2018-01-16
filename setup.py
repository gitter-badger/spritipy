import sys
from codecs import open
from setuptools import setup

if not sys.version_info[0] == 3:
    sys.exit("\n#####################################\n"
             "  Spritipy does not support python 2.\n"
             "  Please install using python 3.x\n"
             "#####################################\n")

with open('README.md', encoding='utf-8') as fd:
    LONG_DESCRIPTION = fd.read()

setup(
    name='spritipy',
    long_description=LONG_DESCRIPTION,
    license='MIT',
    packages=['spritipy'],
    url='https://github.com/brainsprite/spritipy',
    include_package_data=True,
    install_requires=[
        'matplotlib',
        'PILLOW',
        'numpy',
        'nibabel',
        'nilearn',
        'scipy',
        'sklearn',
        'pyqt5'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
    ],
)
