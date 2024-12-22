# Dockerized Services

This section explains the Dockerized architecture of the project, covering the configuration of various services, their interactions, and decisions made along the way. Below, you'll find detailed insights into the tools, technologies, and configurations used to build a robust and scalable Dockerized environment.

---

## Overview

??? info "What You'll Learn"
    By the end of this section, you will understand:

    - How the project's services are containerized using Docker.
    - The purpose and configuration of each service, including HAProxy, web servers, and Nagios.
    - Key challenges faced during the setup and how they were overcome.
    - Lessons learned and future improvements for scaling and optimization.

This project relies on Docker to create isolated and reproducible environments for running its services. The use of Docker Compose ensures seamless coordination and deployment.

---

## Dockerized Setup

The following services are defined in the `docker-compose.yml` file:

### HAProxy

- **Image**: Built from the `Dockerfile.dev` in `./infrastructure/load_balancer`.
- **Purpose**: Acts as a load balancer to distribute traffic between the web servers.
- **Ports**: Maps the port range `60000-60001` to the host for testing purposes.
- **Dependencies**: Depends on `web-a` and `web-b` services to ensure they start first.

### Web Servers

- **Web-A**: A simple web server configured to respond with the message "Web Server: A".
    - **Image**: Built from `Dockerfile.dev` in `./infrastructure/web_server`.
    - **Environment**: Injects the environment variable `MESSAGE="Web Server: A"`.
    - **Ports**: Maps container port `5001` to host port `5001`.
- **Web-B**: Similar setup as Web-A, but configured to respond with "Web Server: B".
    - **Environment**: Sets `MESSAGE="Web Server: B"`.
    - **Ports**: Maps container port `5002` to host port `5002`.

### Nagios

- **Image**: Uses the official `jasonrivers/nagios:latest` image for monitoring.
- **Purpose**: Provides a monitoring interface to observe the health and performance of services.
- **Configuration**:
    - Mounts configuration files and scripts into the container:
        - `/opt/nagios/etc`: Maps the `etc` directory for Nagios configurations.
        - `/opt/nagios/libexec`: Maps the `libexec` directory for custom plugins.
    - **Ports**: Exposes Nagios on host port `8080`.
    - **Environment**: Sets `NAGIOS_TIMEZONE=UTC` for consistent timestamps.
    - **Restart Policy**: Always restarts to ensure availability.

### MkDocs

- **Image**: Uses the official `squidfunk/mkdocs-material` image.
- **Purpose**: Serves project documentation locally during development.
- **Configuration**:
    - Maps the local `mkdocs` directory into the container for live edits.
    - **Ports**: Serves documentation on host port `8000`.

### Network

- **Name**: `expensify_network` (custom bridge network).
- **Purpose**: Ensures seamless communication between all containers.

---

## Challenges Faced

??? danger "Challenges Encountered"
    - **Dependency Management**: Ensuring all services start in the correct order.
    - **Port Conflicts**: Avoiding collisions when mapping multiple container ports to the host.
    - **Configuration Complexity**: Managing multiple configuration files and ensuring they work seamlessly.

How I Solved Them

- **Dependency Management**: Used the `depends_on` key in `docker-compose.yml` to specify service dependencies.
- **Port Conflicts**: Assigned unique ports for each service and documented mappings clearly.
- **Configuration Complexity**: Organized configuration files into well-defined directories for easier maintenance.

---

## Lessons Learned

??? quote "Key Takeaways"
    - Docker Compose simplifies service orchestration but requires clear documentation for maintainability.
    - Using environment variables allows dynamic configurations and easier scaling.
    - Consistent naming conventions and well-structured directories significantly improve project clarity.

---

!!! question "Future Enhancements"
    - **Scaling**: Investigate Docker Swarm or Kubernetes for scaling the architecture to handle higher traffic.
    - **Monitoring**: Enhance monitoring with Prometheus and Grafana for detailed insights.
    - **Security**: Implement SSL/TLS termination at HAProxy for secure communication.
