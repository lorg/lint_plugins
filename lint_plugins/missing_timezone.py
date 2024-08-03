import ast

from lint_plugins.ast_helpers import error_value, is_value_false


class TimezoneChecker:
    name = "flake8-timezone-checker"
    version = "0.1.0"
    error_template = "LTP001 timezone=True must be set for DateTime columns"

    def __init__(self, tree):
        self.tree = tree

    def run(self):
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name):
                continue
            if node.func.id != "mapped_column":
                continue
            args = node.args
            if not args:
                continue
            column_type = args[0]
            if isinstance(column_type, ast.Name):
                if column_type.id == "DateTime":
                    yield error_value(self, node)
            elif isinstance(column_type, ast.Call):
                if not isinstance(column_type.func, ast.Name):
                    continue
                if column_type.func.id == "DateTime":
                    if column_type.args:
                        timezone_arg = column_type.args[0]
                        if is_value_false(timezone_arg):
                            yield error_value(self, node)
                    elif column_type.keywords:
                        for keyword in column_type.keywords:
                            if keyword.arg == "timezone":
                                if is_value_false(keyword.value):
                                    yield error_value(self, node)
                    else:
                        yield error_value(self, node)
