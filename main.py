import os

from src.slack import Slack
from src.oss import OSS
from src.repo import RepoManager
from src.bot import Bot

from src.utils.environment import Environment
from src.utils.logger import get_logger

from src.helpers import yaml_helper, file_manager

logger = get_logger(__name__)

slack = Slack()
oss = OSS()
repo_manager = RepoManager()
mr_bot = Bot()

def run_scirpt():
    """ Main scanner. """
    try:
        config_file = Environment.config_file if Environment.config_file else 'config.yaml'

        data = yaml_helper.yaml_to_dict(config_file)
        logger.info('Checking versions for %s', data.keys())

        for key, val in data.items():
            version_upgrade = False
            oss_version = oss.check_version(repo=val['github'])
            repo_manager.clone_repo(repo=val['internalRepo'], tool=key)

            for version in val['version']:
                local_version = yaml_helper.read_yaml_path(tool=key, file_path=version['file'], yaml_path=version['yamlPath'])
                if oss_version != local_version:
                    version_upgrade = True
                    logger.info('Version upgrade detected: %s | %s => %s', key, local_version, oss_version)
                yaml_helper.update_yaml_version(tool=key, file_path=version['file'], yaml_path=version['yamlPath'], new_version=oss_version)

            if val['autoMR']['enabled'] and version_upgrade:
                release_notes = oss.get_release_notes(repo=val['github'])
                branch = repo_manager.push_to_feature_branch(tool=key, old_version=local_version, new_version=oss_version)
                project_id = val['autoMR']['projectId'] if val['autoMR']['projectId'] else ''
                owner = val['autoMR']['owner'] if val['autoMR']['owner'] else ''
                repo_name = val['autoMR']['repoName'] if val['autoMR']['repoName'] else ''
                mr_url = mr_bot.create_merge_request(
                    repo=val['internalRepo'],
                    project_id=project_id,
                    owner=owner,
                    repo_name=repo_name,
                    tool=key,
                    src_branch=branch,
                    dest_branch=val['autoMR']['masterBranch'],
                    old_version=local_version,
                    new_version=oss_version,
                    notes=release_notes
                )

            if val['slack']['enabled'] and version_upgrade:
                slack.send_message(
                    tool=key,
                    old_version=local_version,
                    new_version=oss_version,
                    people=val['slack']['tag'],
                    auto_mr=val['autoMR']['enabled'],
                    mr_url=mr_url,
                    notes=release_notes
                )
    finally:
        file_manager.cleanup()
        logger.info('%s was cleanup from git cloned folders', os.getcwd())

if __name__ == '__main__':
    run_scirpt()
