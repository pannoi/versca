import pytest
import os
from context import file_manager

@pytest.mark.parametrize('foldername', [
    'test_folder',
    'test_folder2'
])
def test_cleanup(foldername):
    os.chdir('tests/fixture')
    new_file = f'{os.getcwd()}/{foldername}'
    os.makedirs(new_file)

    assert os.path.exists(new_file)

    file_manager.cleanup()
    assert not os.path.exists(new_file)

    assert os.path.exists(f'{os.getcwd()}/test.yaml')

    os.chdir('../../')
