To run test cases manually, simply do

```bash
python tests.py
```


# Base Structure of Test Samples Folder

Test Case folder structure for `terraform-sample-tools/tools/magic-modules-tftools/tests/samples`
```commandline
|____samples
| |____<your_test_folder_name>
| | |____README.md
| | |____tf2erb
| | | |____<suitable_name>.tf       # 
| | | |____user_inputs              # User Input File
| | | |____expectation.tf           # User Input File
| | |____erb2tf
| | | |____expectation.tf.erb       # 
| | | |____terraform.yaml           # User Input File
| | | |____<suitable_name>.tf.erb   # User Input File
```
## To add a test case

Create a sample copy of test-cases
```commandline
cp -r tests/samples/test_template/ tests/samples/<<my_test_name>>/
```
## For Testcases: Terraform -> Erb Template

* To test case for converting Terraform file to ERB templates use `ttf2erb` folder.
* `tf2erb/`
