import pytest
import os
from context import yaml_helper

test_file = f'{os.getcwd()}/tests/fixture/test.yaml'

@pytest.mark.parametrize('lookup_key, lookup_value', [
    ('name', 'testBlock'),
    ('version', '0.1.0')
])
def test_yaml_to_dict(lookup_key, lookup_value):
    data = yaml_helper.yaml_to_dict(file_path=test_file)

    assert data['test'][lookup_key] == lookup_value

@pytest.mark.parametrize('version', [
    '0.1.0'
])
def test_read_yaml_path(version):
    yaml_version = yaml_helper.read_yaml_path(
        tool='tests/fixture',
        file_path='test.yaml',
        yaml_path='test.version'
    )

    assert version == yaml_version

@pytest.mark.parametrize('version', [
    '0.2.0',
    '0.1.0'
])
def test_update_yaml_version(version):
    yaml_helper.update_yaml_version(
        tool='tests/fixture',
        file_path='test.yaml',
        yaml_path='test.version',
        new_version=version
    )

    yaml_helper.update_yaml_version(
        tool='tests/fixture',
        file_path='test.yaml',
        yaml_path='test.version',
        new_version=version
    )
