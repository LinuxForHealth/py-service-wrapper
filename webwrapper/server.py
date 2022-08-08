import os
import importlib
from inspect import signature
from types import ModuleType
from typing import Callable, Dict, List, Tuple

import uvicorn
from fastapi import FastAPI, Header

from .utils import yaml_parser
from .utils import path_builder


_DEFAULT_MODULE_NAME = "_default"


def fix_function_signature_for_headers(func, headers):
    sig = signature(func)
    dp = dict(sig.parameters)
    for header_param in headers:
        orig_param = sig.parameters[header_param]
        default = orig_param.default
        if default == orig_param.empty:
            default = None
        new_param = sig.parameters[header_param].replace(default=Header(default))
        del dp[header_param]
        dp[header_param] = new_param

    sig = sig.replace(parameters=tuple(dp.values()))
    func.__signature__ = sig


def _load_target_modules(modules_def: Dict[str, str]) -> Dict[str, ModuleType]:
    """
    Given a dictionary of module name and paths, load the modules into another dict where the keys are
    the module names and the values are the actual modules

    :param: modules_def: dictionary of module name and module paths
    """
    modules = {}
    for module_name, module_path in modules_def.items():
        if module_name in modules:
            raise ValueError(f"Cannot define more then one module with the same name ({module_name})")

        modules[module_name] = importlib.import_module(module_path)
    return modules


def _parse_function_references(module_dict: Dict[str, ModuleType], function_ref: str) -> Callable:
    if '.' not in function_ref:
        module = _DEFAULT_MODULE_NAME
        function = function_ref
        implicit_default = True
    else:
        module, function = function_ref.split('.', 1)
        implicit_default = False
        
    if module in module_dict:
        return getattr(module_dict[module], function)
    else:
        if implicit_default:
            raise ValueError(f"No default module defined. Cannot have function reference with implicit module: {function_ref}")
        else:
            raise ValueError(f"Undefined module {module} referenced in {function_ref}")


def _setup_framework(project_config):

    # Py service wrapper deployments need to define the following
    # environment variable if a port other than the default is needed.
    _port = int(os.getenv("PY_SERVICE_WRAPPER_PORT", default="5000"))

    routes = project_config["project"]["entrypoints"]
    modules_def = project_config["project"]["modules"]

    app_modules = _load_target_modules(modules_def)

    start_funcs = None
    shutdown_funcs = None
    startup = "startup"
    shutdown = "shutdown"
    if startup in project_config["project"]:
        startups = project_config["project"][startup]
        start_funcs = [_parse_function_references(app_modules, sp) for sp in startups]

    if shutdown in project_config["project"]:
        shutdowns = project_config["project"][shutdown]
        shutdown_funcs = [_parse_function_references(app_modules, sn) for sn in shutdowns]

    app = FastAPI(
        title=project_config["project"]["name"],
        on_startup=start_funcs,
        on_shutdown=shutdown_funcs,
    )

    for route in routes:
        path = route.get("path", None)
        name = route.get("name", None)
        headers = route.get("headers", None)
        methods = route.get("methods", ["GET"])
        entrypoint = route.get("entrypoint", None)
        if entrypoint is None:
            raise ValueError("entrypoint in the entrypoints cannot be None")
        if name is None:
            name = entrypoint

        func = _parse_function_references(app_modules, entrypoint)

        if headers is not None:
            fix_function_signature_for_headers(func, headers)

        if path is None:
            if "GET" in methods:
                path = path_builder.build_path(func, name)
            else:
                path = name

        app.add_api_route(f"/{path}", func, name=name, methods=methods)

    uvicorn.run(app, host="0.0.0.0", port=_port)


def main():
    project_root = os.getenv("PYWEBWRAPPER_PROJECT_ROOT", None)
    if project_root is None:
        raise ValueError(
            "Environment variable PYWEBWRAPPER_PROJECT_ROOT missing or None"
        )

    project_path = os.getenv("PYWEBWRAPPER_PROJECT_FILE", None)
    if project_path is None:
        raise ValueError(
            "Environment variable PYWEBWRAPPER_PROJECT_FILE missing or None"
        )

    project_config = yaml_parser.get_project_configuration(project_root, project_path)
    print(project_config)
    _setup_framework(project_config)


if __name__ == "__main__":
    main()
