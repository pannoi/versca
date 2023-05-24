import re

def version_pattern_parser(version: str) -> str:
    """
    Parsing string to version pattern: 0.0.0

    Parameters:
        version(str): String to convert into pattern
    Rerturns:
        str: Cutted stirng which is matching pattern: 0.0.0
    """
    version = version.replace('v', '') if 'v' in version else version

    version_pattern = re.compile(r"\d+\.\d+\.\d+")
    deletion_pattern = re.sub(version_pattern, '', version)

    return version.replace(deletion_pattern, '')

def non_version_pattern_parser(version: str) -> str:
    """
    Parsing string to NON version pattern: 0.0.0

    Parameters:
        version(str): String to convert into pattern
    Rerturns:
        str: Cutted stirng which is NOT matching pattern: 0.0.0
    """
    version_pattern = re.compile(r"\d+\.\d+\.\d+")
        
    return str(re.sub(version_pattern, '', version))
