import os
import importlib
import uvicorn
from fastapi import FastAPI

from .utils import yaml_parser
from .utils import path_builder


def _setup_framework(project_config):
    app = FastAPI(title=project_config['project']['name'])

    routes = project_config['project']['entrypoints']
    module_path = project_config['project']['module']

    app_module = importlib.import_module(module_path)

    for route in routes:
        path = route.get('path', None)
        name = route.get('name', None)
        methods = route.get('methods', ['GET'])
        entrypoint = route.get('entrypoint', None)
        if entrypoint is None:
            raise ValueError('entrypoint in the entrypoints cannot be None')
        if name is None:
            name = entrypoint

        func = getattr(app_module, entrypoint)

        if path is None:
            if 'GET' in methods:
                path_builder.build_path(func, name)
            else:
                path = name

        print(methods)
        print(func)
        print(path)
        app.add_api_route(f'/{path}', func, name=name, methods=methods)

    uvicorn.run(app, host='0.0.0.0', port=5000)


def main():
    project_root = os.getenv('PYWEBWRAPPER_PROJECT_ROOT', None)
    if project_root is None:
        raise ValueError('Environment variable PYWEBWRAPPER_PROJECT_ROOT missing or None')

    project_path = os.getenv('PYWEBWRAPPER_PROJECT_FILE', None)
    if project_path is None:
        raise ValueError('Environment variable PYWEBWRAPPER_PROJECT_FILE missing or None')

    project_config = yaml_parser.get_project_configuration(project_root, project_path)
    print(project_config)
    _setup_framework(project_config)


if __name__ == '__main__':
    main()
