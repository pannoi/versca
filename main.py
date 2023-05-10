import os

from src.slack import Slack
from src.oss import OSS
from src.repo import RepoManager
from src.bot import Bot

from src.utils.environment import Environment
from src.utils.logger import get_logger

from src.helpers import yaml_helper, file_manager, string_parser

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
            try:
                logger.info('Run version scan for %s', key)
                version_prefix = ''
                version_upgrade = False
                chart_version_upgrade = False
                oss_version = oss.check_version(repo=val['github'])
                repo_manager.clone_repo(repo=val['internalRepo'], tool=key)
                if 'helmChart' in val:
                    chart_oss_version = oss.check_chart_version(repo=val['github'], chart=val['helmChart'])

                if 'version' in val:
                    for version in val['version']:
                        local_version = yaml_helper.read_yaml_path(tool=key, file_path=version['file'], yaml_path=version['yamlPath'])
                        suffixed_version = yaml_helper.read_yaml_path(tool=key, file_path=version['file'], yaml_path=version['yamlPath'], helper=True)
                        if suffixed_version != '':
                            version_prefix = string_parser.non_version_pattern_parser(version=suffixed_version)
                        logger.info('Comparing version for %s: %s (local) | %s (public)', key, local_version, oss_version)
                        if oss_version != local_version:
                            version_upgrade = True
                            logger.info('Version upgrade detected: %s | %s => %s', key, local_version, oss_version)
                            yaml_helper.update_yaml_version(tool=key, file_path=version['file'], yaml_path=version['yamlPath'], new_version=oss_version, prefix=version_prefix)

                if 'chart' in val:
                    for chart_version in val['chart']:
                        chart_local_version = yaml_helper.read_yaml_path(tool=key, file_path=chart_version['file'], yaml_path=chart_version['yamlPath'])
                        logger.info('Comparing chart versions for %s: %s (local) | %s (public)', key, chart_local_version, chart_oss_version)
                        if chart_oss_version != chart_local_version:
                            chart_version_upgrade = True
                            logger.info('Helm chart version upgrade detected: %s | %s => %s', key, chart_local_version, chart_oss_version)
                            yaml_helper.update_yaml_version(tool=key, file_path=chart_version['file'], yaml_path=chart_version['yamlPath'], new_version=chart_oss_version)

                if val['autoMR']['enabled'] and version_upgrade:
                    delete_src_branch = False if 'deleteBranch' not in val['autoMR'] else val['autoMR']['deleteBranch']
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
                        notes=release_notes,
                        delete_src_branch=delete_src_branch
                    )

                if val['autoMR']['enabled'] and chart_version_upgrade:
                    delete_src_branch = False if 'deleteBranch' not in val['autoMR'] else val['autoMR']['deleteBranch']
                    release_notes = oss.get_release_notes(repo=val['github'])
                    branch = repo_manager.push_to_feature_branch(tool=key, old_version=chart_local_version, new_version=chart_oss_version)
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
                        old_version=chart_local_version,
                        new_version=chart_oss_version,
                        notes=release_notes,
                        delete_src_branch=delete_src_branch
                    )

                if 'slack' in val and val['slack']['enabled'] and version_upgrade:
                    slack.send_message(
                        ok=True,
                        tool=key,
                        old_version=local_version,
                        new_version=oss_version,
                        people=val['slack']['tag'],
                        auto_mr=val['autoMR']['enabled'],
                        mr_url=mr_url,
                        notes=release_notes
                    )
            except Exception as err:
                logger.error('Failed to scan version for %s', key)
                logger.error(err)
                if 'slack' in val and val['slack']['enabled']:
                    oss_version = 'Not found' if not oss_version else oss_version
                    local_version = 'Not found' if not local_version else local_version
                    slack.send_message(
                        ok=False,
                        tool=key,
                        old_version=local_version,
                        new_version=oss_version,
                        people=val['slack']['tag'],
                        auto_mr=val['autoMR']['enabled']
                    )
                continue
    finally:
        file_manager.cleanup()
        logger.info('%s was cleanup from git cloned folders', os.getcwd())

if __name__ == '__main__':
    run_scirpt()
