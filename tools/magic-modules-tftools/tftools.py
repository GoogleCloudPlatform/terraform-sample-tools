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
Simple wrapper tool for convert2tf and convert2rb!
"""
import sys

from bin import convert2tf, convert2erb
from bin.util import show_title, show_heading

github_link = "https://github.com/GoogleCloudPlatform/terraform-sample-tools/tree/main/tools/magic-modules-tftools"


def main():
    show_heading("Running:" + " ".join(sys.argv))
    title_line = "\n" + "=" * 35 + " [tftools] " + "=" * 35
    show_title(title_line)
    if (".tf.erb" in " ".join(sys.argv)) and ".yaml" in " ".join(sys.argv):
        show_heading("Running - convert2tf")
        convert2tf.parse_user_args(sys.argv)
    elif ".tf" in " ".join(sys.argv):
        show_heading("Running - convert2erb")
        convert2erb.parse_user_args(sys.argv)
    else:
        print("Received no valid user inputs! Please check usage details @")
        show_heading(f"{github_link}\n")
    show_title(title_line)


if __name__ == "__main__":
    main()
