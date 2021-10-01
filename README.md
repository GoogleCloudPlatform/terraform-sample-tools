# Magic Modules Terraform Tools

Magic Modules Terraform utility tools for Terraform developers.

`tftools` is a command line utility tool, which is internally a wrapper over the following tools but not a replacement.

> For all simple single purpose tasks one can download only the required convert* scripts and check documentation within. It is not required to install this entire package!

## Tool: Convert2tf

To convert Magic Module terraform template(`.tf.erb`) files to terraform (`.tf`) file.

## Tool: Convert2erb

To convert a terraform file (`.tf`) into Magic Module terraform templates files (`.tf.erb` and `.yaml`)

__Note:__ 
1. Please use a proper file name for `.tf` files, as filename is used for generating `.yaml` file module section
2. For some safety concerns files generated will have a suffic `_check`.

# How to use?


## Installation

Downloading files

```bash
cd /tmp
git clone git@github.com:msampathkumar/MagicModules-TerraformTools.git
cd MagicModules-TerraformTools/
```

Install now

```bash
# Development of command line utility is in branch named `command_line_tool`
#   if you don't see setup.py in master branch, please do `git checkout command_line_tool`
python setup.py install
```

Checking your install

```bash
pip3 list | grep tftools
```

__Installation Check__

To check if tftools installed properly, run following command

```bash
which tfools
```

In MacOS - At times even after installation `tftools` might not be available in you in command line. This could be due to `PATH` issue. Recommendation is check & add following to your `~/.bash_profile` file(create it, if it does not exits) and restart your terminal/iterm.

```
alias python=python3
alias pip=pip3
alias tf=terraform

# Below line if for MacOS users, p
export PATH="/Library/Frameworks/Python.framework/Versions/3.6/bin/":$PATH
```

## Usage

As mentioned earlier, `tftools` is simple wrapper over `convert2erb` and `convert2tf` tools.


__How to generate .tf Code from .erb.tf & .yaml files?__

If you pass a `.tf.erb` and `.yaml` file as input variables, then it call `convert2tf` to do requried `.tf` file generation.

```

$ tftools magic_module_terraform_example.tf.erb magic_module_terraform.yaml

```

__How to generate .erb.tf & .yaml from tf file?__

If you pass `.tf` as input, then it cals `convert2erb` to the required (`.erb.tf` and `.yaml`) files generations.

```

$ tftools magic_module_terraform_example.tf

```

Usually files will be generated in location where command is executed!

## Uninstall

```
$ pip3 uninstall tftools
```

## Contributions

Please see the [contributing guidelines](CONTRIBUTING.md)

## License

This library is licensed under Apache 2.0. Full license text is available in [LICENSE](LICENSE).
