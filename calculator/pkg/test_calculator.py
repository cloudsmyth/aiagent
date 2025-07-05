from calculator import Calculator


def test_expression():
    calculator = Calculator()
    expression = "3 + 7 * 2"
    result = calculator.evaluate(expression)
    print(result)
    assert abs(result - 17) < 1e-9


test_expression()
