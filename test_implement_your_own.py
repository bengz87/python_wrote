import pytest

from shlomobot_pytest.pretest import register_tests
from shlomobot_pytest.test_function_tests import check_test_function


from shlomobot_pytest.utils import (
    create_custom_error_json,
)

FILE_FUNCTION_MAP = {"implement_your_own.py": ["count", "is_in", "index", "insert"]}


# Pretest Functions
# ------------------------------------------------------------------------

register_tests(
    globals(),
    FILE_FUNCTION_MAP,
    test_expected_files_exist={},
    test_code_is_parsing={},
    test_expected_functions_exist={},
    test_contains_main_function={},
    test_name_eq_main_statement_exist={},
    test_main_function_is_last_function={},
    test_main_called_in_if_statement={},
    test_code_is_running={}
)

# Test Function Tests
# ------------------------------------------------------------------------
check_test_function(
    globals(),
    FILE_FUNCTION_MAP,
    dependency_map={
        "test_function_exists": ["test_name_eq_main_statement_exist",
                                 "test_code_is_running"]
    },
    test_function_exists={},
)

# Question-specific Test Functions
# ------------------------------------------------------------------------

@pytest.mark.dependency(
    name = "test__insert_func_tests",
    depends=["test_expected_functions_exist",
             "test_name_eq_main_statement_exist",
             "test_code_is_running"]
)

def test_insert_func_tests():
    """
    Testing for insert(obj, lst, index) Function
     - Checks if the function inserts a new obj into lst byt index correctly
    """

    from implement_your_own import insert

    custom_error_message_incorrect_list = create_custom_error_json(
        feedback="Your insert() function did return a correctly sorted new list",
        points_per_error=20,
        max_points_deducted=20,
        number_of_errors=1,
    )

    test_insert = insert('Dog', [0, 1, 1, 2, 2], 2)
    assert test_insert == [0, 1, 'Dog', 1, 2, 2], custom_error_message_incorrect_list
    # assert isinstance(test_insert, list), custom_error_message_not_list

@pytest.mark.parametrize(
    "test_obj, test_lst, result_count",
    [
            (1, [0, 1, 'Dog', 1, 2, 2], 2),
            ('Dog', [0, 1, 'Dog', 1, 2, 2], 1),
            ('Ket', [0, 1, 'Dog', 1, 2, 2], 0),
            (2, [0, 1, 'Dog', 1, 2, 2], 2),
            (22/7, [0, 1, 'Dog', 1, 2, 2], 0),
            (-1, [-1, "-1", '-1', 0-1, (-2)/2, 2, 9000 - 9001], 4),
            ("Nein!", [0, "Nein!", "Nein!", "Nein!", "Nein!", "Nein!", "Nein!", "Nein!", "Nein!", "Nein!", "Nine!"], 9),
    ],
)

def test_count_func_tests(test_obj, test_lst, result_count):
    """
    Testing for count(obj, lst) Function
     - Checks if the function counts correctly based on given object
    """

    from implement_your_own import count

    custom_error_message_no_count = create_custom_error_json(
        feedback="Your count() function did not count correctly",
        points_per_error=10,
        max_points_deducted=10,
        number_of_errors=1,
    )

    func_call = count(test_obj, test_lst)
    assert func_call == result_count, custom_error_message_no_count

@pytest.mark.parametrize(
    "test_obj, test_lst, result_is_in",
    [
            (1, [0, 1, 'Dog', 1, 2, 2], True),
            ('Dog', [0, 1, 'Dog', 1, 2, 2], True),
            ('Ket', [0, 1, 'Dog', 1, 2, 2], False),
            (2, [0, 1, 'Dog', 1, 2, 2], True),
            (22/7, [0, 1, 'Dog', 1, 2, 2], False),
            (-1, [-1, "-1", '-1', 0-1, (-2)/2, 2, 9000 - 9001], True),
            ("Nein!", [0, "Nein!", "Nein!", "Nein!", "Nein!", "Nein!", "Nein!", "Nein!", "Nein!", "Nein!", "Nine!"], True),
    ],
)

def test_is_in_func_tests(test_obj, test_lst, result_is_in):
    """
    Testing for is_in(obj, lst) Function
     - Checks if the function counts correctly based on given object
    """

    from implement_your_own import is_in

    custom_error_message_not_is_in = create_custom_error_json(
        feedback="Your is_in() function did not return the correct state for a test case",
        points_per_error=10,
        max_points_deducted=10,
        number_of_errors=1,
    )

    func_call = is_in(test_obj, test_lst)
    assert func_call == result_is_in, custom_error_message_not_is_in

@pytest.mark.parametrize(
    "test_obj, test_lst, result_index",
    [
            (1, [0, 1, 'Dog', 1, 2, 2], 1),
            ('Dog', [0, 1, 'Dog', 1, 2, 2], 2),
            ('Ket', [0, 1, 'Dog', 1, 2, 2], -1),
            (2, [0, 1, 'Dog', 1, 2, 2], 4),
            (22/7, [0, 1, 'Dog', 1, 2, 2], -1),
            (-1, [-1, "-1", '-1', 0-1, (-2)/2, 2, 9000 - 9001], 0),
            ("Nein!", [0, "Nein!", "Nein!", "Nein!", "Nein!", "Nein!", "Nein!", "Nein!", "Nein!", "Nein!", "Nine!"], 1),
    ],
)

def test_index_func_tests(test_obj, test_lst, result_index):
    """
    Testing for index(obj, lst) Function
     - Checks if the function returns the correct index based on the first occurrence
    """

    from implement_your_own import index

    custom_error_message_wrong_index = create_custom_error_json(
        feedback="Your index() function did not return the correct index a test case",
        points_per_error=10,
        max_points_deducted=10,
        number_of_errors=1,
    )

    func_call = index(test_obj, test_lst)
    assert func_call == result_index, custom_error_message_wrong_index
