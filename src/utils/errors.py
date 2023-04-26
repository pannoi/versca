class YamlConvertError(Exception):
    """ Yaml to dict conver error. """
    def __init__(self, message: str="Failed to convert YAML to dict") -> None:
        self.message = message
        super().__init__(self.message)
    def __str__(self) -> str:
        return f'{self.message}'
    
class YamlPathDepthError(Exception):
    """ To deep yaml path. """
    def __init__(self, depth: int,message: str="Yaml depth more than 7 nests is not supported, provided: ") -> None:
        self.message = message
        self.depth = depth
        super().__init__(self.message)
    def __str__(self) -> str:
        return f'{self.message}{self.depth}'

class YamlReadVersionError(Exception):
    """ Failed to read version from yaml local file. """
    def __init__(self, message: str="Failed to read version field in YAML file") -> None:
        self.message = message
        super().__init__(self.message)
    def __str__(self) -> str:
        return f'{self.message}'

class YamlReadFileError(Exception):
    """ Failed to read yaml local file. """
    def __init__(self, filename: str, message: str="Failed to read yaml file: ") -> None:
        self.message = message
        self.filename = filename
        super().__init__(self.message)
    def __str__(self) -> str:
        return f'{self.message}{self.filename}'

class YamlUpdateFileError(Exception):
    """ Failed to update yaml local file. """
    def __init__(self, filename: str, message: str="Failed to update yaml file: ") -> None:
        self.message = message
        self.filename = filename
        super().__init__(self.message)
    def __str__(self) -> str:
        return f'{self.message}{self.filename}'

class SlackFailedSendMessage(Exception):
    """ Failed to send message to slack. """
    def __init__(self, text: str, message: str="Failed to send slack message: ") -> None:
        self.message = message
        self.text = text
        super().__init__(self.message)
    def __str__(self) -> str:
        return f'{self.message}{self.text}'
    
class SlackWebhookUrlNotSet(Exception):
    """ Slack webhook url env variable not set. """
    def __init__(self, message: str="Env variable SLACK_WEBHOOK_URL not set") -> None:
        self.message = message
        super().__init__(self.message)
    def __str__(self) -> str:
        return f'{self.message}'
    
class GitFailedCloneRepo(Exception):
    """ Failed to clone git repo. """
    def __init__(self, repo: str, message: str="Failed to clone git repo: ") -> None:
        self.message = message
        self.repo = repo
        super().__init__(self.message)
    def __str__(self) -> str:
        return f'{self.message}{self.repo}'
    
class GitFailedToPush(Exception):
    """ Failed to push git repo to custom branch. """
    def __init__(self, branch: str, message: str="Failed to push git repo: ") -> None:
        self.message = message
        self.branch = branch
        super().__init__(self.message)
    def __str__(self) -> str:
        return f'{self.message}{self.branch}'
    
class OssFailedToGetVersion(Exception):
    """ Failed to get release version from oss project. """
    def __init__(self, repo: str, message: str="Failed to get version from OSS project: ") -> None:
        self.message = message
        self.repo = repo
        super().__init__(self.message)
    def __str__(self) -> str:
        return f'{self.message}{self.repo}'
   
class OssFailedToGetChartVersion(Exception):
    """ Failed to get chart version from oss project. """
    def __init__(self, repo: str, message: str="Failed to get chart version from OSS project: ") -> None:
        self.message = message
        self.repo = repo
        super().__init__(self.message)
    def __str__(self) -> str:
        return f'{self.message}{self.repo}'


class OssFailedToGetReleaseNotes(Exception):
    """ Failed to get release notes from oss project. """
    def __init__(self, repo: str, message: str="Failed to get release notes from OSS project: ") -> None:
        self.message = message
        self.repo = repo
        super().__init__(self.message)
    def __str__(self) -> str:
        return f'{self.message}{self.repo}'

class MrBotNotSupportedGitRepository(Exception):
    """ Not supported git repo. """
    def __init__(self,message: str="Not supported version controll app, only suppoerted: Github/Gitlab/Bitbucket") -> None:
        self.message = message
        super().__init__(self.message)
    def __str__(self) -> str:
        return f'{self.message}'

class MrBotFailedCreateMergeRequest(Exception):
    """ Failed to create MR """
    def __init__(self, repo: str, message: str="Failed to create MR: ") -> None:
        self.message = message
        self.repo = repo
        super().__init__(self.message)
    def __str__(self) -> str:
        return f'{self.message}{self.repo}'
