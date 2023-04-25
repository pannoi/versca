import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Environment:
    """ Class describes .env variables. """
    config_file: str = os.getenv("CONFIG_FILE")
    git_username: str = os.getenv("GIT_USERNAME")
    git_access_token: str = os.getenv("GIT_ACCESS_TOKEN")
    slack_webhook_url: str = os.getenv("SLACK_WEBHOOK_URL")
    github_token: str = os.getenv("GITHUB_TOKEN")
