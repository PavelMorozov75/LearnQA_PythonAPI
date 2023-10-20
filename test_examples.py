class TestExample:
    def test_check_math(self):
        a = 5
        b = 9
        assert a + b == 14

    def test_check_math2(self):
        a = 5
        b = 9
        expected_sum = 17
        assert a + b == expected_sum, f"Sum of variables a and b is not equal {expected_sum}"

# python -m pytest test_examples.py -k test_check_math
