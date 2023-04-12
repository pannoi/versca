import sys
import json
import requests

from src.utils.environment import Environment
from src.utils.logger import get_logger
from src.utils.errors import SlackFailedSendMessage, SlackWebhookUrlNotSet

logger = get_logger(__name__)

class Slack():
    """ Class to send messages to slack. """
    def __init__(self) -> None:
        self.url = Environment.slack_webhook_url
        self.title = 'Version check done'

    def send_message(self,
                     tool: str,
                     old_version: str,
                     new_version: str,
                     people: list,
                     auto_mr: bool,
                     mr_url: str,
                     notes: str) -> None:
        """
        Sends message to slack channel provided in env:SLACK_WEBHOOK_URL

        Parameters:
            tool(str): Name of tool which was checked
            old_version(str): Old version which was declared in local repository
            new_version(str): New version which is available in Github
            people(str): People who should be tagged in slack notification
            auto_mr(bool): Is autoMR parameter enabled for app
            mr_url(str): Merge request url which was generated after creating MR to repository
            notes(str): Release notes which were grabbed from Github when release was published
        Raises:
            SlackFailedSendMessage: Raised when response from slack is NOT OK (200/201)
        """
        if not self.url:
            logger.error("SLACK_WEBHOOK_URL env variable not set")
            raise SlackWebhookUrlNotSet

        color = "#36a64f"
        message = f'Goind to upgrade {tool} version: {old_version} => {new_version}'

        if auto_mr:
            message = message + f'\n MR automatically created: {mr_url}'
            message = message + f'\n Release notes: {notes}'

        people = ["@" + el for el in people]
        people = ', '.join(people)
        message = message + f'\n {people}'

        slack_payload = {
            "username": "version-checker",
            "channel": "random",
            "link_names": 1,
            "attachments": [
                {
                "mrkdwn_in": ["text"],
                    "color": color,
                    "title": self.title,
                    "text": message,
                }
            ]
        }

        byte_length = str(sys.getsizeof(slack_payload))
        headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
        response = requests.post(self.url, data=json.dumps(slack_payload), headers=headers, timeout=120)
        if not response.ok:
            logger.error('Failed to send message to slack')
            logger.error(response.json())
            raise SlackFailedSendMessage(text=response.text)
        logger.info('Slack message was sent')
