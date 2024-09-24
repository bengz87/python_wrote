import pytest
import inspect
import ast

from shlomobot_pytest.pretest import register_tests
from shlomobot_pytest.test_function_tests import check_test_function

from shlomobot_pytest.utils import (
    create_custom_error_json,
)

FILE_FUNCTION_MAP = {"double_digits.py":[]}

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
    name="test_code_has_lambda_and_double_digits542",
    depends=["test_expected_functions_exist",
             "test_name_eq_main_statement_exist",
             "test_code_is_running"]
)

def test_code_has_lambda_and_double_digits542():
    """
    Check to see if there are any Lambda functions used in the code.
    Check if double_digits(542) has an argument of 542
    """
    import double_digits

    custom_error_message_no_lambda_functions = create_custom_error_json(
        feedback="No Lambda functions found in code.",
        points_per_error=100,
        max_points_deducted=100,
        number_of_errors=1,
    )

    custom_error_message_no_double_digits542 = create_custom_error_json(
        feedback =  "double_digits() should be passed the arguments of '542' and in the main() function.",
        points_per_error=50,
        max_points_deducted=50,
        number_of_errors=1,
    )

    class LambdaFinder(ast.NodeVisitor):
        def __init__(self):
            self.in_main = None
            self.lambda_functions = []
            self.calls_with_542 = []

        def visit_Lambda(self, node):
            self.lambda_functions.append(node)
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            # checking if we are entering the main function
            if node.name == 'main':
                self.in_main = True
            self.generic_visit(node)
            if node.name =='main':
                self.in_main = False

        def visit_Call(self, node):
            # double_digits func is assigned a lambda, so we need to check for Name instead of a lambda Node
            if isinstance(node.func, ast.Name) and node.func.id == 'double_digits':
                if self.in_main:
                    for arg in node.args:
                        if isinstance(arg, ast.Constant) and arg.value == 542:
                            self.calls_with_542.append(node)
                self.generic_visit(node)

    visitor = LambdaFinder()
    visitor.visit(ast.parse(inspect.getsource(double_digits)))

    assert len(visitor.lambda_functions) > 0, custom_error_message_no_lambda_functions
    assert len(visitor.calls_with_542) > 0, custom_error_message_no_double_digits542

def test_list_comprehension_not_used():
    """
    Check that the solution does not use list comprehension
    """
    import double_digits

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
    visitor.visit(ast.parse(inspect.getsource(double_digits)))

    assert not visitor.list_comprehension_exist, custom_error_message

def test_join_not_used():
    """
    Check that the solution does not use join
    """
    import double_digits

    custom_error_message = create_custom_error_json(
        feedback="You are not allowed to use 'join' in your code.",
        points_per_error=30,
        max_points_deducted=30,
        number_of_errors=1,
    )

    class JoinExistVisitor(ast.NodeVisitor):
        def __init__(self):
            self.join_exist = False

        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Str):
                if node.func.attr == 'join':
                    self.join_exist = True
            self.generic_visit(node)

    visitor = JoinExistVisitor()
    visitor.visit(ast.parse(inspect.getsource(double_digits)))

    assert not visitor.join_exist, custom_error_message


