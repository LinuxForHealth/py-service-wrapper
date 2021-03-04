import yaml
import os


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
