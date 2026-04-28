registry = {}

def add(name, func, types: dict[str, type]):
    registry[name] = (func, types)