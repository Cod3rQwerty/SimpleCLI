# registry.py

import inspect

registry = {}


def infer_func_parameter_types(func):
    """
    Extract type annotations from a function signature.

    Example:
        def f(x: int, y: str): ...

        returns:
        {"x": int, "y": str}
    """

    sig = inspect.signature(func)

    return {
        name: param.annotation
        for name, param in sig.parameters.items()
        if param.annotation is not inspect._empty
    }


def add(name, func, types: dict[str, type] | None = None, *, infer_types=False):
    """
    Register a function in the CLI registry.

    Definition:
    - "registry" = mapping of command name → function + metadata

    Parameters:
        name: command string
        func: callable
        types: manual type mapping (optional)
        infer_types: use function annotations automatically

    Example:
        add("add", lambda x, y: x + y)

        → registry["add"] = (func, {"x": int, "y": int})
    """

    if infer_types or types is None:
        inferred = infer_func_parameter_types(func)

        if inferred:
            types = inferred
        else:
            types = types or {}

    registry[name] = (func, types)