#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup for TF tools."""

import ast
import io

from setuptools import setup


INSTALL_REQUIRES = (
    ['termcolor']
)



with io.open('README.md') as readme:
    setup(
        name='tftools',
        version='0.1',
        description='Terraform Tools for Magic Modules Developers',
        long_description=readme.read(),
        license='Apache License Version 2.0',
        author='Hideo Hattori',
        author_email='hhatto.jp@gmail.com',
        url='https://github.com/msampathkumar/MagicModules-TerraformTools',
        classifiers=[
            # 'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: Apache License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            # 'Topic :: Software Development :: Libraries :: Python Modules',
            # 'Topic :: Software Development :: Quality Assurance',
        ],
        keywords='terraform, magimodules',
        install_requires=INSTALL_REQUIRES,
        py_modules=['convert2tf', 'convert2erb', 'tftools'],
        zip_safe=False,
        entry_points={'console_scripts': ['tftools = tftools:main']},
    )