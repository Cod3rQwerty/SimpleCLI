# casting.py

def cast_args(args: dict, types: dict[str, type]) -> dict:
    """
    Cast argument values to expected types.

    Definition:
    - "cast" means converting a value from one type to another
      (e.g. "123" → int(123))

    Parameters:
        args: dict of raw argument values (usually strings)
        types: dict mapping argument names → expected types

    Returns:
        dict: arguments converted to correct types

    Example:
        args = {"x": "10", "y": "3.5"}
        types = {"x": int, "y": float}

        returns:
        {"x": 10, "y": 3.5}

    If a type is missing from `types`, value is left unchanged.
    """

    casted_args = {}

    for key, value in args.items():
        caster = types.get(key)

        if caster is None:
            casted_args[key] = value
            continue

        try:
            casted_args[key] = caster(value)

        except Exception as e:
            raise ValueError(
                f"Could not cast argument '{key}' "
                f"({value}) to {caster.__name__}: {e}"
            )

    return casted_args