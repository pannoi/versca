import requests

from src.utils.environment import Environment
from src.utils.logger import get_logger
from src.utils.errors import OssFailedToGetReleaseNotes, OssFailedToGetVersion

logger = get_logger(__name__)

class OSS():
    """ Class which refs to OSS projects to grab release info. """
    def __init__(self) -> None:
        if Environment.github_token:
            self.headers = {
                'Accept': 'application/vnd.github+json',
                'Authorization': f'Bearer {Environment.github_token}',
                'X-GitHub-Api-Version': '2022-11-28',
            }
        else:
            self.headers = {
                'Accept': 'application/vnd.github+json',
                'X-GitHub-Api-Version': '2022-11-28',
            }

    def check_version(self, repo: str) -> str:
        """
        Check github latest published release

        Parameters:
            repo(str): OSS Project git repository to check
        Returns:
            str: Version which was scrapped from published releases
        Raises:
            OssFailedToGetVersion: Raises when unable to capture published release version
        """
        repo = repo.replace('https://', '') if 'https://' in repo else repo
        repo = repo.replace('github.com/', '')
        url = f'https://api.github.com/repos/{repo}/releases/latest'

        response = requests.get(url=url, headers=self.headers, timeout=120)
        if not response.ok:
            logger.error('Failed to request version from %s', url)
            logger.error(response.json())
            raise OssFailedToGetVersion(repo=repo)

        version = response.json()['name']
        if " " in version:
            version = version.split(" ")[0]

        return str(version)

    def get_release_notes(self, repo: str) -> str:
        """
        Returns as string scrapped release notes from github

        Parameters:
            repo(str): OSS Project git repository to check
        Returns:
            str: Release notes which was scrapped from published releases
        Raises:
            OssFailedToGetReleaseNotes: Raises when unable to capture published notes
        """
        headers = {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
        }

        repo = repo.replace('https://', '') if 'https://' in repo else repo
        repo = repo.replace('github.com/', '')
        url = f'https://api.github.com/repos/{repo}/releases/latest'

        response = requests.get(url=url, headers=self.headers, timeout=120)
        if not response.ok:
            logger.error('Failed to request version from %s', url)
            logger.error(response.json())
            raise OssFailedToGetReleaseNotes(repo=repo)

        return str(response.json()['body'])
