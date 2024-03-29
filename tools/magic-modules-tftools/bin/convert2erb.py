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
Tool `convert2rb` to convert terraform file into .erb template and yaml file!
"""
import os
import sys

from typing import List

from AntParser.app import main as ant_parser, ResourceRecord

from bin.template import generate_terraform_yaml
from bin.util import show_title, show_warning, timer_func

DEBUG = False


def cleanup_attribute_name(name):
    return name.replace("-", "_")


def dprint(text):
    if DEBUG:
        print(text.strip())


def show_resources_table(resource_records: List[ResourceRecord], heading=None):
    print("")
    if heading:
        show_title(heading)
    else:
        show_title("Terraform Resources Summary")

    # internal function
    def to_3c_table_row_format(word1, word2, word3):
        # Return a row with 3 columns structure
        word3 = word3 or ""
        line = " " * 15 + word2.center(80, " ")
        line = word1 + line[len(word1) : 100 - len(word3)] + word3
        return line

    print("--" * 55)
    print(
        " ID\t" + to_3c_table_row_format("ResourceType", "TFLocalName", "ResourceName")
    )

    for i, data_record in enumerate(resource_records):
        rtype, tfname, rname = (
            data_record.tf_type,
            data_record.tf_tfname,
            data_record.tf_name,
        )
        print(" %2d.\t" % (i + 1) + to_3c_table_row_format(rtype, tfname, rname))
    print("--" * 55)


@timer_func
def generate_erb_file(
    filename: str, resource_records: List[ResourceRecord], main_resource_id: int
):
    text_lines = open(filename).readlines()
    line_numbers = [record.tf_line_no - 1 for record in resource_records]

    def get_template_tf_var_name(name):
        return "<%= ctx[:vars]['{}'] %>".format(cleanup_attribute_name(name))

    def get_template_primary_resource_line(resource_type):
        return 'resource "' + resource_type + '" "<%= ctx[:primary_resource_id] %>" {'

    # update `resource` line
    ct = 0
    for i, ln in enumerate(line_numbers):
        record = resource_records[i]

        if i == main_resource_id:
            dprint(f"Current[{ln}]:\t" + text_lines[ln])
            text_lines[ln] = get_template_primary_resource_line(record.tf_type) + "\n"
            dprint(f"Updated[{ln}]:\t" + text_lines[ln])
            ct += 1

    # update `name` line
    for i, ln in enumerate(line_numbers):
        record = resource_records[i]

        # To update resource's name variable
        if record.tf_name_line and (record.tf_line_no != record.tf_name_line):
            ln = record.tf_name_line - 1
            dprint(f"Current[{ln}]:\t" + text_lines[ln])
            line = text_lines[ln].split("=")
            line[-1] = ' "{}"'.format(get_template_tf_var_name(record.tf_name))
            text_lines[ln] = "=".join(line) + "\n"
            dprint(f"Updated[{ln}]:\t" + text_lines[ln])

    out_file = os.path.basename(filename).split(".")[0] + ".tf.erb_check"
    out_file = os.path.join(os.path.dirname(filename), out_file)

    with open(out_file, "w") as fp:
        fp.write("".join(text_lines))
        print(" -> Output Written to {0}\n".format(out_file))
    return out_file


def terraform_file_quality_checks(resource_records: List[ResourceRecord]):
    _known_rname = set()
    print()
    for data_record in resource_records:
        # rtype, tfname, rname = (
        #     data_record.tf_type,
        #     data_record.tf_tfname,
        #     data_record.tf_name or "",
        # )
        rname = data_record.tf_name or ""
        if "_" in rname:
            show_warning(
                f"-> TFTools recommends using `-` instead of `_` for `{rname}`"
            )
        if rname and rname in _known_rname:
            show_warning(
                f"-> TFTools recommends using names for resources."
                f' Found using `name = "{rname}"` multiple times'
            )
        else:
            _known_rname.add(rname)

        tfname = data_record.tf_tfname
        if "-" in tfname:
            show_warning(
                f"-> TFTools recommends using `_` instead of `-` for `{tfname}`"
            )


def filter_out_nameless_resources(
    resource_records: List[ResourceRecord], display_filtered=True
):
    filtered_ids = []
    for i, rr in enumerate(resource_records):
        if not rr.tf_name:
            filtered_ids.append(i)
    if filtered_ids:
        show_resources_table(
            [rr for i, rr in enumerate(resource_records) if i in filtered_ids],
            heading="Filtering Resources without Name Attributes",
        )
    return [rr for i, rr in enumerate(resource_records) if i not in filtered_ids]


@timer_func
def get_primary_resource_id(resource_records, pm_id=None):
    if not resource_records:
        show_warning(
            "\nError: Found no resource with `name` attribute to be Primary Resource!"
        )
        return

    # show terraform resources summary
    show_resources_table(resource_records)

    # user input - primary resource id
    pm_resource_id = pm_id or input(
        "\nFrom the above table, enter a Primary Resource row ID: "
    )
    try:
        pm_resource_id = int(pm_resource_id) - 1
    except ValueError:
        show_warning("\nSkip executions! Due to invalid or missing UserInput")
        return
    is_valid_user_input = False
    if pm_id or (0 <= pm_resource_id < len(resource_records)):
        is_valid_user_input = True
        data_record = resource_records[pm_resource_id]
        rtype, tfname, rname = (
            data_record.tf_type,
            data_record.tf_tfname,
            data_record.tf_name or "",
        )
        print("\nResourceType\t: " + rtype)
        print("TFLocalName\t: " + tfname)
        print("ResourceName\t: " + rname)

    if is_valid_user_input and input("\nEnter `yes` to proceed: ") == "yes":
        return pm_resource_id

    show_warning("\nSkip executions! Due to invalid or missing UserInput")
    return


@timer_func
def validate_user_inputs(args):
    filename = ""
    for each in args:
        if each.endswith(".tf"):
            filename = each
    if not (os.path.isfile(filename) and filename.endswith(".tf")):
        text = "\nFileInputError: Expected a valid `.tf` file path as input"
        show_warning(text)
        raise Exception("Missing command line input")
    return filename


def main(user_args):
    filename = validate_user_inputs(user_args)
    print("Running - convert2erb - ANTLR4 Parser")
    resource_records = ant_parser(filename)
    print("Running - convert2erb - TF File checks")
    terraform_file_quality_checks(resource_records)
    resource_records = [rr for rr in resource_records if rr.tf_name] + [
        rr for rr in resource_records if not rr.tf_name
    ]
    # Use `filter_out_nameless_resources` to filter out namesless resources
    # resource_records = filter_out_nameless_resources(resource_records, display_filtered=True)
    pm_resource_id = get_primary_resource_id(resource_records)
    if pm_resource_id is not None:
        out_file = generate_terraform_yaml(filename, resource_records, pm_resource_id)
        if __name__ == "__main__":
            print("\n -> Output Written to {0}".format(out_file))
        out_file = generate_erb_file(filename, resource_records, pm_resource_id)
        if __name__ == "__main__":
            print("\n -> Output Written to {0}".format(out_file))


if __name__ == "__main__":
    args = sys.argv
    main(args)
    print("Args:", args)
