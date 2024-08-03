import ast

from lint_plugins.ast_helpers import is_type_nullable, is_value_false, is_value_true


def parse_expr(expr_str: str):
    module = ast.parse(expr_str)
    assert isinstance(module, ast.Module)
    expr = module.body[0]
    assert isinstance(expr, ast.Expr)
    return expr.value


def test_is_type_nullable():
    assert not is_type_nullable(parse_expr("Mapped[DateTime]"))
    assert is_type_nullable(parse_expr("Optional[int]"))
    assert is_type_nullable(parse_expr("Union[int, None]"))
    assert not is_type_nullable(parse_expr("Union[int, str]"))
    assert is_type_nullable(parse_expr("None"))
    assert not is_type_nullable(parse_expr("int"))
    assert is_type_nullable(parse_expr("Optional[Union[int, None]]"))
    assert is_type_nullable(parse_expr("int | None"))
    assert not is_type_nullable(parse_expr("int | str"))


def test_is_value_false():
    assert is_value_false(parse_expr("False"))
    assert not is_value_false(parse_expr("True"))
    assert not is_value_false(parse_expr("None"))


def test_is_value_true():
    assert is_value_true(parse_expr("True"))
    assert not is_value_true(parse_expr("False"))
    assert not is_value_true(parse_expr("None"))
