import os

# mock .env
os.environ['GIT_ACCESS_TOKEN'] = "XXXXXXXX"
os.environ['GIT_USERNAME'] = "bot@gmail.com"
os.environ['CONFIG_FILE'] = "config.yaml"
os.environ['SLACK_WEBHOOK_URL'] = "slack_url"

def test_env_git_access_token():
    git_access_token = os.getenv('GIT_ACCESS_TOKEN', default=None)
    if git_access_token is None:
        raise OSError("GIT_ACCESS_TOKEN is not set")

def test_env_git_username():
    git_username = os.getenv('GIT_USERNAME', default=None)
    if git_username is None:
        raise OSError("GIT_USERNAME is not set")
    
def test_env_config_file():
    config_file = os.getenv('CONFIG_FILE', default=None)
    if config_file is None:
        raise OSError("CONFIG_FILE is not set")

def test_env_slack_webhook_url():
    slack_url = os.getenv('SLACK_WEBHOOK_URL', default=None)
    if slack_url is None:
        raise OSError("SLACK_WEBHOOK_URL is not set")
