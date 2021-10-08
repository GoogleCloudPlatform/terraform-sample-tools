import os
import time


import unittest
import logging
from shutil import copyfile

PATH = ""
sample_test_file = "external_http_lb_mig_backend_custom_header.tf"

# logging settings
logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)


def os_run(command):
    print(command)
    return os.system(command)


class TestTFtools(unittest.TestCase):
    def setUp(self) -> None:
        # check for input file
        self.assertEqual(
            os.path.isfile("external_http_lb_mig_backend_custom_header.tf"),
            True,
            "Error: Testfile is missing!",
        )
        self.sample_test_file = "external_http_lb_mig_backend_custom_header.tf"
        self.sample_backup_file = self.sample_test_file + "_backup"
        self.sample_test_output_erbfile = self.sample_test_file + ".erb"
        self.sample_test_output_yamlfile = "terraform.yaml"
        self.sample_test_tf_configfile = "user_inputs"
        copyfile(self.sample_test_file, self.sample_backup_file)
        return super().setUp()

    def test_convert2erb(self):
        # run tftools
        run_command = "../tftools.py {}  < {}".format(
            self.sample_test_file, self.sample_test_tf_configfile
        )
        self.assertEqual(
            os_run(run_command), 0, "Error: Failed to generate .tf.erb & .yaml files"
        )
        # check for output file
        self.assertEqual(
            os.path.isfile(self.sample_test_output_erbfile + "_check"),
            True,
            "Error: A outputfile(erb) is missing!",
        )
        self.assertEqual(
            os.path.isfile(self.sample_test_output_yamlfile + "_check"),
            True,
            "Error: A outputfile(yaml) is missing!",
        )

    def test_convert2tf(self):
        for file in [self.sample_test_output_erbfile, self.sample_test_output_yamlfile]:
            os.rename(os.path.abspath(file) + "_check", os.path.abspath(file))
        run_command = "../tftools.py {} {}".format(
            self.sample_test_output_erbfile, self.sample_test_output_yamlfile
        )
        self.assertEqual(os_run(run_command), 0, "Error: Failed to generate .tf files")

    def full_integration_test(self):
        import difflib

        # import pdb
        # pdb.set_trace()
        data1 = list(open(self.sample_test_file))
        data2 = list(open(self.sample_backup_file))
        delta = [line for line in data1 if line not in data2]
        self.assertEqual(len(delta), 0, "Error: Integration Test Failed! Please check")

    def tearDown(self) -> None:
        # self.clear_temp_files()
        return super().tearDown()

    def clear_temp_files(self):
        temp_files = [
            self.sample_test_output_erbfile,
            self.sample_test_output_erbfile + "_check",
            self.sample_test_output_yamlfile,
            self.sample_test_output_yamlfile + "_check",
            self.sample_backup_file,
        ]
        for file in temp_files:
            if os.path.isfile(file):
                os.remove(os.path.abspath(file))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestTFtools("test_convert2erb"))
    suite.addTest(TestTFtools("test_convert2tf"))
    suite.addTest(TestTFtools("full_integration_test"))
    suite.addTest(TestTFtools("clear_temp_files"))

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()  # failfast=True)
    runner.run(suite())
