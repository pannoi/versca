import pytest
from context import string_parser

@pytest.mark.parametrize('version, result', [
    ('1.2.3', '1.2.3'),
    ('v1.2.3', '1.2.3'),
    ('15.3.203 alalala', '15.3.203'),
    ('21.2.30-mimir', '21.2.30'),
    ('mimir-go asda2.1.3', '2.1.3')
])
def test_yaml_to_dict(version, result):
    v = string_parser.version_pattern_parser(version=version)

    assert v == result
