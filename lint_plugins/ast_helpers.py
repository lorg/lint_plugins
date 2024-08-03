import ast


def is_value_false(value):
    if isinstance(value, ast.Expr):
        return is_value_false(value.value)
    if isinstance(value, bool) and not value:
        return True
    if isinstance(value, ast.Constant):
        return value.value is False
    return False


def is_value_true(value):
    if isinstance(value, ast.Expr):
        return is_value_true(value.value)
    if isinstance(value, bool) and value:
        return True
    if isinstance(value, ast.Constant):
        return value.value is True
    return False


def is_type_nullable(node):
    if isinstance(node, ast.Name):
        if node.id == "Optional" or node.id == "Any":
            return True
    if isinstance(node, ast.Call):
        func = node.func
        if isinstance(func, ast.Name) and func.id == "Optional":
            return True
        if isinstance(func, ast.Name) and func.id == "Union":
            for arg in node.args:
                if is_type_nullable(arg):
                    return True
    if isinstance(node, ast.Expr):
        return is_type_nullable(node.value)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return is_type_nullable(node.left) or is_type_nullable(node.right)
    if isinstance(node, ast.Constant):
        return node.value is None
    if isinstance(node, ast.Subscript):
        if isinstance(node.value, ast.Name) and node.value.id == "Optional":
            return True
        if isinstance(node.value, ast.Name) and node.value.id == "Union":
            if isinstance(node.slice, ast.Tuple):
                for slice_value in node.slice.elts:
                    if is_type_nullable(slice_value):
                        return True
        return is_type_nullable(node.value)
    return False


def error_value(checker, node):
    return (node.lineno, node.col_offset, checker.error_template, type(checker))


def get_func_keyword_arg(func: ast.Call, arg_name: str):
    for keyword in func.keywords:
        if keyword.arg == arg_name:
            return keyword.value
    return None
