#! /usr/local/bin/python3
"""
Magic Modules Terraform Scripts testing(helper) tool!

Job of this script to convert .erb files to .tf files using values defined in .yaml files


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


def show_warning(text):
    print(colored(color='red', text=str(text + '\n')))

def find_tf_section(vars_file, section_name):
    "To find the yaml related to section_name"
    flag = False
    kv_lines = []
    section_header = '!ruby/object:Provider::Terraform::Examples'
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
            if key == 'primary_resource_id':
                key = "<%= ctx[:primary_resource_id] %>"
            else:
                key = "<%= ctx[:vars]['{0}'] %>".format(key)
            my_dict[key] = value
    return my_dict


def main(tf_file_name, vars_file):
    tf_file = open(tf_file_name).read().strip()
    section_name = os.path.basename(tf_file_name).split('.')[0]
    vars_dict = get_key_value_pairs(find_tf_section(vars_file, section_name))
    # Vars usage validation
    print('##### Vars Validations')
    for k, v in vars_dict.items():
        ct = tf_file.count(k)
        prefix = 'Found `{0}` '.format(k)
        suffix = '{0} times'.format(ct)
        line = ' ' * (80 - len(prefix) - len(suffix))
        print(prefix + line + suffix)
        if ct == 0:
            show_warning(' - Warning! Found no usage for this defined var in .yaml file')
        else:
            # if 'mig_name' in k:
            #     continue
            tf_file = tf_file.replace(k, v)
    # Check for any un-defined var
    missing_var_defs = []
    for line in tf_file.splitlines():
        if '<%= ctx[:vars][' in line:
            missing_var_defs.append(line)
    if missing_var_defs:
        show_warning('\n - Warning! Found no var defined for following lines in .erb file')
        show_warning('\n'.join(missing_var_defs))
    # write TF
    out_file = '{0}.tf'.format(section_name)
    with open(out_file, 'w') as fp:
        fp.write(tf_file)
        print('\nOutputFile: {0}'.format(out_file))


if __name__ == '__main__':
    print('Args:', sys.argv)
    tf_file_name = sys.argv[1]
    if not tf_file_name.endswith('.tf.erb'):
        show_warning('Expected .tf.erb file as the first arg')
        raise Exception('Missing command line input')
    vars_file = sys.argv[2]
    if not vars_file.endswith('.yaml'):
        show_warning('Expected .yaml file as the second arg')
        raise Exception('Missing command line input')
    main(tf_file_name, vars_file)


