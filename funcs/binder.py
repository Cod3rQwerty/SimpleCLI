# binder.py

def bind_args(pargs, kwargs, params):
    """
    Bind raw positional and keyword arguments to a function signature.

    Definition:
    - "bind" means matching incoming arguments (pargs/kwargs)
      to the function's formal parameters.

    - "function signature" refers to the parameters defined in the function's definition,
      which can be inspected using `inspect.signature(func).parameters`.

    This is similar to how Python internally maps:
        func(1, b=2) → a=1, b=2

    Parameters:
        pargs: list of positional arguments (from CLI input)
        kwargs: dict of keyword arguments (from CLI input)
        params: inspect.signature(func).parameters

    Returns:
        dict: {parameter_name: value}

    Example:
        pargs = ["10"]
        kwargs = {"b": "20"}

        params = (a, b)

        returns:
        {"a": "10", "b": "20"}

    Raises:
        TypeError: if arguments are missing, duplicated, or invalid
    """

    result = {}
    parg_index = 0

    for name, param in params.items():

        # positional-only or positional+keyword
        if param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):

            # take positional first
            if parg_index < len(pargs):
                if name in kwargs:
                    raise TypeError(f"Multiple values for argument: {name}")

                result[name] = pargs[parg_index]
                parg_index += 1

            # fallback to keyword
            elif name in kwargs:
                result[name] = kwargs.pop(name)

            # default value fallback
            elif param.default is not param.empty:
                result[name] = param.default

            else:
                raise TypeError(f"Missing required argument: {name}")

        # keyword-only arguments (*, a=1 style)
        elif param.kind == param.KEYWORD_ONLY:
            if name in kwargs:
                result[name] = kwargs.pop(name)
            elif param.default is not param.empty:
                result[name] = param.default
            else:
                raise TypeError(f"Missing required keyword argument: {name}")

        # *args (variadic positional arguments)
        elif param.kind == param.VAR_POSITIONAL:
            result[name] = tuple(pargs[parg_index:])
            parg_index = len(pargs)

        # **kwargs (variadic keyword arguments)
        elif param.kind == param.VAR_KEYWORD:
            result.update(kwargs)
            kwargs.clear()

    # leftover positional args = error
    if parg_index < len(pargs):
        raise TypeError("Too many positional arguments")

    # leftover kwargs = unknown parameters
    if kwargs:
        raise TypeError(f"Unexpected keyword arguments: {', '.join(kwargs.keys())}")

    return result