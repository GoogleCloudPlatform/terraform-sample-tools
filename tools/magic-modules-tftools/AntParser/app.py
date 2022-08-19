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
import os.path
import sys
sys.path.insert(0, os.path.dirname(__file__))

from dataclasses import dataclass
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker

from lang.terraformLexer import terraformLexer
from lang.terraformParser import terraformParser
from lang.terraformListener import terraformListener

# from lang.terraformVisitor import terraformVisitor


@dataclass
class ResourceRecord:
    tf_type: str
    tf_tfname: str
    tf_name: str = ""
    tf_line_no: int = 0
    tf_name_line: int = 0


class CustomListener(terraformListener):
    """
    Listener for collecting Terraform resource information

    Reference: https://github.com/jszheng/py3antlr4book/blob/master/03-Array/test_array.py
    """

    # TODO(msampathkumar): Listener are easy bt they tend to parser every grammar
    #   for better efficient use 'visitor'
    # https://github.com/jszheng/py3antlr4book/blob/master/04-Calc/MyVisitor.py
    # https://stackoverflow.com/questions/20714492/antlr4-listeners-and-visitors-which-to-implement#

    def __init__(self, *args, **kwargs):
        super(CustomListener, self).__init__(*args, **kwargs)
        self._line_number = None
        self._resource_name_line_number = None
        self._resource_name_value = None
        self._resource_type = None
        self._resource_tf_name = None
        self._resources_data = []
        self._is_in_resource = False
        self._init_custom_data_vars()

    def _init_custom_data_vars(self):
        self._is_in_resource = True  # for checking if walker entered a resource
        self._resource_type = None  # for `resource`
        self._resource_tf_name = None  # for `resource's terraform name`
        self._resource_name_value = None  # for `resource's name`
        self._line_number = None  # for `resource` line
        self._resource_name_line_number = None  # for `resource's name` line

    def getcustomResourceData(self):
        return self._resources_data

    # Enter a parse tree produced by terraformParser#resource.
    def enterResource(self, ctx: terraformParser.ResourceContext):
        self._is_in_resource = True
        # print('hi resource')
        # self._line_number = ctx.name().start.line
        self._line_number = ctx.start.line

    # Exit a parse tree produced by terraformParser#resource.
    def exitResource(self, ctx: terraformParser.ResourceContext):
        tf_record = ResourceRecord(
            self._resource_type,
            self._resource_tf_name,
            self._resource_name_value,
            self._line_number,
            self._resource_name_line_number,
        )
        self._resources_data.append(tf_record)
        self._init_custom_data_vars()
        # print(tf_record)

    # Enter a parse tree produced by terraformParser#name.
    def enterName(self, ctx: terraformParser.NameContext):
        if self._is_in_resource:
            self._resource_tf_name = ctx.getText().strip("'").strip('"')

    # Enter a parse tree produced by terraformParser#resourcetype.
    def enterResourcetype(self, ctx: terraformParser.ResourcetypeContext):
        if self._is_in_resource:
            self._resource_type = ctx.getText().strip("'").strip('"')

    # Enter a parse tree produced by terraformParser#argument.
    def enterArgument(self, ctx: terraformParser.ArgumentContext):
        if self._is_in_resource and not self._resource_name_value:
            text = ctx.getText()
            if text.startswith("name="):
                self._resource_name_value = text[5:].strip("'").strip('"')
                self._resource_name_line_number = ctx.start.line


def main(filename, cli_run=False):
    input_data_stream = FileStream(filename)
    lexer = terraformLexer(input_data_stream)
    tokenstream = CommonTokenStream(lexer)
    parser = terraformParser(tokenstream)

    parser.reset()
    tree = parser.file_()

    walker = ParseTreeWalker()
    listener = CustomListener()
    walker.walk(listener, tree)
    if cli_run:
        text = "ANTLR Parser".center(50).replace("  ", "==")
        print("")
        print(text)
        for each in listener.getcustomResourceData():
            print("--> " + str(each))
        print("=" * 50)
        print("")
    return listener.getcustomResourceData()


if __name__ == "__main__":
    cli_arguments = sys.argv
    tf_filename = sys.argv[-1]
    if tf_filename.endswith(".tf") and os.path.isfile(tf_filename):
        main(tf_filename, cli_run=True)
    else:
        print("Error: Expecting a valid .tf file")
