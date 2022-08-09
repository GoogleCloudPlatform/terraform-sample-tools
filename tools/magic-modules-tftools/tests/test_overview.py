import os
import pytest

from bin import Erb2Tf, Tf2Erb, get_test_dirs


# https://docs.pytest.org/en/latest/how-to/fixtures.html#factories-as-fixtures
@pytest.fixture(scope="module", params=get_test_dirs())
def test_folder_name(request):
    return request.param


def test_automated_suite(test_folder_name):
    test_object = None
    if test_folder_name.endswith("tf2erb"):
        test_object = Tf2Erb()
    elif test_folder_name.endswith("erb2tf"):
        test_object = Erb2Tf()
    else:
        raise Exception(f"InputError: {test_folder_name} is not as expected!")
    test_object.init_test_vars(test_folder_name)
    test_object.check_all()


if __name__ == "__main__":
    print(f"{__file__}")
    # pytest.main() #args=["-sv", os.path.abspath(__file__)])
    pytest.main(args=["-v", os.path.abspath(__file__)])
    # test_automated_suite('test1')
    # runner = unittest.TextTestRunner()  # failfast=True)
    # runner.run(automated_suite("test1"))
