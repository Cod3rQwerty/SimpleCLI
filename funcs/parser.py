# parser.py

import ast


class PosAfterKwargError(Exception):
    """
    Raised when positional arguments appear after keyword arguments.

    Example (invalid):
        cmd 1 2 --x 3 4
    """

class FlagBeforeArgsError(Exception):
    """
    Raised when flags appear before positional arguments.

    Example (invalid):
        cmd --flag 1 2
    """


def get_args(args: list[str]) -> tuple[list, dict, set]:
    """
    Parse raw CLI tokens into positional and keyword arguments.

    Rules:
    - Positional args must come before keyword args
    - Keyword args are in format: --key value

    Returns:
        (pargs, kwargs, flags)

    Example:
        input:
            ["1", "2", "--x", "10", "--flag"]

        output:
            (["1", "2"], {"x": "10"}, {"flag"})
    """

    pargs = []
    kwargs = {}
    flags = set()

    flags_reached = False
    kwargs_reached = False
    skip_next = False

    for idx, arg in enumerate(args):

        if arg.startswith("--"):
            if idx + 1 == len(args) or args[idx + 1].startswith("--"): # is a flag
                flags_reached = True
                flags.add(arg[2:])
            else: # is a keyword argument
                if flags_reached:
                    raise FlagBeforeArgsError(
                        "Flags cannot come before keyword arguments"
                    )

                key = arg[2:]

                if key in kwargs:
                    raise ValueError(f"Duplicate argument: --{key}")

                try:
                    kwargs[key] = args[idx + 1]
                except IndexError:
                    raise ValueError(f"Missing value for argument: {arg}")

                kwargs_reached = True
                skip_next = True

        else:
            if skip_next:
                skip_next = False
                continue

            if kwargs_reached:
                raise PosAfterKwargError(
                    "Positional arguments cannot come after keyword arguments"
                )
            
            if flags_reached:
                raise FlagBeforeArgsError(
                    "Positional arguments cannot come before flags"
                    )

            pargs.append(arg)

    return pargs, kwargs, flags


def parse_args(args: dict) -> dict:
    """
    Convert string arguments into Python literals where possible with ast.literal_eval.

    Example:
        {"x": "123", "y": "[1,2,3]"}

        → {"x": 123, "y": [1,2,3]}

    If parsing fails, value is kept as raw string.
    """

    parsed_args = {}

    for key, value in args.items():
        try:
            parsed_args[key] = ast.literal_eval(value)
        except Exception:
            parsed_args[key] = value

    return parsed_args