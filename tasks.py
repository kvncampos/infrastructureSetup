from invoke import task
from dotenv import load_dotenv
import os

load_dotenv()

ENVIRONMENT = os.getenv("ENV", "development")
DOCKER_PATH = (
    "docker-compose.dev.yml"
    if ENVIRONMENT == "development"
    else "docker-compose.prod.yml"
)


@task
def build(c):
    """Build all Docker images using docker-compose."""
    c.run(f"docker compose -f {DOCKER_PATH} build")


@task()
def up(c):
    """Start all services."""
    command = f"docker compose -f {DOCKER_PATH} up -d"
    c.run(command)


@task(help={"service": "Name of the service to start."})
def start(c, service=""):
    """Start services."""
    command = f"docker compose -f {DOCKER_PATH} start"
    if service:
        command += f" {service}"
    c.run(command)


@task(help={"service": "Name of the service to debug (default: nagios)."})
def debug(c, service=""):
    """Start all services in detached mode and attach to a specific service."""
    if service:
        # Start all services in detached mode
        c.run(f"docker compose -f {DOCKER_PATH} up -d")
        # Attach to the specified service
        c.run(f"docker compose -f {DOCKER_PATH} up {service}")

    else:
        # Attach to the specified service
        c.run(f"docker compose -f {DOCKER_PATH} up {service}")


@task(help={"service": "Name of the service to restart (optional)."})
def restart(c, service=""):
    """Restart services."""
    command = f"docker compose -f {DOCKER_PATH} restart"
    if service:
        command += f" {service}"
    c.run(command)


@task(help={"service": "Name of the service to stop (optional)."})
def stop(c, service=""):
    """Stop services."""
    command = f"docker compose -f {DOCKER_PATH} stop"
    if service:
        command += f" {service}"
    c.run(command)


@task(help={"volumes": "Remove all volumes, including orphans (default: True)."})
def destroy(c, volumes=True):
    """Destroy all containers, orphaned volumes, and images."""
    command = f"docker compose -f {DOCKER_PATH} down --rmi all"
    if volumes:
        command += " --volumes"
    c.run(command)


@task(help={"service": "The name of the specific service to view logs for (optional)."})
def logs(c, service=None):
    """View logs for all or a specific service."""
    command = f"docker compose -f {DOCKER_PATH} logs"
    if service:
        command += f" {service}"
    c.run(command)


@task(
    help={
        "container_name": "The name of the Docker container to access (default: nagios)."
    }
)
def shell(c, container_name="nagios"):
    """
    Open a shell inside the specified Docker container.
    """
    print(f"Opening shell in container: {container_name}")
    try:
        # Attempt to use bash
        c.run(f"docker exec -it {container_name} bash", pty=True)
    except Exception as e:
        print("bash not found. Trying sh...")
        # Fallback to sh if bash is not available
        c.run(f"docker exec -it {container_name} sh", pty=True)


@task
def serve_docs(c):
    """
    Start the MkDocs documentation service on port 8000.
    """
    print("Starting MkDocs documentation service on http://localhost:8000...")
    c.run("mkdocs serve -f mkdocs/mkdocs.yml", pty=True)


@task
def black(ctx):
    """Format Python files in the infrastructure/web_server/ folder with black."""
    python_path = "infrastructure/web_server/"
    print(f"Formatting Python files in {python_path} with black...")
    ctx.run(f"black {python_path}", pty=True)


@task
def ruff(ctx, fix=False):
    """Lint Python files in the infrastructure/web_server/ folder with ruff."""
    python_path = "infrastructure/web_server/"
    print(f"Linting Python files in {python_path} with ruff...")
    ruff_command = f"ruff check {python_path}"
    if fix:
        ruff_command += " --fix"
    print(f"Running command: {ruff_command}")
    ctx.run(ruff_command, pty=True)


@task(pre=[black, ruff])
def check_python(ctx):
    """Run linting and formatting for Python files."""
    print("Python linting and formatting completed!")


@task
def lint_html(ctx):
    """Lint HTML files with tidy."""
    print("Linting HTML files...")
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                print(f"Linting {filepath}...")
                ctx.run(f"tidy -e {filepath}", warn=True)


@task
def lint_haproxy(ctx):
    """Validate HAProxy configuration."""
    print("Validating HAProxy configuration...")
    haproxy_cfg = "infrastructure/load_balancer/haproxy.cfg"
    if os.path.exists(haproxy_cfg):
        ctx.run(f"haproxy -c -f {haproxy_cfg}", pty=True)
    else:
        print(f"HAProxy config file {haproxy_cfg} not found.")


@task
def lint_nagios(ctx):
    """Validate Nagios configuration."""
    print("Validating Nagios configuration...")
    nagios_cfg = "/infrastructure/nagios/etc/nagios.cfg"
    if os.path.exists(nagios_cfg):
        ctx.run(f"nagios -v {nagios_cfg}", pty=True)
    else:
        print(f"Nagios config file {nagios_cfg} not found.")


@task(pre=[check_python, lint_html, lint_haproxy, lint_nagios])
def lint_all(ctx):
    """Run all linting tasks."""
    print("All linting tasks completed!")


@task
def pytest(ctx, path="infrastructure/tests/"):
    """Run pytest on the specified test path (default: infrastructure/tests/)."""
    print(f"Running pytest in {path}...")
    ctx.run(f"pytest {path}", pty=True)
