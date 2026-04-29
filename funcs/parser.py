import ast

class PosAfterKwargError(Exception):
    pass

def get_args(args: list[str]) -> tuple[list, dict]:
    pargs = []
    kwargs = {}

    kwargs_reached = False
    skip_next = False

    for idx, arg in enumerate(args):

        if arg.startswith("--"):
            try:
                key = arg[2:]
                if key in kwargs:
                    raise ValueError(f"Duplicate argument: --{key}")
                
                kwargs[arg[2:]] = args[idx + 1]

            except IndexError:
                raise ValueError(f"Missing value for argument: {arg}")
            kwargs_reached = True
            skip_next = True
        else:
            if skip_next:
                skip_next = False
                continue

            if kwargs_reached:
                raise PosAfterKwargError("Positional arguments cannot come after keyword arguments")
            else:
                pargs.append(arg)

    return pargs, kwargs
    
def parse_args(args: dict) -> dict:
    parsed_args = {}
    for key, value in args.items():
        try:
            parsed_args[key] = ast.literal_eval(value)
        except Exception as e:
            raise ValueError(f"Could not parse argument '{key}' with value '{value}': {e}")
    return parsed_args