import pytest
import inspect
import ast

from shlomobot_pytest.pretest import register_tests
from shlomobot_pytest.test_function_tests import check_test_function

from shlomobot_pytest.utils import (
    create_custom_error_json,
)

FILE_FUNCTION_MAP = {"happy_birthday.py":["happy_birthday"]}

# Pretest Functions
# ------------------------------------------------------------------------

register_tests(
    globals(),
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
    name="test_for_happy_birthday",
    depends=["test_expected_functions_exist",
             "test_name_eq_main_statement_exist",
             "test_code_is_running"]
)

def test_for_happy_birthday_code_structure():
    """
    Check to see if there are any Lambda functions used in the happy_birthday function
    Checks if any testing functions calls happy_birthday()
    """
    import happy_birthday

    custom_error_message_no_lambda_functions = create_custom_error_json(
        feedback="No Lambda functions found in happy_birthday(name) function.",
        points_per_error=50,
        max_points_deducted=50,
        number_of_errors=1,
    )

    custom_error_message_no_happy_birthday_in_main = create_custom_error_json(
        feedback="Please use a main or test function to call the happy_birthday function and test your solution.",
        points_per_error=30,
        max_points_deducted=30,
        number_of_errors=1,
    )

    class LambdaFinder(ast.NodeVisitor):
        def __init__(self):
            self.lambda_functions = []
            self.happy_birthday_in_main = []

        def visit_Lambda(self, node):
            self.lambda_functions.append(node)
            self.generic_visit(node)

        def visit_Call(self, node):
            # happy_birthday func is assigned a lambda, so we need to check for Name instead of a lambda Node
            if isinstance(node.func, ast.Name) and node.func.id == 'happy_birthday':
                    self.happy_birthday_in_main.append(node)
            self.generic_visit(node)

    visitor = LambdaFinder()
    visitor.visit(ast.parse(inspect.getsource(happy_birthday)))

    assert len(visitor.lambda_functions) > 0, custom_error_message_no_lambda_functions
    assert len(visitor.happy_birthday_in_main) > 0, custom_error_message_no_happy_birthday_in_main

    visitor = LambdaFinder()
    visitor.visit(ast.parse(inspect.getsource(happy_birthday)))

    # all the assert checks for the conditions above
    assert len(visitor.lambda_functions) > 0, custom_error_message_no_lambda_functions
    assert len(visitor.happy_birthday_in_main) > 0, custom_error_message_no_happy_birthday_in_main

def test_for_happy_birthday_function_output():
    """
    Checks to see if happy_birthday func was defined or accessible as a module
    Checks if the return value prints out happy birthday 4 times
    Checks if the return value prints out the name in the 3rd line
    """

    from happy_birthday import happy_birthday

    test_name = "Sonic"
    birthday_salutations = happy_birthday(test_name)
    test_count_hbd = birthday_salutations.count('Happy Birthday')
    test_third_line = birthday_salutations.split('\n')[2]

    custom_error_message_happy_birthday_not_4x = create_custom_error_json(
        feedback =  f"Your output: {test_count_hbd}\n" +
                    "Expected output: 4 counts of 'Happy Birthday' \n" +
                    "The happy_birthday(name) function should print 'Happy Birthday' 4 times :).",
        points_per_error=20,
        max_points_deducted=20,
        number_of_errors=1,
    )

    custom_error_message_happy_birthday_does_not_include_name = create_custom_error_json(
        feedback =  "Your 3rd line: " + test_third_line + "\n"  +
                        "Expected output: 'Happy Birthday dear " + test_name + "\n"
                        "You should print out the happy birthday song with the name on the 3rd line. :)",
        points_per_error=10,
        max_points_deducted=10,
        number_of_errors=1,
    )

    assert test_count_hbd == 4, custom_error_message_happy_birthday_not_4x
    assert test_name.lower() in test_third_line.lower(), custom_error_message_happy_birthday_does_not_include_name

def test_list_comprehension_not_used():
    """
    Check that the solution does not use list comprehension
    """
    import happy_birthday

    custom_error_message = create_custom_error_json(
        feedback="You are not allowed to use list comprehension in your code.",
        points_per_error=30,
        max_points_deducted=30,
        number_of_errors=1,
    )

    class ListComprehensionExistVisitor(ast.NodeVisitor):
        def __init__(self):
            self.list_comprehension_exist = False

        def visit_ListComp(self, node):
            self.list_comprehension_exist = True
            self.generic_visit(node)

    visitor = ListComprehensionExistVisitor()
    visitor.visit(ast.parse(inspect.getsource(happy_birthday)))

    assert not visitor.list_comprehension_exist, custom_error_message
