# Magic Modules Terraform Tools

Magic Modules Terraform testing(helper) tools! Please check the details with in the scripts!

## Tool: Tftools

`tftools` is a command line tool, which is internally acts as a wrapper over the following tools.

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
# We are developing command in a branch named `command_line_tool`
#   if you don't see setup.py in master branch, please do `git checkout command_line_tool`
python setup.py install
```

Checking your install

```bash
pip3 list | grep tftools
```

## Installation Check

`tftools` is designed to install as a command line utility, just like `pip3` or `autopepy` or `terraform`. To check run following command

```bash
which tfools
```

## Usage

`tftools` is small wrapper over `convert2erb` and `convert2tf` tools.

If you pass `.tf.erb` and `.yaml` file as inputs, then it call `convert2tf` to do requried `.tf` file generation.

```bash
tftools some_file_name.tf.erb terraform_file.yaml 
```

If you pass `.tf` as input, then it cals `convert2erb` to the required (`.erb.tf` and `.yaml`) files generations.

```bash
tftools some_file_name.tf
```

Usually files will be generated in location where command is executed!

## Uninstall

```bash
pip3 uninstall tftools
```

## Contributions

Please see the [contributing guidelines](CONTRIBUTING.md)

## License

This library is licensed under Apache 2.0. Full license text is available in [LICENSE](LICENSE).
