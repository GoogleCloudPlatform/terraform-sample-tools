import os
import unittest
import difflib


class Base(unittest.TestCase):
    @staticmethod
    def os_run(command):
        print(command)
        return os.system(command)

    @staticmethod
    def get_file_difference(file1, file2):
        print(f"Checking for files b/w {file1} & {file2}")
        diff = difflib.ndiff(file1.readlines().strip(), file2.readlines().strip())
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


class Tf2Erb(Base):
    # inputs
    input_tf_file = None
    input_cli_file = None
    # expectations
    expect_erb_file = None
    expect_yaml_file = None

    @property
    def output_erb_file(self):
        return self.input_tf_file + ".erb_check"

    @property
    def output_yaml_file(self):
        return os.path.join(os.path.dirname(self.input_tf_file), "terraform.yaml_check")

    def check_input_files(self):
        self._file_check(self.input_tf_file)
        self._file_check(self.input_cli_file)
        self._file_check(self.expect_yaml_file)
        self._file_check(self.expect_erb_file)

    def check_output_file(self):
        self._file_check(self.output_yaml_file, False)
        self._file_check(self.output_erb_file, False)

    def check_expectations(self):
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

    def run_tftools(self, tf_file, cli_inputs_file):
        """to check for execution failure in conversion of TF -> Erb & Yaml"""
        # run tftools
        run_command = "python3 ../tftools.py {} < {}".format(tf_file, cli_inputs_file)
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

    @property
    def output_tf_file(self):
        # ../../filename.tf.erb --> ../../filename.tf
        return os.path.join(
            os.path.dirname(self.input_erb_file),
            os.path.basename(self.input_erb_file).strip(".erb"),
        )

    def check_input_files(self):
        self._file_check(self.input_erb_file)
        self._file_check(self.input_yaml_file)
        self._file_check(self.expect_tf_file)

    def check_output_file(self):
        self._file_check(self.output_tf_file, False)

    def check_expectations(self):
        file_diff, error_message = self.get_file_difference(
            self.expect_tf_file, self.output_tf_file
        )
        self.assertEqual(len(file_diff), 0, error_message)

    def run_tftools(self, erb_file, yaml_file):
        """to check for execution failure in conversion of Erb & Yaml -> TF"""
        # run tftools
        run_command = "python3 ../tftools.py {} {}".format(erb_file, yaml_file)
        self.assertEqual(
            self.os_run(run_command), 0, "Error: Failed to generate .tf files"
        )
