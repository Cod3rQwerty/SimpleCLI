# registry.py

import inspect

registry = {}

def infer_func_parameter_types(func):
    sig = inspect.signature(func)
    return {
        name: param.annotation
        for name, param in sig.parameters.items()
        if param.annotation is not inspect._empty
    }


def add(name, func, types: dict[str, type] | None = None, *, infer_types=False):
    if infer_types or types is None:
        inferred = infer_func_parameter_types(func)

        # only override if inference actually found something
        if inferred:
            types = inferred
        else:
            types = types if types is not None else {}

    registry[name] = (func, types)