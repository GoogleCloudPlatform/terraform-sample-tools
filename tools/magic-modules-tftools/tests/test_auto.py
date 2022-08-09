import os
import glob
import pytest

from bin import Erb2Tf, Tf2Erb


def get_test_dirs():
    for each in glob.glob("samples/*/*"):
        if each.endswith("erb2tf") or each.endswith("tf2erb"):
            if "test_template" not in each:
                yield each


# https://docs.pytest.org/en/latest/how-to/fixtures.html#factories-as-fixtures
@pytest.fixture(scope="module", params=get_test_dirs())
def test_folder_name(request):
    return request.param


def test_automated_suite(test_folder_name):
    if test_folder_name.endswith("tf2erb"):
        test_object = Tf2Erb(test_folder_name)
        test_object.check_all()
    if test_folder_name.endswith("erb2tf"):
        test_object = Erb2Tf(test_folder_name)
        test_object.check_all()


if __name__ == "__main__":
    print(f"{__file__}")
    # pytest.main() #args=["-sv", os.path.abspath(__file__)])
    pytest.main(args=["-v", os.path.abspath(__file__)])
    # test_automated_suite('test1')
    # runner = unittest.TextTestRunner()  # failfast=True)
    # runner.run(automated_suite("test1"))
