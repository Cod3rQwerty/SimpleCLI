# simplecli.py

import inspect
import sys

from funcs.binder import bind_args
from funcs.casting import cast_args
from funcs.parser import get_args, parse_args, PosAfterKwargError
from funcs.registry import registry

from funcs.registry import add  # unused, but allows users to import `add` directly from `simplecli`

EARLY_EXIT_FLAGS = {"help", "h", "?"}

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
        pargs, kwargs, flags = get_args(args)

        early_exit_flags_used = EARLY_EXIT_FLAGS.intersection(flags)

        if early_exit_flags_used:
            for flag in early_exit_flags_used:
                if flag in {"help", "h", "?"}:
                    print(f"Help for command '{command}':")
                    print(registry[command][0].__doc__)
                    return

        func, types = registry[command]

        params = inspect.signature(func).parameters

        # bind = match CLI args → function parameters
        combined_args = bind_args(pargs, kwargs, flags, params)

        parsed_args = parse_args(combined_args)

        # cast = convert strings → correct Python types
        casted_args = cast_args(parsed_args, types)

    except (ValueError, TypeError, PosAfterKwargError) as e:
        print(f"Error: {e}")
        return

    print(func(**casted_args))