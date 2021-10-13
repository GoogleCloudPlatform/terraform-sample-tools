# Magic Modules - Terraform Tools

__TL;DR__: Magic Modules Terraform utility tools is for Terraform developers who want to develop/test terraform snippets in Magic Modules.

In [Magic Modules](https://github.com/GoogleCloudPlatform/magic-modules), every terraform example(say `main.tf`) is written in two files

1. `main.tf.erb` extension file: A ruby based template file of `main.tf`.
2. `terraform.yaml` config file: A ruby config file for the above template file.

Purpose of this tool is help developers to translate `.tf` file to `.tf.erb` & `.yaml` files or viceversa. This eliminates the necessity of manually writting ruby template and ruby config files.

```
                       [Inputs: main.tf] ---- [tftools] ----> [Output: main.tf.erb  &  terraform.yaml]
[Inputs: main.tf.erb  &  terraform.yaml] ---- [tftools] ----> [Output: main.tf]
```


## UserTools

On installation, `tftools`, `convert2tf` & `convert2erb` command line tools are available to user.

- _convert2tf_: To translate Magic Module terraform template(`.tf.erb`) files to terraform (`.tf`) file.
- _convert2erb_: To convert a terraform file (`.tf`) into Magic Module terraform templates files (`.tf.erb` and `.yaml`)
- _tftools_: Simple wrapper over `convert2tf` & `convert2erb`. Based on input provided, identifies which tools to run.

_Note:_

1. For safety concern, output files(.erb & .yaml) will have a suffix `_check`.
1. For Terraform samples pull requests to Magic Modules, use a descriptive filename for your `.tf` files. As filename is used for generating the `name` attribute in the `.yaml` file block.
    - For example, instead of `main.tf`,  use the pattern `my-product-with-x-feature.tf`.
    - For example: `int_https_lb_https_with_redirect.tf` for internal https load balancer with redirect.
1. _convert2erb_ Limitation: In terraform file, with in the resources, the `name` attribute is expected to defined as the first attribute. This is for the convert2erb parser to recognise a resource and generate a variable name for .yaml config. Otherwise, for that resource no config .yaml variable is created and that resesource definition will be as-is copied to .erb template file._

### How to Install?

- Step1: Clone this repo or optionally, one can download as a .zip as well.

  ```bash
  git clone git@github.com:msampathkumar/MagicModules-TerraformTools.git
  ```

- Step2: Move to `setup.py` script location path and install

  ```bash
  cd MagicModules-TerraformTools/
  python3 setup.py install
  ```

- Step3: Check, to see if `tftools` is installed

  ```bash
  pip show tftools
  ```

- Step4: Check, to see if `tftools` are in user path

  ```bash
  which tfools
  ```
  If you dont see `tftools` location from above step, proceed to Step5 to resolve your path issue.

- Step5: (Optional) In Mac/Linux, even after installation `tftools` might not be available in you in command line. This could be due to `PATH` issue. Recommendation is check & add following to your `~/.bash_profile` file(create it, if it does not exits) and restart your terminal/iterm.

  ```bash
  alias python=python3
  alias pip=pip3
  alias tf=terraform

  # In your bash terminal run `python3 -c 'import sys; print(sys.prefix + "/bin")'`
  #  to know your python library tools path & update below python path accordingly.
  export PATH="/Library/Frameworks/Python.framework/Versions/3.6/bin":$PATH
  ```

### How to use?

- To generating terraform file: From command line provide `.tf.erb` and `.yaml` files as input for `tftools`, then it calls `convert2tf` script to generate a terraform `.tf` file.

  ```bash
  $ tftools      magic_module_terraform_example.tf.erb   magic_module_terraform.yaml

  # (Alternavitely) This also works
  $ convert2tf   magic_module_terraform_example.tf.erb   magic_module_terraform.yaml
  ```

- To generating ruby template file: From commandline provide `.tf` as input to `tftools`, then it interall calls `convert2erb` script to the generate (`.erb.tf` and `.yaml`) files.

  ```bash
  $ tftools       magic_module_terraform_example.tf

  # (Alternavite) This also works
  $ convert2erb   magic_module_terraform_example.tf
  ```

### How to uninstall?

```bash
$ pip3 uninstall tftools
```


## Contributions

Please see the [contributing guidelines](CONTRIBUTING.md)

## License

This library is licensed under Apache 2.0. Full license text is available in [LICENSE](LICENSE).
