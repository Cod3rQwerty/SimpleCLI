from pprint import pprint


def cast_args(args: dict, types: dict[str, type]) -> dict:
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
                f"Could not cast argument '{key}' with value '{value}' to {caster.__name__}: {e}"
            )
    
    pprint(f"casted_args: {casted_args}")
    return casted_args