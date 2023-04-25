# Tool Version Scanner

VerSca is a tool to version scanner for applications which you are deploying into [Kubernetes](https://github.com/kubernetes/kubernetes) with
- [Helm](https://github.com/helm/helm)
- [Manifests](https://github.com/kubernetes/kubernetes)
- [Kustomize](https://github.com/kubernetes-sigs/kustomize)

Once you specify version in your *private* repository in one YAML files, which would be use by one of technologies above

## Usage

### Config

In [config](config.yaml) you need to specify the tools which to scan with needed parameters. [Example](config-example.yaml) file is located in repository

__Example:__

```yaml
prometheus: # Tool name
  github: https://github.com/prometheus/prometheus # Publich Tool repo
  internalRepo: # Internal repo which contains some values.yaml file
  slack:
    enabled: true # If you'd like to receive some slack notification
    tag: # Who tag in slack message (keep empty if noone tag: [])
      - team # Slack group to tag 
      - UXXXXXXX # Slack User Id to tag
  autoMR:
    enabled: true # Automatically create MR to masterBranch if new version is detected
    masterBranch: main # To which branch create MR/PR if new version is detected
    projectId: 00000000 # Mandatory for gitlab (Gitlab projectId)
    repoName: prometheus # Mandatory for github/bitbucket (repository name)
    owner: pannoi # Mandatory for github/bitbucket (Owner name: usually organisation)
  version:
    - file: base/prometheus-prometheus.yaml # values.yaml file with specified version
      yamlPath: spec.version # Yaml path where version specified in file
```
---
__Example with Helm:__

```yaml
mimir:
  github: https://github.com/grafana/mimir # Publich Tool repo
  internalRepo: # Internal repo which contains some values.yaml file
  helmChart: operations/helm/charts/mimir-distributed/Chart.yaml # Optional
  slack:
    enabled: true # If you'd like to receive some slack notification
    tag: # Who tag in slack message (keep empty if noone tag: [])
      - team # Slack group to tag 
      - UXXXXXXX # Slack User Id to tag
  autoMR:
    enabled: true # Automatically create MR to masterBranch if new version is detected
    masterBranch: main # To which branch create MR/PR if new version is detected
    projectId: 00000000 # Mandatory for gitlab
  chart: # Needed only if helmChart specified
    - file: overlays/kustomization.yaml # File where is specified helm chart version
      yamlPath: helmCharts[0].version # Yaml path to where is chart version specified
```


### Auto MR/PR

Support for Version Control application to provide automatic MR/PR when new version is detected:

- [Github](https://github.com)
- [Gitlab](https://gitlab.com)
- [Bitbucket](https://bitbucket.org)

Once new version would be detected changed would be pushed to new branch `{tool}-version-upgrade-{new_version}-utc-{datetime}` and MR/PR would be created to `main` branch which you specified in your repository

> Be aware that your bot account which you specify in env variables should have propper permissions

### Notifications

To receive notifications, you need to generate slack webhook url and set is [env variable](#environment)

It will be posting new release version with release notes as description

Also might tag people/groups if you specify them in [config file](#config)

> For group just write name, for users slack UserId is needed

## How to run

- Clone repository
```bash
git clone https://github.com/pannoi/versca.git && cd versca
```
- Fill [config YAML file](config.yaml) based on [example](config-example.yaml)

- Set [env variables](#environment)

### Environment

| Variable          | Description                                                                                | Required | Type   |
|-------------------|--------------------------------------------------------------------------------------------|----------|--------|
| GIT_USERNAME      | Git username to pull/push repository and create MR/PR                                      | YES      | string |
| GIT_ACCESS_TOKEN  | Git access token for user authentication (R/W access to repository)                        | YES      | string |
| CONFIG_FILE       | If you'd like to use custom config file name(Default: config.yaml in application root dir) | NO       | string |
| SLACK_WEBHOOK_URL | Generated webhook by slack to send messages (if you'd like to receive notification)        | NO       | string |
| GITHUB_TOKEN      | Generated Github token, to extends API quota (60 per hour => 5000 per hour)                | NO       | string |

### Local
  
```bash
python3 -u main.py
```

### Docker

```bash
docker build -t versca .
docker run -it \
    -e GIT_ACCESS_TOKEN="" \
    -e GIT_USERNAME="" \
    -e CONFIG_FILE="config.yaml" \
    -e SLACK_WEBHOOK_URL="" \
    versca
```

### Kubernetes

- Build and publish docker image 

```bash
docker build -t my.registry/versca:latest .
docker push my.registry/versca:latest
```

- Deploy kubernetes `cronjob` resource with built image

```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: versca
spec:
  schedule: "*/30 5-15 * * 1-5"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: versca
            image: my.registry/versca:latest
            imagePullPolicy: IfNotPresent
            env:
              - name: GIT_USERNAME
                value:
              - name: GIT_ACCESS_TOKEN
                value:
              - name: CONFIG_FILE
                value:
              - name: SLACK_WEBHOOK_URL
                value:
              - name: GITHUB_TOKEN
                value:
          restartPolicy: OnFailure
```

> Don't forget to change schedule based on your needs
