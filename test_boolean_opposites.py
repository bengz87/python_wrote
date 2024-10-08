import pytest

from shlomobot_pytest.utils import (
    create_custom_error_json, check_pattern,
)

@pytest.fixture
def file_path(tmp_path):
    path = "boolean_opposites.txt"
    return path

PATTERN_NOT_KEYWORD = ["""(?:^|\s)not(?:\s|$)"""]
PATTERN_SOLUTION_1 = ["""(?i)a\s*<=\s*b"""]
PATTERN_SOLUTION_2 = ["""(?i)a\s*<\s*b"""]
PATTERN_SOLUTION_3 = ["""(?i)a\s*<\s*18\s+or\s+day\s*!=\s*3"""]
PATTERN_SOLUTION_4 = ["""(?i)a\s*<\s*18\s+and\s+day\s*==\s*3"""]


# Question-specific Test Functions
# ------------------------------------------------------------------------

def test_for_not(file_path):
    """
    Test to see if the 'not' keyword is within boolean_opposites.txt
    """
    custom_error_message_not_in_solution = create_custom_error_json(
        feedback="keyword 'Not' is detected in the .txt file.\n " +
                 "Please follow the exercise requirements.\n",
        points_per_error=100,
        max_points_deducted=100,
        number_of_errors=1,
    )

    assert not check_pattern(PATTERN_NOT_KEYWORD, file_path), custom_error_message_not_in_solution

def test_for_part_1(file_path):
    """
    Test to see if solution 1's regex is within boolean_opposites.txt
    """

    custom_error_message_no_pattern_1 = create_custom_error_json(
        feedback =  "Correct solution for 1 is not detected.\n" +
                    "The solution should look like: 'a [comparison operator(s)] b' (without the quotes) " +
                    "Do ensure you submitted the correct structure also.\n" +
                    "Example structure 1: 'a [!=] b' (without the quotes) \n " +
                    "Example structure 2: 'a [>] b' (without the quotes) \n",
        points_per_error=10,
        max_points_deducted=10,
        number_of_errors=1,
    )

    #regex is case-insensitive and does not check for start or end of a line.
    assert check_pattern(PATTERN_SOLUTION_1, file_path), custom_error_message_no_pattern_1

def test_for_part_2(file_path):
    """
    Test to see if solution 2's regex is within boolean_opposites.txt
    """

    custom_error_message_no_pattern_2 = create_custom_error_json(
        feedback =  "Correct solution for 2 is not detected.\n" +
                    "The solution should look like: 'a [comparison operator(s)] b' (without the quotes) " +
                    "Do ensure you submitted the correct structure also.\n" +
                    "Example structure 1: 'a [>] b' (without the quotes) \n " +
                    "Example structure 2: 'a [==] b' (without the quotes) \n",
        points_per_error=10,
        max_points_deducted=10,
        number_of_errors=1,
    )

    #regex is case-insensitive and does not check for start or end of a line.
    assert check_pattern(PATTERN_SOLUTION_2, file_path), custom_error_message_no_pattern_2

def test_for_part_3(file_path):
    """
    Test to see if solution 3's regex is within boolean_opposites.txt
    """

    custom_error_message_no_pattern_3 = create_custom_error_json(
        feedback =  "Correct solution for 3 is not detected.\n" +
                    "Hint: The solution should comprise of 'a [comparison operator(s)] 18 [logical operator(s)] day [comparison operator(s)] 3'\n" +
                    "Example structure: a [!=] 18 [AND/OR] day [<=] 3 \n " +
                    "There are many possibilities to try, good luck!",
        points_per_error=10,
        max_points_deducted=10,
        number_of_errors=1,
    )

    #regex is case-insensitive and does not check for start or end of a line.
    assert check_pattern(PATTERN_SOLUTION_3, file_path), custom_error_message_no_pattern_3

def test_for_part_4(file_path):
    """
    Test to see if solution 4's regex is within boolean_opposites.txt
    """

    custom_error_message_no_pattern_4 = create_custom_error_json(
        feedback =  "Correct solution for 4 is not detected.\n" +
                    "Hint: The solution should comprise of 'a [comparison operator(s)] 18 [logical operator] day [comparison operator(s)] 3'\n" +
                    "Example structure: a [==] 18 [AND/OR] day [>=] 3 \n " +
                    "There are many possibilities to try, good luck!",
        points_per_error=10,
        max_points_deducted=10,
        number_of_errors=1,
    )

    #regex is case-insensitive and does not check for start or end of a line.
    assert check_pattern(PATTERN_SOLUTION_4, file_path), custom_error_message_no_pattern_4
