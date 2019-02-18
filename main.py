import json
import os
from datetime import datetime, timedelta

import requests
import timeago
from github import Github

# create API token on https://github.com/settings/tokens
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPO = os.environ["GITHUB_REPO"]
SLACK_HOOK_URL = os.environ["SLACK_HOOK_URL"]
SLACK_CHANNEL_NAME = os.environ["SLACK_CHANNEL_NAME"]
SLACK_BOT_NAME = os.environ["SLACK_BOT_NAME"]
HOURS_OLD = int(os.environ["HOURS_OLD"])

URL_TEMPLATE = "https://github.com/" + GITHUB_REPO + "/pull/{number}"


def slack_message(text, channel=SLACK_CHANNEL_NAME, name=SLACK_BOT_NAME, icon_emoji=":fire:"):
    payload = {
        "channel": channel,
        "username": name,
        "text": text,
        "icon_emoji": icon_emoji
    }
    requests.post(SLACK_HOOK_URL, data=json.dumps(payload))


def run(event, context):
    gh_client = Github(GITHUB_TOKEN)
    now = datetime.utcnow()
    date_from = now - timedelta(hours=HOURS_OLD)

    pulls = []
    repo = gh_client.get_repo(GITHUB_REPO)
    for pull in repo.get_pulls(state='open', sort='created'):
        # check if matching date and title does not contain WIP
        if pull.created_at < date_from and not ("wip" in pull.title.lower()):
            url = URL_TEMPLATE.format(number=pull.number)
            pulls.append(
                "*<{}|{}>* from *{}* - _created {}_".format(url, pull.title, pull.user.login, timeago.format(pull.created_at, now)))

    if len(pulls):
        msg = "*Unresolved Pull-Requests found!*\n{}".format("\n".join(pulls))
        slack_message(msg)
