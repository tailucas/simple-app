# simple-app

A minimal reference application extending [base-app](https://github.com/tailucas/base-app) with practical examples of multi-language application development (Python, Java, Rust) within a containerized environment.

**Key Features:**
- Extends [base-app](https://github.com/tailucas/base-app) Docker image from [GitHub Container Registry](https://github.com/tailucas/base-app/pkgs/container/base-app)
- Multi-language support: Python 3.12+ with async patterns, Java 25 with Spring Boot parent, Rust (2021 edition)
- Demonstrates practical threading, configuration management, and inter-process communication patterns
- Example cron job integration (`simplejob.sh` runs every 5 minutes)
- Ready for development via VS Code dev containers with Docker-out-of-Docker support
- Licensed under MIT

# Getting Started

This project uses [VS Code Dev Containers](https://containers.dev/) for a consistent development environment. You will need:

1. **[Docker](https://docs.docker.com/engine/install/)** with Compose and proper user group configuration:
   ```bash
   # Add current user to docker group to avoid sudo requirement
   sudo usermod -aG docker $USER
   ```
   Also install the [Docker Compose CLI plugin](https://docs.docker.com/compose/install).

2. **[Dev Container CLI](https://code.visualstudio.com/docs/devcontainers/devcontainer-cli)**: Requires [Node.js](https://nodejs.org/en/download/package-manager) for installation.

3. **This project**: Clone the repository
   ```bash
   git clone https://github.com/tailucas/simple-app.git
   cd simple-app
   ```

## Starting the Development Container

### Option A: Using Make (recommended)
```bash
make
```

The `Makefile` default target automatically:
- Builds the dev container
- Starts the container
- Connects your terminal to a `vscode` user session inside the container

```
vscode ➜ /workspace/simple-app (main) $ whoami
vscode
```

### Option B: Using VS Code
1. Open the `simple-app` folder in [VS Code](https://code.visualstudio.com/)
2. VS Code automatically detects `.devcontainer/` configuration
3. Click "Reopen in Container" when prompted
4. Open a terminal within VS Code to use the dev container environment

## Exploring the Project

The development container includes all build tools: Python 3, Java 25, Rust, Maven, and uv dependency manager.

### Python Application
- **File**: `./app/__main__.py` (70 lines)
- **Demonstrates**:
  - Async patterns using `asyncio`
  - Configuration loading with `app_config`
  - Signal handling and graceful shutdown
  - Threading with `thread_nanny` for automatic thread lifecycle management
  - Integration with [tailucas_pylib][pylib-url]
- **Dependencies**: Managed with [uv][uv-url] (see [pyproject.toml](pyproject.toml))
  - Requires: `tailucas-pylib>=0.5.2`
- **Run in container**: `uv run python app/__main__.py`

### Java Application
- **File**: `./src/main/java/simple/app/App.java`
- **Demonstrates**:
  - Spring Boot parent project integration
  - SLF4J logging with proper JVM locale handling
  - INI configuration file reading
  - Shutdown hook patterns
- **Parent**: Spring Boot 3.4.13
- **Build**: Maven 3.9+ (executed during container build)
- **Output JAR**: `app.jar` (compiled into container)
- **Dependencies**: ini4j, commons-lang3, SLF4J, Jackson, ZeroMQ, MQTT, RabbitMQ, Sentry, Prometheus metrics

### Rust Components
- **Library** (`rlib/`): Shared utility functions
- **Application** (`rapp/`): Example binary demonstrating library usage
- **Demonstrates**: Workspace structure with library and binary crates

## Configuration

The application inherits all base-app configuration patterns. Key customizations:

### Application Configuration
- **File**: `./config/app.conf`
- **Settings**:
  - `shutting_down_grace_secs=5`: Graceful shutdown timeout
  - `simple_config=42`: Example configuration value (accessed by Java and Python apps)

### Cron Jobs
- **File**: `./config/cron/simplejob`
- **Schedule**: Runs every 5 minutes (`*/5 * * * *`)
- **Script**: `./simplejob.sh` - Demonstrates environment variable loading and syslog integration

### Custom Entrypoint
- **File**: `./app_entrypoint.sh`
- **Purpose**: Allows custom initialization logic before application startup

## Building and Running

### Build the Application Container
Inside the development container:
```bash
task build
```

This uses Docker to compile:
- Java application via Maven (produces `app.jar`)
- Python dependencies via uv
- Rust components

### Configure Runtime Environment
```bash
task configure
```

Generates `.env` file from:
- `base.env` template
- 1Password Secrets (requires running 1Password Connect server)

### Run the Application

**Foreground (interactive, see logs in real-time):**
```bash
task run
```

**Background (detached, container persists after terminal closes):**
```bash
task rund
```

The background mode works because the dev container has `docker-outside-of-docker` enabled, allowing you to exit the container while the application continues running on your host Docker daemon.

### View Application Logs
Application logs are sent to syslog. Inside the container:
```bash
tail -f /var/log/syslog | grep simple-app
```

Or on the host machine:
```bash
docker logs <container-name>
```

## Project Structure

```
simple-app/
├── app/                          # Python application
│   ├── __init__.py
│   └── __main__.py               # Async app with signal handling
├── src/                          # Java application
│   ├── main/java/simple/app/
│   │   └── App.java              # Spring Boot example
│   └── test/java/simple/app/
│       └── AppTest.java
├── rapp/                         # Rust application (binary)
│   ├── Cargo.toml
│   └── src/main.rs
├── rlib/                         # Rust library
│   ├── Cargo.toml
│   └── src/lib.rs
├── config/                       # Application configuration
│   ├── app.conf                  # INI-format configuration
│   └── cron/simplejob            # Cron schedule (every 5 min)
├── Dockerfile                    # Multi-stage build extending base-app
├── docker-compose.yml            # Container orchestration
├── Taskfile.yml                  # Build orchestration (task CLI)
├── Makefile                      # Dev container setup
├── pyproject.toml               # Python project config (uv)
├── pom.xml                      # Java project config (Maven)
├── Cargo.toml                   # Rust workspace config
└── .devcontainer/               # VS Code dev container
    ├── Dockerfile
    ├── devcontainer.json        # Configuration
    └── dev-env-deps.sh          # Post-create setup script
```

## Build System Overview

### Task CLI (Taskfile.yml)
Primary build orchestration inside the application container:
- `task build` - Build Docker image
- `task run` - Run container in foreground
- `task rund` - Run container detached
- `task configure` - Generate runtime .env from secrets
- `task java` - Build Java artifacts with Maven
- `task python` - Setup Python virtual environment with uv
- `task datadir` - Prepare shared data directory
- `task push` - Push image to Docker registry

### Make (Makefile)
Development container setup:
- `make` / `make dev` - Build and enter dev container
- `make check` - Verify required tools installed

### Dockerfile
Multi-stage build extending `tailucas/base-app:latest`:
1. **Builder stage**: Compiles Java artifacts
2. **Final stage**:
   - Installs additional system packages (html-xml-utils, wget)
   - Copies Python application code
   - Copies Rust source files
   - Builds and optimizes all components
   - Runs as user `app` (UID 999)

### Docker Compose
- Uses `base.env` for default environment
- Generates `.env` from 1Password Secrets
- Exposes ports: 4041, 8095, 8085, 9400
- Mounts shared data volume at `/data`
- Logs to syslog on Docker host
- Requires 1Password Connect server to be running

## Dependencies

### Python (via uv)
- `tailucas-pylib>=0.5.2` - Common utilities for threading, configuration, credentials, logging

### Java (via Maven)
- **Spring Boot 3.4.13** - Parent project
- Core: commons-lang3, ini4j, SLF4J
- Messaging: ZeroMQ, RabbitMQ, MQTT/Paho
- Monitoring: Sentry, Prometheus metrics
- Data: Jackson (JSON/MessagePack)

### Rust (Cargo)
- `rlib` - Local library dependency in `rapp`

### Base-App Inheritance
This project extends `tailucas/base-app:latest` which provides:
- Ubuntu base image with build tools
- Java 25 (Amazon Corretto via SDKMan)
- Python 3.12+ with uv
- Rust toolchain
- Supervisor process management
- Cron integration
- Syslog configuration
- ZeroMQ support
- AWS CLI support
- 1Password Secrets Automation integration

## Development Workflow

### Direct Application Execution (for testing)

**Python**: Inside dev container
```bash
uv run python app/__main__.py
```

**Java**: Run directly from VS Code or command-line
```bash
java -cp target/app-0.1.0.jar:target/dependency/* simple.app.App
```

**Rust**: Build and run
```bash
cargo run --manifest-path rapp/Cargo.toml
```

### Container-Based Execution (for integration testing)

Build the full application container and run with all components:
```bash
task build      # Compile Java/Python/Rust, create Docker image
task configure  # Setup .env from 1Password secrets
task run        # Start container with all services via supervisor
```

The container runs:
- **Python** app via supervisor (`app` program section)
- **Java** app via supervisor (`java` program section)
- **Cron** daemon (configured in supervisor)
- **Syslog** logging aggregation

## Notes

### Environment Variables

Key environment variables that affect behavior:

- `NO_PYTHON_APP`: Set to any value to skip Python app startup
- `RUN_JAVA_APP`: Set to `false` to skip Java app startup (default: `true`)
- `CONTAINER_NAME`: Docker image name (set in `base.env`)
- `DEVICE_NAME`: Container hostname (set via 1Password secrets)
- `LC_ALL` / `LANG` / `LANGUAGE`: Locale settings for currency/date formatting

### Extending Simple-App

To use this as a template for your own application:

1. Modify `app/__main__.py` for your Python logic
2. Replace `src/main/java/simple/app/App.java` with your Java code
3. Update `rapp/` for your Rust binary logic
4. Customize `config/app.conf` and `config/cron/*` for your needs
5. Update entrypoint scripts as needed

### Troubleshooting

**Import errors in Python development:**
- Ensure VS Code has selected `./.venv/bin/python` as the Python runtime
- Run `uv sync` to install dependencies in the virtual environment

**Java compilation errors:**
- Verify `javac` and `mvn` are available: `javac -version && mvn -v`
- Check Maven dependencies: `mvn dependency:tree`

**Application logs not visible:**
- Inside container: `tail -f /var/log/syslog | grep simple-app`
- From host: `docker logs <container-name>` or check Docker syslog driver output
- Verify syslog is running: `sudo systemctl status rsyslog`

**1Password Connect issues:**
- Ensure 1Password Connect server container is running on host
- Verify `OP_CONNECT_HOST`, `OP_CONNECT_TOKEN`, `OP_VAULT` environment variables
- Test connection: `docker compose run app /opt/app/dot_env_setup.sh`

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## References

- [base-app](https://github.com/tailucas/base-app) - Extended base image
- [tailucas-pylib][pylib-url] - Python utilities
- [Spring Boot](https://spring.io/projects/spring-boot) - Java framework parent
- [uv][uv-url] - Python package manager
- [Rust Edition 2021](https://doc.rust-lang.org/edition-guide/rust-2021/index.html)
- [ZeroMQ][zmq-url] - Message queue library
- [1Password Secrets Automation][1p-url] - Secrets management

<!-- MARKDOWN LINKS -->
[1p-url]: https://developer.1password.com/docs/connect/
[pylib-url]: https://github.com/tailucas/pylib
[uv-url]: https://docs.astral.sh/uv/
[zmq-url]: https://zeromq.org/
