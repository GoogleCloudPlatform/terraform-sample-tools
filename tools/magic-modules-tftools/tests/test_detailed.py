from bin import Erb2Tf, Tf2Erb, get_test_dirs
import pytest


@pytest.fixture(params=get_test_dirs(), scope="module")
def test_folder(request):
    return request.param


class TestTFTools:
    def _setup(self, test_folder):
        if "erb2tf" in test_folder:
            self.test_object = Erb2Tf()
        elif "tf2erb" in test_folder:
            self.test_object = Tf2Erb()
        else:
            assert False, "Input Error: Not able to determine Test Details"
        self.test_object.init_test_vars(test_folder)

    def test_input_files(self, test_folder):
        self._setup(test_folder)
        self.test_object.check_input_files()

    def test_run_tftools(self, test_folder):
        self._setup(test_folder)
        self.test_object.run_tftools()

    def test_output_file(self, test_folder):
        self._setup(test_folder)
        self.test_object.check_output_files()

    def test_output_expectations(self, test_folder):
        self._setup(test_folder)
        self.test_object.check_expectations()


if __name__ == "__main__":
    import os
    print(f"{__file__}")
    # pytest.main() #user_args=["-sv", os.path.abspath(__file__)])
    pytest.main(args=["-v", os.path.abspath(__file__)])
