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
from termcolor import cprint

import convert2erb
import convert2tf


def main():
    print(" ".join(sys.argv))
    cprint(
        "\n================================ [tftools] ================================\n",
        "blue", attrs=["bold"]
    )
    if (".tf.erb" in " ".join(sys.argv)) and ".yaml" in " ".join(sys.argv):
        cprint('\nRunning - convert2tf\n', 'cyan')
        convert2tf.parse_user_args(sys.argv)
    elif ".tf" in " ".join(sys.argv):
        cprint('\nRunning - convert2erb\n', 'cyan')
        convert2erb.parse_user_args(sys.argv)
    else:
        print("Received no valid user inputs! Please check usage details @")
        cprint(
            "\n\thttps://github.com/msampathkumar/MagicModules-TerraformTools/tree/command_line_tool#usage\n",
            "cyan",
        )
    cprint(
        "\n================================ [tftools] ================================\n",
        "blue", attrs=["bold"]
    )


if __name__ == "__main__":
    main()
