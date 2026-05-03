# simplecli.py

import inspect
import sys

from funcs.binder import bind_args
from funcs.casting import cast_args
from funcs.parser import get_args, parse_args, PosAfterKwargError
from funcs.registry import registry


def run():
    """
    CLI entry point.

    Flow:
        1. Read command
        2. Parse CLI args
        3. Bind args → function signature
        4. Parse literals
        5. Cast to correct types
        6. Execute function

    Example usage:
        python app.py add 1 2

    Output:
        3
    """

    argv = sys.argv

    if len(argv) < 2:
        print("No command provided")
        return

    command = argv[1]

    if command not in registry:
        print(f"Unknown command: {command}")
        return

    args = argv[2:]

    try:
        pargs, kwargs = get_args(args)

        func, types = registry[command]

        params = inspect.signature(func).parameters

        # bind = match CLI args → function parameters
        combined_args = bind_args(pargs, kwargs, params)

        parsed_args = parse_args(combined_args)

        # cast = convert strings → correct Python types
        casted_args = cast_args(parsed_args, types)

    except (ValueError, TypeError, PosAfterKwargError) as e:
        print(f"Error: {e}")
        return

    print(func(**casted_args))