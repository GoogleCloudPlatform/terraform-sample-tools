#! /usr/local/bin/python3
"""
Simple wrapper tool for convert2tf and convert2rb!
"""
import sys
from termcolor import cprint

import convert2erb
import convert2tf

def main():
    cprint('\====== TF Tools =======\n', 'blue')
    if '.erb.tf' in ' '.join(sys.argv):
        convert2tf.parse_user_args(sys.argv)
    elif '.tf' in ' '.join(sys.argv):
        convert2erb.parse_user_args(sys.argv)

if __name__ == '__main__':
    main()
