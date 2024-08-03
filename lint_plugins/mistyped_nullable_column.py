import ast

from lint_plugins.ast_helpers import (
    get_func_keyword_arg,
    is_type_nullable,
    error_value,
    is_value_false,
    is_value_true,
)


class NullableColumnChecker:
    name = "flake8-mistyped_nullable_columns"
    version = "0.1.0"
    error_template = "LTP002 column type and nullable value must agree"

    def __init__(self, tree):
        self.tree = tree

    def run(self):
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.AnnAssign):
                continue
            if not node.simple:
                continue
            if not isinstance(node.annotation, ast.Subscript):
                continue
            if not isinstance(node.annotation.value, ast.Name):
                continue
            if node.annotation.value.id != "Mapped":
                continue
            sub_slice = node.annotation.slice
            value = node.value
            if not isinstance(value, ast.Call):
                continue
            if not isinstance(value.func, ast.Name):
                continue
            if value.func.id != "mapped_column":
                continue
            is_nullable = None
            nullable = get_func_keyword_arg(value, "nullable")
            if nullable is not None:
                if is_value_true(nullable):
                    is_nullable = True
                if is_value_false(nullable):
                    is_nullable = False
            func_args = value.args
            if func_args and isinstance(func_args[0], ast.Name) and func_args[0].id == "JSON":
                continue
            if is_type_nullable(sub_slice) and is_nullable is False:
                yield error_value(self, node)
            if not is_type_nullable(sub_slice) and is_nullable is True:
                yield error_value(self, node)
