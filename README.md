# Magic Modules - Terraform Tools

Magic Modules Terraform utility tools is for Terraform developersn who want to develop/test terraform snippets in [Magic Modules](https://github.com/GoogleCloudPlatform/magic-modules).

For leveraging the automated test valiations in [Magic Modules](https://github.com/GoogleCloudPlatform/magic-modules), every terraform example(say `main.tf`) is written in two files

1. `.tf.erb` extension file: A ruby based template format file of `main.tf`.
2. `terraform.yaml` config file: A ruby config file to update values in `.tf.erb`.


Purpose of `tftools` is help developer to translate `.tf` file to `.tf.erb` & `.yaml` files or viceversa.

```
                             [file: main.tf] ---- [tftools] ----> [file: main.tf.erb] & [file: terraform.yaml]
[file: main.tf.erb] & [file: terraform.yaml] ---- [tftools] ----> [file: main.tf]
```

Available as a `tftools` command line utility tool, `tftools` is internally a wrapper over the following python modules(individually executable scripts).

- __Convert2tf__: To translate Magic Module terraform template(`.tf.erb`) files to terraform (`.tf`) file.

- __Convert2erb__: To convert a terraform file (`.tf`) into Magic Module terraform templates files (`.tf.erb` and `.yaml`)

    _Limitation: In terraform file, with in the resources, the `name` attribute is expected to defined as the first attribute. This is for the convert2erb.py parser to recognise a resource and generate a variable name for .yaml config. Otherwise, for that resource no config .yaml variable is created and that resesource definition will be as-is copied to .erb template file._

__Note:__ 

1. Please use a proper file name for `.tf` files, as filename is used for generating `.yaml` file module section
  
  > __Tip:__ Use a descriptive filename for your `.tf` file. For example, instead of `main.tf`,  use the pattern `my-product-with-x-feature.tf`. For example: `int_https_lb_https_with_redirect.tf` for internal https load balancer with redirect. This filename is used for generating the `name` attribute in the `terraform.yaml` example block.

2. For some safety concerns files generated will have a suffix `_check`.

### How to Install?

To clone this repo run the following. Optionally, once can download as a .zip as well.

```bash
git clone git@github.com:msampathkumar/MagicModules-TerraformTools.git
```

Move to `setup.py` script location and install

```bash
cd MagicModules-TerraformTools/
python setup.py install
```

Check, to see if `tftools` is installed

```bash
pip show tftools
```

Check, to see if `tftools` are in user path

```
which tfools
```

> In MacOS/Linux, at times even after installation `tftools` might not be available in you in command line. This could be due to `PATH` issue. Recommendation is check & add following to your `~/.bash_profile` file(create it, if it does not exits) and restart your terminal/iterm.

```
alias python=python3
alias pip=pip3
alias tf=terraform

# In your bash terminal run `python -c 'import sys; print(sys.prefix + "/bin")'`
#  to know you python library tools path & update below python path accordingly.
export PATH="/Library/Frameworks/Python.framework/Versions/3.6/bin":$PATH
```

### How to use?

From command line provide `.tf.erb` and `.yaml` files as input for `tftools`, then it calls `convert2tf` script to generate a terraform `.tf` file.

```bash
$ tftools     magic_module_terraform_example.tf.erb     magic_module_terraform.yaml
```

From commandline provide `.tf` as input to `tftools`, then it interall calls `convert2erb` script to the generate (`.erb.tf` and `.yaml`) files.

```bash
$ tftools    magic_module_terraform_example.tf
```

### How to uninstall?

```bash
$ pip3 uninstall tftools
```


## Contributions

Please see the [contributing guidelines](CONTRIBUTING.md)

## License

This library is licensed under Apache 2.0. Full license text is available in [LICENSE](LICENSE).
