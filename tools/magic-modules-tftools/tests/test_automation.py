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
"""
System tests for TFTOOLS
"""
try:
    from test.bin import Erb2Tf, Tf2Erb, get_test_dirs
except ImportError:
    from bin import Erb2Tf, Tf2Erb, get_test_dirs
import pytest


@pytest.fixture(params=get_test_dirs(), scope="module")
def test_folder(request):
    return request.param


class TestTFTools:
    def _setup(self, test_folder):
        if "erb2tf" in test_folder:
            self.test_object = Erb2Tf()
        elif "tf2erb" in test_folder:
            self.test_object = Tf2Erb()
        else:
            assert False, "Input Error: Not able to determine Test Details"
        self.test_object.init_test_vars(test_folder)

    def test_input_files(self, test_folder):
        self._setup(test_folder)
        self.test_object.check_input_files()

    def test_run_tftools(self, test_folder):
        self._setup(test_folder)
        self.test_object.run_tftools()

    def test_output_file(self, test_folder):
        self._setup(test_folder)
        self.test_object.check_output_files()

    def test_output_expectations(self, test_folder):
        self._setup(test_folder)
        self.test_object.check_expectations()


if __name__ == "__main__":
    import os
    print(f"{__file__}")
    # pytest.main() #user_args=["-sv", os.path.abspath(__file__)])
    pytest.main(args=["-xv", os.path.abspath(__file__)])
