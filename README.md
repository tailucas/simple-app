# simple-app
Simplest possible app based on [base-app](https://github.com/tailucas/base-app) whose built images are maintained by me in [Docker Hub](https://hub.docker.com/repository/docker/tailucas/base-app/tags?page=1&ordering=last_updated).

# Required Tools

## Option 1: VSCode Dev Container
Assuming a Linux environment like Ubuntu with no-password SSH enabled:
1) Install the [docker engine](https://docs.docker.com/engine/install/ubuntu/) with the current user added to the [docker group](https://docs.docker.com/engine/install/linux-postinstall/) to eliminate the need to run the docker CLI using sudo.
2) Clone this project: https://github.com/tailucas/simple-app.git
3) Start [VS Code](https://code.visualstudio.com/) and add an SSH remote to your device that has the checked out project and add the project folder to the workspace at which point VS Code will prompt to build the project using a development container. When the container build is done, then open a new terminal in vscode.
4) Open `./app/__main__.py` for an example Python project. Make sure that VS Code has selected `./.venv/bin/python` as the runtime that Poetry has set up for you, then imports to `tailucas_pylib` will resolve properly.
5) Verify that the local Java dependencies are working by opening `./src/main/java/simple/app/App.java` and checking imports.
6) Run the applications using `task run` and in a separate terminal look for the application logs under `/var/log/syslog`.
7) If you do not want to run any Python app, set the environment variable `NO_PYTHON_APP` to anything. See [base_entrypoint.sh](https://github.com/tailucas/base-app/blob/862c244bb0f53dff47d4a6e8f829972e060cf060/base_entrypoint.sh#L20) for an example. If you do not want to run a Java app, set the environment variable `RUN_JAVA_APP` to anything other than `true`. See [base_entrypoint.sh](https://github.com/tailucas/base-app/blob/862c244bb0f53dff47d4a6e8f829972e060cf060/base_entrypoint.sh#L34C9-L34C21) for an example. See the `create-dot-env` command in [Taskfile.yml](https://github.com/tailucas/simple-app/blob/a90d6f4f752738277b0b5c90bb840a1b6e5170a6/Taskfile.yml#L25) for example environment variable settings.

## Option 2: Native Environment
Install these tools and make sure that they are on the environment `$PATH`.

* `task` for project build orchestration: https://taskfile.dev/installation/#install-script
* `docker` and `docker-compose` for container builds and execution: https://docs.docker.com/engine/install/
* `mvn` Maven for Java build orchestration: https://maven.apache.org/download.cgi
* `poetry` for Python dependency management: https://python-poetry.org/docs/#installation
* `java` and `javac` for Java build and runtime: https://aws.amazon.com/corretto/
* `python` is `python3` for Python runtime: https://www.python.org/downloads/
