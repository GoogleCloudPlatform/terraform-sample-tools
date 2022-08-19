#!/usr/bin/env python3.8
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Setup for TF tools."""

import io

from setuptools import setup, find_packages


INSTALL_REQUIRES = open('requirements.txt').readlines()


with io.open("README.md") as readme:
    setup(
        name="tftools",
        version="2.0.1b",
        description="Terraform Tools for Magic Modules Developers",
        long_description=readme.read(),
        license="Apache License Version 2.0",
        author="Sampath Kumar Maddula",
        author_email="sampathm@google.com",
        url="https://github.com/GoogleCloudPlatform/terraform-sample-tools/tree/main/tools/magic-modules-tftools",
        classifiers=[
            # 'Development Status :: 5 - Production/Stable',
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: Apache License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            # 'Topic :: Software Development :: Libraries :: Python Modules',
            # 'Topic :: Software Development :: Quality Assurance',
        ],
        keywords="Google Cloud Docs, GCP, MagicModules, Terraform, Code, Snippet, Samples",
        install_requires=INSTALL_REQUIRES,
        py_modules=["tftools"],
        packages=['bin', 'AntParser', 'AntParser.lang'],
        zip_safe=False,
        entry_points={"console_scripts": ["tftools = tftools:main"]},
    )
