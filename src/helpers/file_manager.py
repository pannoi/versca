import os
import shutil

from src.utils.logger import get_logger

logger = get_logger(__name__)

def cleanup() -> None:
    """ Method to cleanup application filesystem after run. """
    retain = [
        '.git',
        'src',
        'tests',
        'kubernetes',
        'docs',
        '.pytest_cache',
        '__pycache__',
    ]

    dirs = filter(os.path.isdir, os.listdir(os.getcwd()))
    try:
        for item in dirs:
            if item not in retain:
                shutil.rmtree(item)
    finally:
        logger.info('Directory was cleanup from local files')