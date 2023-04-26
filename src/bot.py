import requests

from src.utils.environment import Environment
from src.utils.logger import get_logger
from src.utils.errors import MrBotNotSupportedGitRepository, MrBotFailedCreateMergeRequest

logger = get_logger(__name__)

class Bot():
    """ MR Bot to create in version control apps. """
    def create_merge_request(self,
                             tool: str,
                             repo: str,
                             project_id: int,
                             repo_name: str,
                             owner: str,
                             src_branch: str,
                             dest_branch: str,
                             old_version: str,
                             new_version: str,
                             notes: str,
                             delete_src_branch: bool) -> str:
        """
        Call propper MR creationg method in class based on repo url

        Parameters:
            tool(str): Name of tool which version was checked
            repo(str): Local repository git url
            project_id(int): Gitlab project ID (Empty if not Gitlab)
            repo_name(str): Repository name (Empty if Gitlab)
            owner(str): Organization owner (Empty if Gitlab)
            src_branch(str): Generated branch where version update was pushed
            dest_branch(str): Main repository branch (ususally: master/main)
            old_version(str): Old version which was detected in local repository
            new_version(str): New version which was scrapped from OSS project
            notes(str): Release notes from OSS project
            delete_src_branch(bool): if True src branch checkbox would be enabled, else disabled
        Returns:
            str: Generated Merge Request url after webhook
        Raises:
            MrBotNotSupportedGitRepository: Raises when non supported version control
        """
        mr_title = f'{tool.capitalize()} version upgrade: {old_version} => {new_version}'

        if 'gitlab' in repo:
            return self.create_gitlab_mr(
                project_id=project_id,
                src_branch=src_branch,
                dest_branch=dest_branch,
                mr_title=mr_title,
                notes=notes,
                delete_src_branch=delete_src_branch
            )
        elif 'github' in repo:
            return self.create_github_pr(
                repo_name=repo_name,
                owner=owner,
                src_branch=src_branch,
                dest_branch=dest_branch,
                mr_title=mr_title,
                notes=notes
            )
        elif 'bitbucket' in repo:
            return self.create_bitbucket_pr(
                owner=owner,
                repo_name=repo_name,
                mr_title=mr_title,
                src_branch=src_branch,
                dest_branch=dest_branch,
                notes=notes,
                delete_src_branch=delete_src_branch
            )
        else:
            logger.error('%s auto MR/PR not supported', repo)
            raise MrBotNotSupportedGitRepository

    def create_gitlab_mr(self,
                         project_id: int,
                         dest_branch: str,
                         src_branch: str,
                         mr_title: str,
                         notes: str,
                         delete_src_branch: bool) -> str:
        """
        Method to create Merge Request in Gitlab

        Parameters:
            project_id(int): Gitlab project id
            dest_branch(str): Destination branch where to merge
            src_branch(str): Source branch which to merge
            mr_title(str): Merge Request title
            notes(str): Release notes from OSS project
            delete_src_branch(bool): if True src branch checkbox would be enabled, else disabled
        Returns:
            str: Generated Merge Request url after webhook
        Raises:
            MrBotFailedCreateMergeRequest: Raises when POST response NOT OK (200/201)
        """
        url = f'https://gitlab.com/api/v4/projects/{project_id}/merge_requests'

        headers = {'PRIVATE-TOKEN': f'{Environment.git_access_token}'}

        payload = {
            'source_branch': src_branch,
            'target_branch': dest_branch,
            'title': mr_title,
            'description': notes,
            'remove_source_branch': delete_src_branch
        }

        response = requests.post(url=url, json=payload, headers=headers, timeout=60)
        if not response.ok:
            logger.error('Failed to create MR in GitLab')
            logger.error(response.json())
            raise MrBotFailedCreateMergeRequest(repo=str(project_id))

        logger.info('Merge request in gitlab was created: %s', mr_title)
        return response.json()['web_url']

    def create_github_pr(self,
                         owner: str,
                         repo_name: str,
                         dest_branch: str,
                         src_branch: str,
                         mr_title: str,
                         notes: str) -> str:
        """
        Method to create Pull Request in Github

        Parameters:
            owner(str): Repository owner (Organization name)
            repo_name(int): Repository name in Github
            dest_branch(str): Destination branch where to merge
            src_branch(str): Source branch which to merge
            mr_title(str): Pull Request title
            notes(str): Release notes from OSS project
        Returns:
            str: Generated Pull Request url after webhook
        Raises:
            MrBotFailedCreateMergeRequest: Raises when POST response NOT OK (200/201)
        """
        url = f'https://api.github.com/repos/{owner}/{repo_name}/pulls'

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {Environment.git_access_token}',
            'X-GitHub-Api-Version': '2022-11-28'
        }

        payload = {
            'title': 'mr_title',
            'owner': owner,
            'repo': repo_name,
            'body': notes,
            'base': src_branch,
            'head': dest_branch
        }

        response = requests.post(url=url, json=payload, headers=headers, timeout=60)
        if not response.ok:
            logger.error('Failed to create PR in Github')
            logger.error(response.json())
            raise MrBotFailedCreateMergeRequest(repo=repo_name)

        logger.info('Pull request in github was created: %s', mr_title)
        return response.json()['html_url']

    def create_bitbucket_pr(self,
                         owner: str,
                         repo_name: str,
                         dest_branch: str,
                         src_branch: str,
                         mr_title: str,
                         notes: str,
                         delete_src_branch: bool) -> str:
        """
        Method to create Pull Request in Bitbucket

        Parameters:
            owner(str): Repository owner (Organization name)
            repo_name(int): Repository name in Bitbucket
            dest_branch(str): Destination branch where to merge
            src_branch(str): Source branch which to merge
            mr_title(str): Pull Request title
            notes(str): Release notes from OSS project
            delete_src_branch(bool): if True src branch checkbox would be enabled, else disabled
        Returns:
            str: Generated Pull Request url after webhook
        Raises:
            MrBotFailedCreateMergeRequest: Raises when POST response NOT OK (200/201)
        """
        url = f'https://api.bitbucket.org/2.0/repositories/{owner}/{repo_name}/pullrequests'

        headers = {'Content-Type': 'application/json'}

        payload = {
            'title': mr_title,
            'description': notes,
            'close_source_branch': delete_src_branch,
            'destination': {
                'branch': {
                    'name': dest_branch
                }
            },
            'source': {
                'branch': {
                    'name': src_branch
                }
            }
        }

        response = requests.post(url=url, json=payload, headers=headers, auth=(Environment.git_username, Environment.git_access_token), timeout=60)
        if not response.ok:
            logger.error('Failed to create PR in BitBucket')
            logger.error(response.json())
            raise MrBotFailedCreateMergeRequest(repo=repo_name)
        
        logger.info('Pull request in bitbucket was created: %s', mr_title)
        return response.json()
