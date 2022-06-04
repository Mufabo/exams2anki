from setuptools import setup, find_packages

import sys
import os

if sys.version_info.major != 3:
    print('This Package is only compatible with Python 3, but you are running '
          'Python {}. The installation will likelyfail.'.format(sys.version_info.major))
          
setup(name='exams2anki',
      version='0.1.1',
      description='Turns examdumps form exam4training into Anki decks',
      author='M. Fatih Bostanci',
      author_email='fatbos1206@gmail.com',
      license='MIT',
      packages=find_packages(
        include=['exams2anki', 'exams2anki.*'])  # ["*"] by default)
    ,
      install_requires=[
        'requests',
        'bs4',
        'genanki',
        'hashlib',
        'sys'
        ],
      entry_points={
        "console_scripts": [
            "exams2anki=exams2anki.main:main"
        ]
      },
      zip_safe=False)