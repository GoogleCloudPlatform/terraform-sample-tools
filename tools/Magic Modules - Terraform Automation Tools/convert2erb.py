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

Job of this script to convert .tf into .erb & .yaml file.

## How to use this script?

1. Download this script.
2. Make this script executeable: `chmod +x convert2erb.py`.
3. Run `pip3 install termcolor`.
4. Run the script: `./convert2erb.py <filename>.tf`

   When prompted, select a resource to be the primary one.

   Note: In the Hashicorp Google provider reference documentation, the
   primary resource is the one that gets updated to include your
   new example.

## Output files

The following output files are generated from the location where script is
executed:

*  An .erb file that you can add to Magic Modules in mmv1/templates/terraform/examples.
   The output .erb file will have same name as the .tf file
   (for test.tf, output file is test.tf.erb).
*  A terraform.yaml_check file contains content that you can add to Magic Modules in
   mmv1/products/<your_product>/terraform.yaml.


Example:
```
# Download this script to required location
# run - `chmod +x convert2erb.py`
# run - `pip3 install termcolor`. We use pkg this for error highlighting in terminal!

# example - generating .erb * .yaml
bash$ ./convert2erb.py my_terraform_snippet.tf

Limitation:
    - It is expected all the `tf resources` have a `name` associated with them
    - It is expected all the tf resource attribute `name` is the first attribute defined
```
"""
import os
import sys
import re
import logging
from time import time
from termcolor import colored, cprint


# logging settings
logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)


def show_warning(text):
    print(colored(color="red", text=str(text + "\n")))


tf_lines = []
resource_lines = []
resource_name_lines = []
resource_regex_pattern = 'resource\s*"([\w, -]+)"\s*"([\w, -]+)"'
resource_name_regex_pattern = 'name\s*=\s*"([\w, -]+)"'
resource_types, resource_tfnames, resource_names = [], [], []

# yaml templates
template_header = """
      - !ruby/object:Provider::Terraform::Examples
        name: "{}"
        primary_resource_id: "{}"
        vars:
""".strip(
    "\n"
)
template_vars_prefix = """
          {}: "{}"
""".strip(
    "\n"
)
template_footer = """
        min_version: beta
        # ignore_read_extra:
        #   - "port_range"
        #   - "target"
        #   - "ip_address"
""".lstrip(
    "\n"
)


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        line = "---------------------[starting - {}]---------------------"
        logging.debug(line.format(func.__name__))
        result = func(*args, **kwargs)
        t2 = time()
        logging.info(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
        line = "---------------------[ending - {}]---------------------"
        return result

    return wrap_func


def get_resource_name(text):
    try:
        name = re.findall(resource_name_regex_pattern, text)[0]
    except Exception as err:
        print(
            colored(
                "\n\tError: Failed to find name for the following line", color="red"
            )
        )
        print("\t\t--->[" + text + "]<---")
        raise Exception("Parsing Error!")
    return name


def get_resource_rtype_and_tfname(text):
    try:
        rtype, tfname = re.findall(resource_regex_pattern, text)[0]
    except Exception as err:
        print(
            colored(
                "\n\tError: Failed to find name for the following line", color="red"
            )
        )
        print("\t\t--->[" + text + "]<---")
        raise Exception(err)
    return rtype, tfname


def to_table3c_row_format(word1, word2, word3):
    # Return a row with 3 columns structure
    line = " " * 15 + word2.center(80, " ")
    line = word1 + line[len(word1) : 100 - len(word3)] + word3
    return line


def cleanup_tfvar_name(name):
    return name.replace("-", "_")


def get_template_tfvar_name(name):
    return "<%= ctx[:vars]['{}'] %>".format(cleanup_tfvar_name(name))


def get_template_primary_resource_line(resource_type):
    return 'resource "' + resource_type + '" "<%= ctx[:primary_resource_id] %>" {'


@timer_func
def tf_resource_parser(filename):
    tf_lines = list(open(filename))
    flag = False
    flag2 = False
    # logging.debug('File Parsing,...')
    for line in tf_lines:
        line = line.strip()
        # identify resource tf line
        if line.startswith("resource "):
            resource_lines.append(line)
            flag = True
            # print('\t' + line)
        # identify resource name line
        if flag and line.startswith("name "):
            resource_name_lines.append(line)
            flag = False
            flag2 = True
            # print('\t' + line)
        # update records
        if flag2:
            flag2 = False
            rtype, tfname = get_resource_rtype_and_tfname(resource_lines[-1])
            rname = get_resource_name(resource_name_lines[-1])
            resource_types.append(rtype)
            resource_tfnames.append(tfname)
            resource_names.append(rname)
    # logging.debug("parsing is compelted !!")

    if not len(resource_types) == len(resource_tfnames) == len(resource_names):
        cprint("\nNoticed unexpected pattern! Please check the parsing logic!\n", "red")
        raise Exception("Error: Failed to Parse file for details!")


def show_tf_resources_table():
    cprint("Terraform Resources Summary", "blue", attrs=["bold"])
    print("--" * 55)
    print(
        " ID\t" + to_table3c_row_format("ResourceType", "TFLocalName", "ResourceName")
    )
    for i, (rtype, tfname, rname) in enumerate(
        zip(resource_types, resource_tfnames, resource_names)
    ):
        print(" %2d.\t" % (i + 1) + to_table3c_row_format(rtype, tfname, rname))
    print("--" * 55)


def replace_text_in_double_quotes(erb_template, astring, bstring):
    # To replace terraform resource names
    logging.debug(" - Repace [{}] with [{}]".format(astring, bstring))
    erb_template_len = len(erb_template)
    erb_template = erb_template.replace('"{}"'.format(astring), '"{}"'.format(bstring))
    if len(erb_template) == erb_template_len:
        logging.warning(
            "\nPlease check [{}] as text replacement did not work!!\n".format(astring)
        )
    return erb_template


def _generate_erb_file_primary_resource_replacement(erb_template, resource_id):
    # primary line
    rtype, tfname, rname = (
        resource_types[resource_id],
        resource_tfnames[resource_id],
        resource_names[resource_id],
    )
    tf_primary_resource_line = None
    for line in resource_lines:
        if rtype in line and tfname in line:
            tf_primary_resource_line = line
            break
    if not tf_primary_resource_line:
        raise Exception("Error: Failed to identify primary Line for replacement!")
    else:
        tf_primary_resource_new_line = get_template_primary_resource_line(
            resource_types[resource_id]
        )

    logging.debug(
        "Replace primary resource lines \n\t--->[{}]<----\n\t--->[{}]<----\n".format(
            tf_primary_resource_line, tf_primary_resource_new_line
        )
    )
    erb_template = erb_template.replace(
        tf_primary_resource_line, tf_primary_resource_new_line
    )
    return erb_template


def _generate_erb_file(filename, resource_id):
    erb_template = open(filename).read()
    # convert vars with vars template
    for k in resource_names:
        erb_template = replace_text_in_double_quotes(
            erb_template, k, get_template_tfvar_name(k)
        )
    # primary resource name replacement
    erb_template = _generate_erb_file_primary_resource_replacement(
        erb_template, resource_id
    )

    out_fname = os.path.basename(filename).split(".")[0] + ".tf.erb_check"
    with open(out_fname, "w") as fp:
        fp.write(erb_template)
        # print("Written to {0}".format(out_fname))
    return out_fname


def _generate_teraform_yaml(filename, resource_id):
    data = []
    data.append(
        template_header.format(
            os.path.basename(filename).split(".")[0], resource_tfnames[resource_id]
        )
    )
    for each in resource_names:
        data.append(template_vars_prefix.format(cleanup_tfvar_name(each), each))
    data.append(template_footer)
    out_fname = "terraform.yaml_check"
    with open(out_fname, "w") as fp:
        fp.write("\n".join(data))
        # print("Written to {0}".format(out_fname))
    return out_fname


@timer_func
def generate_erb_yaml_files(filename, pm_resource_id):
    cprint("\n(Re)Created Files", "blue", attrs=["bold"])
    # create .tf.erb
    print(" - {}".format(_generate_erb_file(filename, pm_resource_id)))
    # create .yaml file
    print(" - {}".format(_generate_teraform_yaml(filename, pm_resource_id)))


def convert_to_erb(filename):
    # parse file to collect resources details
    tf_resource_parser(filename)

    # show terraform resources summary
    show_tf_resources_table()

    # user input - primary resource id
    pm_resource_id = input(
        "\nFrom above a table please check and provide Primary Resource row ID: "
    )
    pm_resource_id = int(pm_resource_id) - 1
    is_valid_user_input = False
    if 0 <= pm_resource_id < len(resource_types):
        is_valid_user_input = True
        rtype, tfname, rname = (
            resource_types[pm_resource_id],
            resource_tfnames[pm_resource_id],
            resource_names[pm_resource_id],
        )
        print("\nResourceType\t: " + rtype)
        print("TFLocalName\t: " + tfname)
        print("ResourceName\t: " + rname)

    if is_valid_user_input and input("\nEnter `yes` to proceed: ") == "yes":
        generate_erb_yaml_files(filename, pm_resource_id)


def parse_user_args(args):
    filename = ""
    for each in sys.argv:
        if each.endswith(".tf"):
            filename = each
    if not (os.path.isfile(filename) and filename.endswith(".tf")):
        text = "\nFileInputError: Expected a valid `.tf` file path as input"
        show_warning(text)
        raise Exception("Missing command line input")
    convert_to_erb(filename)


def main():
    print("Args:", sys.argv)
    parse_user_args(sys.argv)


if __name__ == "__main__":
    main()
