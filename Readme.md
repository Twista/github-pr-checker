Serverless GH PR Checker
===

Simple CRON-like lambda script for automatic PR checking and posting them into Slack.

_Pull requests with `WIP` in name are ignored._

![Example](example.png)

Install
=====

1) clone this repository
```bash
$ git clone git@github.com:Twista/github-pr-checker.git
```
2) install serverless framework
```bash
$ yarn add global serverless
# or
$ npm i g serverless
```

3) install package dependencies
```bash
cd github-pr-checker
yarn
```

4) copy example config and fill variables
```bash
mv example-env .env
```

5) tweak serverless.yml settings (mainly time and your region)
6) deploy
```bash
sls deploy
```

Configuration
=====
`GITHUB_TOKEN` is token you can obtain at https://github.com/settings/tokens 
`GITHUB_REPO` target repository in `<org>/<repo>` format 
`SLACK_HOOK_URL` https://hooks.slack.com/services/...
`HOURS_OLD` since when we want to notify about Pull Requests