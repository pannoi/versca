import pytest
from context import errors

def test_yaml_converter_error():
    with pytest.raises(errors.YamlConvertError) as excinfo:
        raise errors.YamlConvertError()
    
    assert "Failed to convert YAML to dict" in str(excinfo.value)

def test_yaml_dept_error():
    with pytest.raises(errors.YamlPathDepthError) as excinfo:
        raise errors.YamlPathDepthError(depth=6)

    assert "Yaml depth more than 5 nests is not supported, provided: " in str(excinfo.value)

def test_yaml_read_version_error():
    with pytest.raises(errors.YamlReadVersionError) as excinfo:
        raise errors.YamlReadVersionError()
    
    assert "Failed to read version field in YAML file" in str(excinfo.value)

def test_yaml_read_file_error():
    with pytest.raises(errors.YamlReadFileError) as excinfo:
        raise errors.YamlReadFileError(filename='test.txt')
    
    assert "Failed to read yaml file: " in str(excinfo.value)

def test_yaml_update_file_error():
    with pytest.raises(errors.YamlUpdateFileError) as excinfo:
        raise errors.YamlUpdateFileError(filename='test.txt')
    
    assert "Failed to update yaml file: " in str(excinfo.value)

def test_slack_failed_send_message():
    with pytest.raises(errors.SlackFailedSendMessage) as excinfo:
        raise errors.SlackFailedSendMessage(text='placeholder')
    
    assert "Failed to send slack message: " in str(excinfo.value)

def test_slack_webhook_url_not_set():
    with pytest.raises(errors.SlackWebhookUrlNotSet) as excinfo:
        raise errors.SlackWebhookUrlNotSet()
    
    assert "Env variable SLACK_WEBHOOK_URL not set" in str(excinfo.value)

def test_git_failed_clone_repo():
    with pytest.raises(errors.GitFailedCloneRepo) as excinfo:
        raise errors.GitFailedCloneRepo(repo='github.com')
    
    assert "Failed to clone git repo: " in str(excinfo.value)

def test_git_failed_to_push():
    with pytest.raises(errors.GitFailedToPush) as excinfo:
        raise errors.GitFailedToPush(branch='master')
    
    assert "Failed to push git repo: " in str(excinfo.value)

def test_oss_failed_to_get_version():
    with pytest.raises(errors.OssFailedToGetVersion) as excinfo:
        raise errors.OssFailedToGetVersion(repo='github.com')
    
    assert "Failed to get version from OSS project: " in str(excinfo.value)

def test_oss_failed_to_get_release_notes():
    with pytest.raises(errors.OssFailedToGetReleaseNotes) as excinfo:
        raise errors.OssFailedToGetReleaseNotes(repo='github.com')
    
    assert "Failed to get release notes from OSS project: " in str(excinfo.value)

def test_oss_failed_to_get_chart_version():
    with pytest.raises(errors.OssFailedToGetChartVersion) as excinfo:
        raise errors.OssFailedToGetChartVersion(repo='github.com')
    
    assert "Failed to get chart version from OSS project: " in str(excinfo.value)

def test_mr_bot_not_supported_git_repository():
    with pytest.raises(errors.MrBotNotSupportedGitRepository) as excinfo:
        raise errors.MrBotNotSupportedGitRepository()
    
    assert "Not supported version controll app, only suppoerted: Github/Gitlab/Bitbucket" in str(excinfo.value)

def test_mr_bot_failed_create_merge_request():
    with pytest.raises(errors.MrBotFailedCreateMergeRequest) as excinfo:
        raise errors.MrBotFailedCreateMergeRequest(repo='github.com')
    
    assert "Failed to create MR: " in str(excinfo.value)