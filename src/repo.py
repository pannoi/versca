import git
import os

from src.utils.environment import Environment
from src.utils.logger import get_logger
from src.utils.errors import GitFailedCloneRepo, GitFailedToPush

from src.helpers import date_manager

logger = get_logger(__name__)

class RepoManager():
    """ Local git repo manager. """
    def clone_repo(self, repo: str, tool: str) -> None:
        """
        Parameters:
            repo(str): Remote git origin repository to clone localy
            tool(str): Name of tool to name folder for cloning
        Raises:
            GitFailedCloneRepo: Raised when failure in cloning remote git repository
        """
        repo = repo.replace('https://', '') if 'https://' in repo else repo
        repo_url = f'https://{Environment.git_username}:{Environment.git_access_token}@{repo}'
        local_path = f'{os.getcwd()}/{tool}'

        try:
            git.Git(local_path).clone(repo_url)
            logger.info('Repo was cloned to %s', local_path)
        except Exception as err:
            logger.error('Failed to clone repo %s', repo_url)
            logger.error(str(err))
            raise GitFailedCloneRepo(repo=repo)

    def push_to_feature_branch(self, tool: str, old_version: str, new_version: str) -> str:
        """
        Parameters:
            tools(str): Name of tool to mention in branch name
            old_version(str): Old version which was declared in local repository
            new_version(str): New version whcih is declared in Github release
        Returns:
            str: New branch name where changes were pushed
        Raises
            GitFailedToPush: Raised when failure creating and pushing new branch
        """
        now = date_manager.now_as_string().replace(':', '-').replace(' ', '-').replace('/', '-')
        branch_name = f'{tool}-version-upgrade-{new_version.replace(".", "-")}-utc-{now}'

        local_repo = git.Repo(f'{os.getcwd()}/{tool}')

        try:
            new_branch = local_repo.create_head(branch_name)
            new_branch.checkout()

            local_repo.git.add(A=True)
            local_repo.git.commit(m=f'Upgrade version {old_version} => {new_version}')
            local_repo.git.push('--set-upstream', 'origin', new_branch)

            logger.info('Changes were pushed for %s to branch %s', tool, branch_name)
            return branch_name
        except Exception as err:
            logger.error('Failed to push to feature branch: %s', new_branch)
            logger.error(err)
            raise GitFailedToPush(branch=branch_name)

