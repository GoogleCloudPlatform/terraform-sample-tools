#! /usr/local/bin/python3
"""
Simple wrapper tool for convert2tf and convert2rb!
"""
import sys
from termcolor import cprint

import convert2erb
import convert2tf


def main():
    cprint(
        "\n================================ [tftools] ================================\n",
        "blue", attrs=["bold"]
    )
    if ".erb.tf" in " ".join(sys.argv):
        convert2tf.parse_user_args(sys.argv)
    elif ".tf" in " ".join(sys.argv):
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
