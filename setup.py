#!/usr/bin/python3

from distutils.core import setup

setup(name='recent',
      description='Command line news reader',
      author='Julian Rother',
      author_email='julian@toksik.org',
      url='https://github.com/toksik/recent',
      packages=['recent', 'recent.providers', 'recent.notifier',
                'recent.deps', 'recent.markup'],
      scripts=['bin/recent', 'bin/recent-daemon']
      )
