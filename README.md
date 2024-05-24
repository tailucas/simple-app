# simple-app
Simplest possible app based on [base-app](https://github.com/tailucas/base-app) whose built images are maintained by me in the [GitHub Container Registry](https://github.com/tailucas/base-app/pkgs/container/base-app).

# Required Tools
1) Install the [docker engine](https://docs.docker.com/engine/install/ubuntu/) with the current user added to the [docker group](https://docs.docker.com/engine/install/linux-postinstall/) to eliminate the need to run the docker CLI using sudo. You will also need the [compose](https://docs.docker.com/compose/install) CLI plugin.
2) Install the [Dev Container CLI](https://code.visualstudio.com/docs/devcontainers/devcontainer-cli). NodeJS on which the CLI depends can be installed using [this](https://nodejs.org/en/download/package-manager).
3) Clone this project: https://github.com/tailucas/simple-app.git
4) Use the project's provided `Makefile` whose default action is to build and start a development container, by simply invoking `make`. If `make` successful, your terminal will show the session on the development container, running as the user `vscode`.
```
vscode ➜ /home/user/simple-app (main) $ whoami
vscode
```

Note: this step can be replaced by opening the `simple-app` folder in [vscode](https://code.visualstudio.com/) which will automatically detect the dev container configuration in `.devcontainer/` and prompt to re-open the project in a container. At this point, you can start a terminal session within the editor and this is redunant.

# Explore the project
1) Open `./app/__main__.py` for an example Python project. Make sure that VS Code has selected `./.venv/bin/python` as the runtime that Poetry has set up for you, then imports to `tailucas_pylib` will resolve properly.
2) Verify that the local Java dependencies are working by opening `./src/main/java/simple/app/App.java` and checking imports.

# Configure the project
If you do not want to run any Python app, set the environment variable `NO_PYTHON_APP` to anything. See [base_entrypoint.sh](https://github.com/tailucas/base-app/blob/862c244bb0f53dff47d4a6e8f829972e060cf060/base_entrypoint.sh#L20) for an example. If you do not want to run a Java app, set the environment variable `RUN_JAVA_APP` to anything other than `true`. See [base_entrypoint.sh](https://github.com/tailucas/base-app/blob/862c244bb0f53dff47d4a6e8f829972e060cf060/base_entrypoint.sh#L34C9-L34C21) for an example. See the `create-dot-env` command in [Taskfile.yml](https://github.com/tailucas/simple-app/blob/a90d6f4f752738277b0b5c90bb840a1b6e5170a6/Taskfile.yml#L25) for example environment variable settings.

# Build and run the runtime container
1) In a dev container terminal session, run the applications using `task run` and in a separate terminal look for the application logs under `/var/log/syslog`.

Note: the applications are designed to run in an application container via the `task run` command for interactive execution or `task rund` for background execution from which Docker will then manage the container life-cycle. For development purposes, the Java sample can be run directly from VS Code and the Python application can be run from the command-line using `poetry run app` which uses a tooling hint found in [pyproject.toml](https://github.com/tailucas/simple-app/blob/42219b79593d12d2646e277d169ff35447c9651f/pyproject.toml#L9). `task rund` is useful because the terminal session can be closed and your built container will continue running on the host docker instance, made possible by the feature `ghcr.io/devcontainers/features/docker-outside-of-docker:1` configured in [base-app](https://github.com/tailucas/base-app/blob/1581a48e6d4d873e58f30c547af1d91fba53df7f/.devcontainer/devcontainer.json#L11).
