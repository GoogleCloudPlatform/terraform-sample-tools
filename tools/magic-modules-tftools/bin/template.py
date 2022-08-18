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
import os

HEADER = """
      - !ruby/object:Provider::Terraform::Examples
        name: "{}"
        primary_resource_type: "{}"
        primary_resource_id: "{}"
        vars:
""".strip(
    "\n"
)

VARS_PREFIX = """
          {}: "{}"
""".strip(
    "\n"
)

FOOTER = """
        skip_docs: true  # Change to false if you want to add sample to https://registry.terraform.io/providers/hashicorp/google/latest/docs
        min_version: beta
        # ignore_read_extra:
        #   - "port_range"
        #   - "target"
        #   - "ip_address"
""".lstrip(
    "\n"
)

YAML_FILE = "terraform.yaml_check"


def cleanup_tf_name(name):
    return name.replace("-", "_")


def generate_terraform_yaml(filename, resource_records, main_resource_id):
    data = []
    record = resource_records[main_resource_id]
    # HEADER, primary resource
    temp = HEADER.format(
        os.path.basename(filename).split(".")[0],
        record.tf_type,
        cleanup_tf_name(record.tf_name),
    )
    data.append(temp)
    # vars
    for resource_record in resource_records:
        var_name = resource_record.tf_name
        data.append(VARS_PREFIX.format(cleanup_tf_name(var_name), var_name))
    # FOOTER
    data.append(FOOTER)
    # print("\n".join(data))
    # save to file
    out_file = os.path.join(os.path.dirname(filename), YAML_FILE)
    with open(out_file, "w") as fp:
        fp.write("\n".join(data))
    print("\n -> Output Written to {0}".format(out_file))
    return out_file
