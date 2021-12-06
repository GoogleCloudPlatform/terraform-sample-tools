To run test cases manually, simply do

For tests, download Terraform example file [terraform-sample-tools](https://github.com/GoogleCloudPlatform/terraform-sample-tools).

```bash
curl -o external_http_lb_mig_backend_custom_header.tf https://raw.githubusercontent.com/terraform-google-modules/terraform-docs-samples/master/external_http_lb_mig_backend_custom_header/main.tf 
```

Note: A file named `external_http_lb_mig_backend_custom_header.tf` is expected.

```bash
python tests.py
```
