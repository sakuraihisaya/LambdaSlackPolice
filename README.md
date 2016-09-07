# Slack Police

Slack Police can delete files on slack at regular intervals.

## Examples

```python
police = SlackPolice()
police.delete_all_files()
```

## Installation

```shell
$ pip install -r requirements.txt
```

## Settings
set slack api token to enviroment variables.

```shell
$ export SLACK_API_TOKEN=xxxxxxxxx
```