# Magic Modules Terraform Tools

Magic Modules Terraform testing(helper) tools! Please check the details with in the scripts!

## Tool: Convert2tf

To convert Magic Module terraform template(`.tf.erb`) files to terraform (`.tf`) file.

## Tool: Convert2erb

To convert a terraform file (`.tf`) into Magic Module terraform templates files (`.tf.erb` and `.yaml`)

__Tip:__ Use a descriptive filename for your `.tf` file. The filename is used for generating
the `name` attribute in the `terraform.yaml` example block. For example, instead of naming your `.tf`
file `main.tf`, name it `my-product-with-x-feature.tf`. For example:
`int_https_lb_https_with_redirect.tf`.

## Contributions

Please see the [contributing guidelines](CONTRIBUTING.md)

## License

This library is licensed under Apache 2.0. Full license text is available in [LICENSE](LICENSE).
