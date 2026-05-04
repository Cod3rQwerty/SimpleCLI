# registry.py
from __future__ import annotations

import inspect

class registry_entry:
    def __init__(self, name, func, types, print_result):
        self.name = name
        self.func = func
        self.types = types
        self.print_result = print_result

class registry_class:
    def __init__(self):
        self.entries: set[registry_entry] = set()

    def add(self, entry: registry_entry):
        self.entries.add(entry)

    def get(self, name: str) -> registry_entry:
        for entry in self.entries:
            if entry.name == name:
                return entry
        raise KeyError(f"Command '{name}' not found in registry.")

registry: registry_class = registry_class()

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


def add(name, func, types: dict[str, type] | None = None, *, infer_types=False, print_result=False):
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

    registry.entries.add(registry_entry(name, func, types, print_result))