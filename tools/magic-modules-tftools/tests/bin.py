# System tests for TFTOOLS
import os
import glob
import difflib
from abc import abstractmethod
import logging

LOGGER = logging.getLogger(__name__)

__version__ = "0.1.0"
print(f"Version {__file__}: {__version__}")


class Base:
    def __init__(self, test_folder, methodName="check_all"):
        print(f"[{test_folder}]> Setting Init Vars")
        self.init_test_vars(test_folder)
        super().__init__()
        self._test_folder = None

    @staticmethod
    def assert_equal(actual, expected, error_message):
        assert actual == expected, error_message

    @abstractmethod
    def init_test_vars(self, test_folder: str) -> None:
        pass

    @staticmethod
    def os_run(command):
        command = command + "> /dev/null"
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
        self.assert_equal(os.path.isfile(filename), True, error_message)

    @abstractmethod
    def _test_input_files(self):
        pass

    @abstractmethod
    def _test_output_file(self):
        pass

    @abstractmethod
    def _test_expectations(self):
        pass

    @abstractmethod
    def _test_run_tftools(self):
        pass

    def check_all(self):
        test_folder = self._test_folder
        LOGGER.info("eggs info")
        print(f"[{test_folder}]> Testing Input Files")
        self._test_input_files()
        print(f"[{test_folder}]> Test run TFTools")
        self._test_run_tftools()
        print(f"[{test_folder}]> Testing Output Files")
        self._test_output_file()
        print(f"[{test_folder}]> Testing Expectations")
        self._test_expectations()


class Tf2Erb(Base):
    # inputs
    input_tf_file = None
    input_cli_file = None
    # expectations
    expect_erb_file = None
    expect_yaml_file = None

    def init_test_vars(self, test_folder):
        self._test_folder = test_folder
        assert (
            "tf2erb" in test_folder
        ), "InputError: Expect `samples/*/erb2tf` type inputs"
        self.input_cli_file = f"{test_folder}/user_inputs"
        self.input_tf_file = glob.glob(f"{test_folder}/*.tf")[0]
        self.expect_erb_file = glob.glob(f"{test_folder}/*.erb")[0]
        self.expect_yaml_file = glob.glob(f"{test_folder}/*.yaml")[0]

    @property
    def output_erb_file(self):
        return self.input_tf_file + ".erb_check"

    @property
    def output_yaml_file(self):
        return os.path.join(os.path.dirname(self.input_tf_file), "terraform.yaml_check")

    def _test_input_files(self):
        self._file_check(self.input_tf_file)
        self._file_check(self.input_cli_file)
        self._file_check(self.expect_yaml_file)
        self._file_check(self.expect_erb_file)

    def _test_output_file(self):
        self._file_check(self.output_yaml_file, False)
        self._file_check(self.output_erb_file, False)

    def _test_expectations(self):
        file_diff, error_message = self.get_file_difference(
            self.expect_erb_file, self.output_erb_file
        )
        self.assert_equal(len(file_diff), 0, error_message)

        file_diff, error_message = self.get_file_difference(
            self.expect_yaml_file, self.output_yaml_file
        )
        self.assert_equal(
            len(file_diff), 0, "FileError: Output File not matching expectation"
        )

    def _test_run_tftools(self):
        """to check for execution failure in conversion of TF -> Erb & Yaml"""
        # run tftools
        run_command = "python3 ../tftools.py {} < {}".format(
            self.input_tf_file, self.input_cli_file
        )
        # check for execution status
        self.assert_equal(
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
        self._test_folder = test_folder
        assert (
            "erb2tf" in test_folder
        ), "InputError: Expect `samples/*/erb2tf` type inputs"
        self._test_folder = test_folder
        self.input_erb_file = glob.glob(f"{test_folder}/*.tf.erb")[0]
        self.input_yaml_file = glob.glob(f"{test_folder}/*.yaml")[0]
        self.expect_tf_file = glob.glob(f"{test_folder}/*.tf")[0]

    @property
    def output_tf_file(self):
        # ../../filename.tf.erb --> ../../filename.tf
        return os.path.join(
            os.path.dirname(self.input_erb_file),
            os.path.basename(self.input_erb_file).rstrip(".erb"),
        )

    def _test_input_files(self):
        self._file_check(self.input_erb_file)
        self._file_check(self.input_yaml_file)
        self._file_check(self.expect_tf_file)

    def _test_output_file(self):
        self._file_check(self.output_tf_file, False)

    def _test_expectations(self):
        file_diff, error_message = self.get_file_difference(
            self.expect_tf_file, self.output_tf_file
        )
        self.assert_equal(len(file_diff), 0, error_message)

    def _test_run_tftools(self):
        """to check for execution failure in conversion of Erb & Yaml -> TF"""
        # run tftools
        run_command = "python3 ../tftools.py {} {}".format(
            self.input_erb_file, self.input_yaml_file
        )
        self.assert_equal(
            self.os_run(run_command), 0, "Error: Failed to generate .tf files"
        )
