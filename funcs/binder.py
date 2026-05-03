# binder.py

def bind_args(pargs, kwargs, params):
    result = {}
    parg_index = 0

    for name, param in params.items():
        # positional or positional+keyword
        if param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):
            if parg_index < len(pargs):
                if name in kwargs:
                    raise TypeError(f"Multiple values for argument: {name}")
                result[name] = pargs[parg_index]
                parg_index += 1
            elif name in kwargs:
                result[name] = kwargs.pop(name)
            elif param.default is not param.empty:
                result[name] = param.default
            else:
                raise TypeError(f"Missing required argument: {name}")

        # keyword-only
        elif param.kind == param.KEYWORD_ONLY:
            if name in kwargs:
                result[name] = kwargs.pop(name)
            elif param.default is not param.empty:
                result[name] = param.default
            else:
                raise TypeError(f"Missing required keyword argument: {name}")

        # *args
        elif param.kind == param.VAR_POSITIONAL:
            result[name] = tuple(pargs[parg_index:])
            parg_index = len(pargs)

        # **kwargs
        elif param.kind == param.VAR_KEYWORD:
            result.update(kwargs)
            kwargs.clear()

    # leftover positional args
    if parg_index < len(pargs):
        raise TypeError("Too many positional arguments")

    # leftover kwargs
    if kwargs:
        unknown = ", ".join(kwargs.keys())
        raise TypeError(f"Unexpected keyword arguments: {unknown}")

    return result