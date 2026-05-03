import inspect
import sys

from funcs.binder import bind_args
from funcs.casting import cast_args
from funcs.parser import get_args, parse_args, PosAfterKwargError
from funcs.registry import registry

from funcs.registry import add

def run():
    argv = sys.argv

    if len(argv) < 2:
        print("No command provided")
        return

    command = argv[1]

    if command not in registry.keys():
        print(f"Unknown command: {command}")
        return

    args = argv[2:]

    try:
        pargs, kwargs = get_args(args)

        func, types = registry[command]

        params = inspect.signature(func).parameters
        combined_args = bind_args(pargs, kwargs, params)

        parsed_args = parse_args(combined_args)
        casted_args = cast_args(parsed_args, types)

    except (ValueError, TypeError, PosAfterKwargError) as e:
        print(f"Error: {e}")
        return
    
    print(func(**casted_args))
