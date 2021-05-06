from inspect import signature
from inspect import Parameter


def build_path(func, base_name: str = None, param_kinds: list = None) -> str:
    if not callable(func):
        raise TypeError(f'{func} is not a callable object.')
    if base_name is None:
        base_name = func.__name__
    if param_kinds is None:
        param_kinds = [Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY]

    path = base_name
    sig = signature(func)
    for param in sig.parameters.values():
        if (param.kind in param_kinds and
                param.default is param.empty):
            path = path + "/{{{0}}}".format(param.name)
    return path
