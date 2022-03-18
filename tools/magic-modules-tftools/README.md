# Magic Modules - Terraform Automation Tools

The Magic Modules Terraform Automation Tools (`tftools`) are utilities written in Python3 for Terraform developers who want to develop and test Terraform snippets in [Magic Modules](https://github.com/GoogleCloudPlatform/magic-modules).

As input, the script takes a `filename.tf` and outputs `filename.tf.erb` plus `terraform.yaml` content. The tool lets you do the reverse as well.

> This repo is in development mode. To contribute to this repo, see the [contributing guidelines](CONTRIBUTING.md).

In [Magic Modules](https://github.com/GoogleCloudPlatform/magic-modules), every Terraform example (`filename.tf`) is represented by two files, as follows:

1. `filename.tf.erb`: A Ruby-based template file of `filename.tf`.
2. `terraform.yaml`: A Ruby configuration file.

The purpose of `tftools` is to automatically translate back and forth between the Terraform example (`filename.tf`) to the Magic Modules Ruby files (`filename.tf.erb` file and `terraform.yaml`). Without `tftools`, the translation must be done manually.


To summarize:

    ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                                                                                                            │
    │                                                                                                            │
    │                                                                                                            │
    │       ┌───────────────────┐                TFtools                       ┌───────────────────────────┐     │
    │       │  my_app_setup.tf  │ ─────────────────────────────┬───────────►   │  my_app_setup.tf.erb      │     │
    │       └───────────────────┘                              │               └───────────────────────────┘     │
    │                                                          │                                                 │
    │                                                          │               ┌───────────────────────────┐     │
    │      A standard terraform file                           └───────────►   │ terraform.yaml            │     │
    │                                                                          └───────────────────────────┘     │
    │                                                                                                            │
    │                                                                 Google's Magic Module terraform template   │
    │                                                                                                            │
    │                                                                           & yaml config files              │
    │                                                                                                            │
    └────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    
    ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                                                                                                            │
    │                                                                                                            │
    │                                                                                                            │
    │   ┌───────────────────────────┐             TFtools                       ┌───────────────────┐            │
    │   │  my_app_setup.tf.erb      │  ────────┬──────────────────────────────► │  my_app_setup.tf  │            │
    │   └───────────────────────────┘          │                                └───────────────────┘            │
    │                                          │                                                                 │
    │   ┌───────────────────────────┐          │                                                                 │
    │   │ terraform.yaml            │  ────────┘                               A standard terraform file         │
    │   └───────────────────────────┘                                                                            │
    │                                                                                                            │
    │    Google's Magic Module terraform template                                                                │
    │                                                                                                            │
    │              & yaml config files                                                                           │
    │                                                                                                            │
    └────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

Chart Credits: https://github.com/lewish/asciiflow

Note: The `_check` extension is added to prevent accidental overwrite of files that you might be working on in your output directory.

## About the installation

The installation includes the following command-line tools: `convert2tf`,  `convert2erb`, and `tftools`

- _convert2tf_: To convert a Magic Module terraform template (`filename.tf.erb`) files into a Terraform (`filename.tf`) file.
- _convert2erb_: To convert a Terraform file (`filename.tf`) into a Magic Module files (`filename.tf.erb_check` and `terraform.yaml_check`)
- _tftools_: A wrapper over `convert2tf` and `convert2erb`. Based on the input provided, this wrapper tool identifies which conversion tool to run.

## How to install

1. Clone this repo. Or, optionally, you can download the `.zip` file.

   ```bash
   git clone https://github.com/GoogleCloudPlatform/terraform-sample-tools.git
   ```

1. Move to the `setup.py` script location path and install.

   ```bash
   cd terraform-sample-tools/tools/magic-modules-tftools/
   sudo python3 setup.py install
   ```

1. Verify that `tftools` is installed.

   ```bash
   pip3 show tftools
   ```

1. Verify that `tftools` is in your user path.

   ```bash
   which tftools
   ```

1. After installation `tftools` might not be available in the command line. This might be caused by a `PATH` issue.

   To fix this issue, perform these steps:

   a. Run the following command and copy the output to your clipboard.
   
      ```bash
      python3 -c 'import sys; print(sys.prefix + "/bin")'
      ```
   b. Add the following to your `~/.bash_profile` file (create it, if it does not exist). Replace [PATH] with the output from the previous step.

      ```bash
      export PATH="[PATH]":$PATH.  
      ```
      
      For example:
      
      ```bash
      export PATH="/Library/Frameworks/Python.framework/Versions/3.7/bin/":$PATH
      ```
      
   c. Restart your terminal or iterm.
  
  Alternatively, for Macs, you can use the following procedure to update your path:
  
   a. Run the following command and copy the output to your clipboard.
 
      python3 -c 'import sys; print(sys.prefix + "/bin")'
     
   b. Open `/etc/paths`:
   
      sudo nano /etc/paths
      
   c. Paste the output from the previous step.


## How to use `tftools`

### Prepare your `filename.tf` file for conversion

1. Get or create a Terraform file (`filename.tf`).

2. Use a descriptive name for your Terraform file. The filename must be unique in the [Magic Modules template directory](https://github.com/GoogleCloudPlatform/magic-modules/tree/master/mmv1/templates/terraform/examples). So instead of `main.tf`, use the pattern `my-product-with-x-feature.tf`. For example: `int-https-lb-https-with-redirect.tf` for internal HTTPS load balancer with redirect.

3. In your Terraform file, within each resource, make sure that the `name` argument is the first argument. For example:

   ```
   resource "x" "default" {
     name               = "name"  # `name` argument is listed first in this resource
     ...
   }
   resource "y" "default" {
     name               = "name"  # `name` argument is listed first in this resource
     ...
   }
   ```
 
   This is required for the `convert2erb` parser to recognize a resource and generate a variable name for the `terraform.yaml` config. Otherwise, for that resource no config `terrarform.yaml` variable is created, and that resesource definition will be copied as-is to the `.tf.erb` template file.
   
4. In your Terraform file, after you are finished with local testing, remove any resources for generating unique resource names, such as `random_pet`. These resources are unnecessary because Magic Modules automatically generates unique names when testing resources that have the `vars` tag, as follows:

  ```
  resource "google_compute_backend_bucket" "static" {
    name        = "<%= ctx[:vars]['backend_bucket_name'] %>"
    bucket_name = google_storage_bucket.static.name
    enable_cdn  = true
  }
  ```
  
  Therefore, in your Terraform file, you can include something like the following, where the name of the bucket isn't globally unique:
  
  ```
  resource "google_compute_backend_bucket" "static" {
    name        = "backend-bucket-name"  # Generic, non-unique bucket name
    bucket_name = google_storage_bucket.static.name
    enable_cdn  = true
  }
  ```
  
  If your Terraform file includes a reference to `random_pet` in the `name` argument, `tftools` operation fails with a parsing error.

### Generate the Ruby files for Magic Modules

Now that you have prepared your `descriptive-and-unique-filename.tf` file, you can generate the Ruby template file (`filename.tf.erb`) and the `terraform.yaml` content:

1. From the command line, provide `descriptive-and-unique-filename.tf` as input to `tftools`:

   ```bash
   $ tftools descriptive-and-unique-filename.tf

   # (Alternative) This also works:
   $ convert2erb descriptive-and-unique-filename.tf
   ```
    
1. When prompted, select a resource to be the primary one. The primary resource should be the most important or canonical resource in the snippet.
  
    The following output files are generated from the location where the script is executed:

    * `descriptive-and-unique-filename.tf.erb_check`
    * `terraform.yaml_check`

1. After checking the output and confirming that you want to keep it, remove `_check` from `descriptive-and-unique-filename.tf.erb_check`.

   ```
   mv descriptive-and-unique-filename.tf.erb_check descriptive-and-unique-filename.tf.erb
   ```
   
   Note: At this point, you don't need to remove `_check` from `terraform.yaml_check`.

Now you can do a pull request to add your content to Magic Modules.

* Add `descriptive-and-unique-filename.tf.erb` to the [Magic Modules template directory](https://github.com/GoogleCloudPlatform/magic-modules/tree/master/mmv1/templates/terraform/examples).
* Add the content inside of your `terraform.yaml_check` to the correct `terraform.yaml`, depending on your product. For example, for Cloud Run, you would add your `terraform.yaml_check` content to the [Cloud Run `terraform.yaml` file](https://github.com/GoogleCloudPlatform/magic-modules/blob/master/mmv1/products/cloudrun/terraform.yaml).

For detailed instructions on creating a pull request for Magic Modules, see the [Include Terraform snippets](https://cloud.google.com/guides/authoring/terraform-snippets) page.

### Generate a new `.tf` file from the Ruby files

In your workflow, you might make some changes in your Ruby file and then need to retest in Terraform to make sure your example still works. Because you can't directly test a `tf.erb` file, you must generate a new `.tf` file.

1. Remove `_check` from `terraform.yaml_check`.

   ```
   mv terraform.yaml_check terraform.yaml
   ```
   
1. From command line, provide `.tf.erb` and `terraform.yaml` files as input for `tftools`. `tftools` calls `convert2tf` script to generate a Terraform `.tf` file.

   ```bash
   $ tftools      magic_module_terraform_example.tf.erb   magic_module_terraform.yaml

   # (Alternavitely) This also works
   $ convert2tf   magic_module_terraform_example.tf.erb   magic_module_terraform.yaml
   ```
  
  The script outputs an updated `.tf` file. In this example, `magic_module_terraform_example.tf`.

### How to uninstall

Use the standard `pip3` tool for uninstallation.

```bash
$ pip3 uninstall tftools
```
