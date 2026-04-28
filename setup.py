# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='stepxmlclient',
      version='0.9.4',
      description='STEP-XML Client',
      author='Claudius Hansch',
      author_email='claudius.hansch@hoerl-im.de',
      packages=find_packages(include=["stepxmlclient*"]),
      package_data={
          'stepxmlclient': ['openapi.json'],
      },
      install_requires=['requests-openapi', 'requests', 'pydantic>=2.0']
      )
