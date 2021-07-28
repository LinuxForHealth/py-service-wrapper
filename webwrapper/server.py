import os
import importlib
from inspect import signature

import uvicorn
from fastapi import FastAPI, Header

from .utils import yaml_parser
from .utils import path_builder


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


def _setup_framework(project_config):

    # Py service wrapper deployments need to define the following
    # environment variable if a port other than the default is needed.
    _port = int(os.getenv("PY_SERVICE_WRAPPER_PORT", default="5000"))

    routes = project_config["project"]["entrypoints"]
    module_path = project_config["project"]["module"]

    app_module = importlib.import_module(module_path)

    start_funcs = None
    shutdown_funcs = None
    startup = "startup"
    shutdown = "shutdown"
    if startup in project_config["project"]:
        startups = project_config["project"][startup]
        start_funcs = [getattr(app_module, sp) for sp in startups]

    if shutdown in project_config["project"]:
        shutdowns = project_config["project"][shutdown]
        shutdown_funcs = [getattr(app_module, sn) for sn in shutdowns]

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

        func = getattr(app_module, entrypoint)

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
