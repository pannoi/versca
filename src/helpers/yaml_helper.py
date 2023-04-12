import yaml
import os
import ruamel.yaml

from src.utils.logger import get_logger
from src.utils.errors import YamlConvertError, YamlPathDepthError, YamlReadFileError, YamlUpdateFileError, YamlReadVersionError

logger = get_logger(__name__)

def yaml_to_dict(file_path: str) -> dict:
    """
    Converts YAML file into dict

    Parameters:
        file_path: YAML file path to convert into dict
    Returns:
        dict: Converted YAML file conent
    Raises:
        YamlConvertError: Raises when failed to convert YAML into dict
    """
    with open(file_path, 'r', encoding='UTF-8') as config:
        try:
            data = yaml.load(config, Loader=yaml.FullLoader)
            return data
        except Exception as err:
            logger.error("Failed to convert yaml to dict: ")
            logger.error(err)
            raise YamlConvertError()

def read_yaml_path(tool: str, file_path: str, yaml_path: str) -> str:
    """
    Read YAML version based on provided path

    Parameters:
        tool(str): Name of tool to specify as folder in path
        file_path(str): File path to lookup in tool directory
        yaml_path(str): Provided yaml path to read version
    Returns:
        str: Found current version of application
    Raises:
        YamlReadVersionError: Raises when unable to locate provided yaml_path in YAML file
    """
    file_path = f'{os.getcwd()}/{tool}/{file_path}'
    yaml_path = yaml_path.split('.')
    path_counter = 0

    data = yaml_to_dict(file_path=file_path)

    while path_counter <= (len(yaml_path) - 1):
        if path_counter == 0:
            version = data[yaml_path[path_counter]]
        else:
            version = version[yaml_path[path_counter]]
        path_counter += 1

    if not str(version):
        logger.error('Cannot find version in provided YAML path: %s', yaml_path)
        raise YamlReadVersionError

    return str(version)

def update_yaml_version(tool: str, file_path: str, yaml_path: str, new_version: str) -> None:
    """
    Update YAML version based on provided path

    Parameters:
        tool(str):  Name of tool to specify as folder in path
        file_path(str): File path to lookup in tool directory
        yaml_path(str): Provided YAML path to update
        new_version(str): New version to which update yaml_path
    Raises:
        YamlReadFileError: Raises when unable to read YAML file
        YamlPathDepthError: Raises when yaml nested depth more than 5
        YamlUpdateFileError: Raises when unable to update YAML file
    """
    file_name = f'{os.getcwd()}/{tool}/{file_path}'
    try:
        config, ind, bsi = ruamel.yaml.util.load_yaml_guess_indent(open(file_name, encoding='UTF-8'))
    except Exception as err:
        logger.error('Failed to read YAML filed: %s', file_path)
        logger.error(err)
        raise YamlReadFileError(filename=file_name)

    yaml_path = yaml_path.split('.')

    upd = {yaml_path[-1]: new_version}

    if len(yaml_path) == 1:
        config.update(upd)
    elif len(yaml_path) == 2:
        config[yaml_path[0]].update(upd)
    elif len(yaml_path) == 3:
        config[yaml_path[0]][yaml_path[1]].update(upd)
    elif len(yaml_path) == 4:
        config[yaml_path[0]][yaml_path[1]][yaml_path[2]].update(upd)
    elif len(yaml_path) == 5:
        config[yaml_path[0]][yaml_path[1]][yaml_path[2]][yaml_path[3]].update(upd)
    else:
        logger.error('Depth more than 6 nests is not supported')
        raise YamlPathDepthError(depth=len(yaml_path))

    try:
        yml = ruamel.yaml.YAML()
        with open(f'{tool}/{file_path}', 'w', encoding='UTF-8') as fp:
            yml.dump(config, fp)
    except Exception as err:
        logger.error('Failed to update provided YAML file: %s', file_path)
        logger.error(err)
        raise YamlUpdateFileError(filename=file_name)
