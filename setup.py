# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import setup, find_packages

setup(name='stepxmlclient',
      version='1.0.0',
      description='STEP-XML Client',
      long_description=Path(__file__).with_name('README.md').read_text(encoding='utf-8'),
      long_description_content_type='text/markdown',
      author='Everleah',
      author_email='everleah@hansch.info',
      license='MIT',
      license_files=['LICENSE'],
      python_requires='>=3.9',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
      packages=find_packages(include=["stepxmlclient*"]),
      install_requires=['requests-openapi', 'requests', 'pydantic>=2.0']
      )
