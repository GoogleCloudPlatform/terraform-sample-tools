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
Magic Modules Terraform Scripts testing(helper) tool!

Job of this script to convert .erb files to .tf files using values defined in .yaml files

__Note:__ Please use a proper file name for `.tf` files, as filename is used for generating `.yaml` file module section.

## How to use this script?

1. Download this script. Make this scrpt executeable & `pip3 install termcolor`
2. run shell command `./convert2tf.py <....tf.erb file>  <.....yaml file>`
3. Output .tf file is generated from the location where script is executed!
4. Output .tf file will have same name as .erb file (for test.tf.erb, output file is test.tf)

Example:
```
# from magic-modules directory
bash$ mkdir test; cd test

# download this script to here
# run - `chmod +x convert2tf.py`
# run - `pip3 install termcolor`. We use pkg this for erros highlighting in terminal!

# example - generating tf file for http external load balencer
bash$ ./convert2tf.py ../mmv1/templates/terraform/examples/external_http_lb_mig_backend_custom_header.tf.erb ../mmv1/products/compute/terraform.yaml
```
"""
import os
import sys
import re
import logging
from termcolor import colored

# logging settings
logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)


def show_warning(text):
    print(colored(color="red", text=str(text + "\n")))


def find_tf_section(vars_file, section_name):
    "To find the yaml related to section_name"
    flag = False
    kv_lines = []
    section_header = "!ruby/object:Provider::Terraform::Examples"
    for line in open(vars_file):
        if section_header in line:
            flag = False
        if flag:
            kv_lines.append(line.rstrip())
        if section_name in line:
            flag = True
    return kv_lines


def get_key_value_pairs(kv_lines):
    regex = r"^\s*(\w+):\s*\"([\w,-]+)\"$"
    my_dict = {}
    for line in kv_lines:
        # print(line)
        for pair in re.findall(regex, line):
            if len(pair) != 2:
                continue
            key, value = pair
            if key == "primary_resource_id":
                key = "<%= ctx[:primary_resource_id] %>"
            else:
                key = "<%= ctx[:vars]['{0}'] %>".format(key)
            my_dict[key] = value
    return my_dict


def convert_to_tf(tf_file_name, vars_file):
    tf_file = open(tf_file_name).read().strip()
    section_name = os.path.basename(tf_file_name).split(".")[0]
    vars_dict = get_key_value_pairs(find_tf_section(vars_file, section_name))
    # Vars usage validation
    print("##### Vars Validations")
    for k, v in vars_dict.items():
        ct = tf_file.count(k)
        prefix = "Found `{0}` ".format(k)
        suffix = "{0} times".format(ct)
        line = " " * (80 - len(prefix) - len(suffix))
        print(prefix + line + suffix)
        if ct == 0:
            show_warning(
                " - Warning! Found no usage for this defined var in .yaml file"
            )
        else:
            # if 'mig_name' in k:
            #     continue
            tf_file = tf_file.replace(k, v)
    # Check for any un-defined var
    missing_var_defs = []
    for line in tf_file.splitlines():
        if "<%= ctx[:vars][" in line:
            missing_var_defs.append(line)
    if missing_var_defs:
        show_warning(
            "\n - Warning! Found no var defined for following lines in .erb file"
        )
        show_warning("\n".join(missing_var_defs))
    # write TF
    out_file = "{0}.tf".format(section_name)
    with open(out_file, "w") as fp:
        fp.write(tf_file)
        print("\nOutputFile: {0}".format(out_file))


def parse_user_args(args):
    tf_file_name = None
    vars_file = None
    for each in args:
        if each.endswith(".tf.erb"):
            tf_file_name = each
        elif each.endswith(".yaml"):
            vars_file = each
    if not tf_file_name:
        show_warning("\nExpected a valid `.tf.erb` file as the first input arg")
        raise Exception("Missing command line input")
    if not vars_file:
        show_warning("\nExpected a valid `.yaml` file as the second input arg")
        raise Exception("Missing command line input")
    convert_to_tf(tf_file_name, vars_file)


def main():
    print("Args:", sys.argv)
    parse_user_args(sys.argv)


if __name__ == "__main__":
    main()
