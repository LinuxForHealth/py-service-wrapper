import yaml
import os
import sys


def _parse_project_configuration(project_file_path: str) -> dict:
    with open(project_file_path) as project_file:
        return yaml.safe_load(project_file)


def get_project_configuration(project_root: str, project_filename: str) -> dict:
    project_file_path = os.path.join(project_root, project_filename)
    
    if not os.path.exists(project_file_path):
        raise ValueError(f'{project_file_path} does not exist in the project root')

    if not os.path.isfile(project_file_path):
        raise ValueError(f'{project_file_path} is not a file')

    project_config = _parse_project_configuration(project_file_path)

    return project_config

def get_framework_required(project_root: str, project_filename: str) -> str:
    project_config = get_project_configuration(project_root, project_filename)
    return 'quart' if project_config['async'] == True else 'flask'

if __name__ == '__main__':
    project_root = sys.argv[1]
    project_filename = sys.argv[2]
    print(get_framework_required(project_root, project_filename))