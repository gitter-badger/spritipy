from codecs import open
from setuptools import setup


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
        'shutil',
        'scipy'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
    ],
)
