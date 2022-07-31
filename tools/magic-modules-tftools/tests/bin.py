import glob
import os
import unittest
import difflib
from abc import abstractmethod

__version__ = "0.1.0"
print(f'Version {__file__}: {__version__}')


class Base(unittest.TestCase):

    @abstractmethod
    def init_test_vars(self, test_folder):
        pass

    @staticmethod
    def os_run(command):
        print(command)
        return os.system(command)

    @staticmethod
    def get_file_difference(file1, file2):
        print(f"Checking for files b/w {file1} & {file2}")

        def get_data(file_name):
            return open(file_name).read().strip().splitlines()
        diff = difflib.ndiff(get_data(file1), get_data(file2))
        changes = [l for l in diff if l.startswith("+ ") or l.startswith("- ")]
        for each in changes:
            print(each)
        error_message = (
            f"FileError: Output file{file1} not matching Expectation file{file2}"
        )
        return changes, error_message

    def _file_check(self, filename, is_input_file=True):
        if is_input_file:
            error_message = f"FileError: InputFile{filename} Not Found!"
        else:
            error_message = f"FileError: OutputFile{filename} Not Found!"
        self.assertEqual(os.path.isfile(filename), True, error_message)

    @abstractmethod
    def test_input_files(self):
        pass

    @abstractmethod
    def test_output_file(self):
        pass

    @abstractmethod
    def test_expectations(self):
        pass

    @abstractmethod
    def test_run_tftools(self):
        pass

    def check_all(self):
        self.test_input_files()
        self.test_run_tftools()
        self.test_output_file()
        self.test_expectations()


class Tf2Erb(Base):
    # inputs
    input_tf_file = None
    input_cli_file = None
    # expectations
    expect_erb_file = None
    expect_yaml_file = None

    def init_test_vars(self, test_folder):
        self.test_folder = test_folder
        self.input_cli_file = f'samples/{self.test_folder}/tf2erb/user_inputs'
        self.input_tf_file = glob.glob(f'samples/{self.test_folder}/tf2erb/*.tf')[0]
        self.expect_erb_file = glob.glob(f'samples/{self.test_folder}/tf2erb/*.erb')[0]
        self.expect_yaml_file = glob.glob(f'samples/{self.test_folder}/tf2erb/*.yaml')[0]

    @property
    def output_erb_file(self):
        return self.input_tf_file + ".erb_check"

    @property
    def output_yaml_file(self):
        return os.path.join(os.path.dirname(self.input_tf_file), "terraform.yaml_check")

    def test_input_files(self):
        self._file_check(self.input_tf_file)
        self._file_check(self.input_cli_file)
        self._file_check(self.expect_yaml_file)
        self._file_check(self.expect_erb_file)

    def test_output_file(self):
        self._file_check(self.output_yaml_file, False)
        self._file_check(self.output_erb_file, False)

    def test_expectations(self):
        file_diff, error_message = self.get_file_difference(
            self.expect_erb_file, self.output_erb_file
        )
        self.assertEqual(len(file_diff), 0, error_message)

        file_diff, error_message = self.get_file_difference(
            self.expect_yaml_file, self.output_yaml_file
        )
        self.assertEqual(
            len(file_diff), 0, "FileError: Output File not matching expectation"
        )

    def test_run_tftools(self):
        """to check for execution failure in conversion of TF -> Erb & Yaml"""
        # run tftools
        run_command = "python3 ../tftools.py {} < {}".format(self.input_tf_file, self.input_cli_file)
        # check for execution status
        self.assertEqual(
            self.os_run(run_command),
            0,
            "Error: Failed to generate .tf.erb & .yaml files",
        )


class Erb2Tf(Base):
    # inputs
    input_erb_file = None
    input_yaml_file = None
    # expectations
    expect_tf_file = None

    def init_test_vars(self, test_folder):
        self.test_folder = test_folder
        self.input_erb_file = glob.glob(f'samples/{test_folder}/erb2tf/*.tf.erb')[0]
        self.input_yaml_file = glob.glob(f'samples/{test_folder}/erb2tf/*.yaml')[0]
        self.expect_tf_file = glob.glob(f'samples/{test_folder}/erb2tf/*.tf')[0]

    @property
    def output_tf_file(self):
        # ../../filename.tf.erb --> ../../filename.tf
        return os.path.join(
            os.path.dirname(self.input_erb_file),
            os.path.basename(self.input_erb_file).strip(".erb"),
        )

    def test_input_files(self):
        self._file_check(self.input_erb_file)
        self._file_check(self.input_yaml_file)
        self._file_check(self.expect_tf_file)

    def test_output_file(self):
        self._file_check(self.output_tf_file, False)

    def test_expectations(self):
        file_diff, error_message = self.get_file_difference(
            self.expect_tf_file, self.output_tf_file
        )
        self.assertEqual(len(file_diff), 0, error_message)

    def test_run_tftools(self):
        """to check for execution failure in conversion of Erb & Yaml -> TF"""
        # run tftools
        run_command = "python3 ../tftools.py {} {}".format(self.input_erb_file, self.input_yaml_file)
        self.assertEqual(
            self.os_run(run_command), 0, "Error: Failed to generate .tf files"
        )


def automated_suite(test_folder_name):
    suite = unittest.TestSuite()
    suite.addTest(Tf2Erb("test_convert2erb"))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()  # failfast=True)
    runner.run(suite())
