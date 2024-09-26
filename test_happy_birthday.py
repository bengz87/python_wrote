import pytest
import inspect
import ast

from shlomobot_pytest.pretest import register_tests
from shlomobot_pytest.test_function_tests import check_test_function

from shlomobot_pytest.utils import (
    create_custom_error_json,
)

FILE_FUNCTION_MAP = {"happy_birthday.py":["happy_birthday(name)"]}

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
    Checks if main() has a happy_birthday()
    Checks if main() uses assert
    Checks if happy_birthday() has a "name" parameter taken in
    It is possible that the trainee's solution does not include map/range due to this range of checks in autograder
    """
    import happy_birthday

    custom_error_message_no_lambda_functions = create_custom_error_json(
        feedback="No Lambda functions found in happy_birthday(name).",
        points_per_error=50,
        max_points_deducted=50,
        number_of_errors=1,
    )

    custom_error_message_no_happy_birthday_in_main = create_custom_error_json(
        feedback="Please include at least 1 happy_birthday function call in the main function.",
        points_per_error=50,
        max_points_deducted=50,
        number_of_errors=1,
    )

    custom_error_message_no_assert_in_main = create_custom_error_json(
        feedback="Do use the 'assert' keyword in your tests in the main function",
        points_per_error=20,
        max_points_deducted=20,
        number_of_errors=1,
    )
    custom_error_message_happy_birthday_has_name_parameter = create_custom_error_json(
        feedback="Your happy_birthday function should have a 'name' parameter taken in.",
        points_per_error=30,
        max_points_deducted=30,
        number_of_errors=1,
    )

    class LambdaFinder(ast.NodeVisitor):
        def __init__(self):
            self.in_main = None
            self.has_lambda = False
            self.happy_birthday_in_main = []
            self.assert_in_main = False
            self.in_happy_birthday = None
            self.has_name_parameter = False

        def visit_FunctionDef(self, node):
            # checking if we are entering the main function
            if node.name == 'main':
                self.in_main = True
            self.generic_visit(node)
            if node.name == 'main':
                self.in_main = False
            # checking if we are entering the happy_birthday function
            if node.name == 'happy_birthday':
                for param in node.args.args:
                    # checking if happy_birthday function takes in a parameter named "name"
                    if param.arg == "name":
                        self.has_name_parameter = True
                        break
                self.in_happy_birthday = True
            self.generic_visit(node)
            if node.name == 'happy_birthday':
                self.in_happy_birthday = False

        def visit_Call(self, node):
            # happy_birthday func is assigned a lambda, so we need to check for Name
            # instead of a lambda Node during calling
            if isinstance(node.func, ast.Name) and node.func.id == 'happy_birthday':
                if self.in_main:
                    self.happy_birthday_in_main.append(node)
                self.generic_visit(node)

        # if lambda was visited within a map function, it will also count
        # and set flag to True
        def visit_Lambda(self, node):
            self.has_lambda = True
            self.generic_visit(node)

        def visit_Assert(self, node):
            # if an assert was visited, set flag to True
            if self.in_main:
                self.assert_in_main = True
            self.generic_visit(node)

    visitor = LambdaFinder()
    visitor.visit(ast.parse(inspect.getsource(happy_birthday)))

    # all the assert checks for the conditions above
    assert visitor.has_lambda == True, custom_error_message_no_lambda_functions
    assert len(visitor.happy_birthday_in_main) > 0, custom_error_message_no_happy_birthday_in_main
    assert visitor.assert_in_main == True, custom_error_message_no_assert_in_main
    assert visitor.has_name_parameter == True, custom_error_message_happy_birthday_has_name_parameter

def test_for_happy_birthday_function_output():
    """
    Check if the return value prints out happy birthday 4 times
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

    assert birthday_salutations.count("Happy Birthday") == 4, custom_error_message_happy_birthday_not_4x
    assert test_name in test_third_line, custom_error_message_happy_birthday_does_not_include_name


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
