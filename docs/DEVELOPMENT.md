# Development Guide

Target audience: benchmark developers. You want to create/modify tasks, and/or modify data pre-baked into the servers.

## Contribute to server data

All services (GitLab, ownCloud, Rocket.Chat, Plane) are pre-baked with data. If you do not need to modify the data, you can skip this section. We generally don't accept contributions to change of data since most of them is in binary format. You could, however, modify the data and host your own server with the modified data for your own use.

**GitLab:** Please refer to [this](../servers/gitlab/README.md) for more details.

**OwnCloud** Please create a GitHub issue if you want to modify the data on your self-hosted server.

**Rocket.Chat:** After the service starts, run `backup-rocketchat` to back up the service, and run `restore-rocketchat` to restore the service.

**Plane:** Please create a GitHub issue if you want to modify the data on your self-hosted server.

## Contribute to a task

If you want to create a task or modify an existing task, please read [this](../workspaces/tasks/example/README.md). We welcome
contributions to tasks, including new tasks and bug fixes to existing tasks.

