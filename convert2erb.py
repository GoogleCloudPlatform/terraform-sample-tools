#! /usr/local/bin/python3
"""
Magic Modules Terraform Scripts testing(helper) tool!

Job of this script to convert .tf into .erb & .yaml file.

## How to use this script?

1. Download this script. Make this scrpt executeable & `pip3 install termcolor`
2. run shell command `./convert2erb.py <....tf file>`
3. Output .erb file is generated from the location where script is executed!
4. Output .erb file will have same name as .tf file (for test.tf, output file is test.tf.erb)

Example:
```
# Download this script to required location
# run - `chmod +x convert2erb.py`
# run - `pip3 install termcolor`. We use pkg this for erros highlighting in terminal!

# example - generating .erb * .yaml
bash$ ./convert2erb.py external_http_lb_mig_backend_custom_header.tf
```
"""
import os
import sys
import re
import logging
from termcolor import colored, cprint


tf_lines = []
resource_lines = []
resource_name_lines = []
resource_regex_pattern = 'resource\s*"([\w, -]+)"\s*"([\w, -]+)"'
resource_name_regex_pattern = 'name\s*=\s*"([\w, -]+)"'
resource_types, resource_tfnames, resource_names = [], [], []

# yaml templates
template_header = """
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
""".strip(
    "\n"
)


def get_resource_names(text):
    try:
        name = re.findall(resource_name_regex_pattern, text)[0]
    except Exception as err:
        print(
            colored(
                "\n\tError: Failed to find name for the following line", color="red"
            )
        )
        print("\t\t[" + text + "]")
        raise Exception("Parsing Error!")
    return name


def collect_resource_details(text):
    try:
        rtype, tfname = re.findall(resource_regex_pattern, text)[0]
    except Exception as err:
        print(
            colored(
                "\n\tError: Failed to find name for the following line", color="red"
            )
        )
        print("\t\t[" + text + "]")
        raise Exception(err)
    return rtype, tfname


def ppline(word1, word2, word3):
    line = " " * 15 + word2.center(80, " ")
    line = word1 + line[len(word1) : 100 - len(word3)] + word3
    return line


def clean_up_var_name(name):
    return name.replace("-", "_")


def get_var_name(name):
    return "<%= ctx[:vars]['{}'] %>".format(clean_up_var_name(name))


def get_primary_resource_line(resource_type):
    return 'resource "' + resource_type + '" "<%= ctx[:primary_resource_id] %>" {'


def parse_file(filename):
    tf_lines = list(open(filename))
    flag = False
    flag2 = False
    # print('File Parsing,...')
    for line in tf_lines:
        line = line.strip()
        # identify resource tf line
        if line.startswith("resource "):
            # print('---' * 25)
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
            rtype, tfname = collect_resource_details(resource_lines[-1])
            rname = get_resource_names(resource_name_lines[-1])
            resource_types.append(rtype)
            resource_tfnames.append(tfname)
            resource_names.append(rname)
    # print('----' * 25)
    # print("parsing is compelted !!")


def generate_erb_file(filename, resource_id):
    erb_template = open(filename).read()
    for k in resource_names:
        erb_template = erb_template.replace(k, get_var_name(k))
    erb_template = erb_template.replace(
        resource_lines[resource_id],
        get_primary_resource_line(resource_types[resource_id]),
    )
    out_fname = os.path.basename(filename).split(".")[0] + ".tf.erb_check"
    with open(out_fname, "w") as fp:
        fp.write(erb_template)
        # print("Written to {0}".format(out_fname))
    return out_fname


def generate_teraform_yaml(resource_id):
    data = []
    data.append(
        template_header.format(
            os.path.basename(filename).split(".")[0], resource_tfnames[resource_id]
        )
    )
    for each in resource_names:
        data.append(template_vars_prefix.format(clean_up_var_name(each), each))
    data.append(template_footer)
    out_fname = "terraform.yaml_check"
    with open(out_fname, "w") as fp:
        fp.write("\n".join(data))
        # print("Written to {0}".format(out_fname))
    return out_fname


def main(filename):
    # parse file to collect resources details
    parse_file(filename)
    if not len(resource_types) == len(resource_tfnames) == len(resource_names):
        cprint("\nNoticed unexpected pattern! Plese check parsing logic!\n", 'red')
        raise Exception('Error: Failed to Parse file for details!')
    # show terraform resources summary
    cprint("\nTerraform Resources Summary", "blue", attrs=["bold"])
    print("--" * 55)
    print(" ID\t" + ppline("ResourceType", "TFLocalName", "ResourceName"))
    for i, (rtype, tfname, rname) in enumerate(
        zip(resource_types, resource_tfnames, resource_names)
    ):
        print(" %2d.\t" % (i + 1) + ppline(rtype, tfname, rname))
    print("--" * 55)
    #
    resource_id = input(
        "\nFrom above a table please check and provide Primary Resource row ID: "
    )
    resource_id = int(resource_id) - 1
    prepare_files = False
    if 0 <= resource_id < len(resource_types):
        prepare_files = True
        print("\nResourceType\t: " + rtype)
        print("TFLocalName\t: " + tfname)
        print("ResourceName\t: " + rname)

    if prepare_files and input("\nEnter `yes` to proceed: ") == "yes":
        cprint("Created files", "blue")
        # create .tf.erb
        print(" - {}".format(generate_erb_file(filename, resource_id)))
        # create .yaml file
        print(" - {}".format(generate_teraform_yaml(resource_id)))
    print("\n")

def parse_user_args(args):
    filename = ""
    for each in sys.argv:
        if each.endswith(".tf"):
            filename = each
    if not (os.path.isfile(filename) and filename.endswith(".tf")):
        raise Exception("FileInputError: Expected .tf as input")
    main(filename)

if __name__ == "__main__":
    print("Args:", sys.argv)
    parse_user_args(sys.argv)
