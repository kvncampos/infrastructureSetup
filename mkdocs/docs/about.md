# About

Welcome to the "About" section of the Infrastructure Documentation. This page provides background information about the project, including its purpose, goals, and the context in which it was developed.

## Project Purpose and Objectives

The primary goal of this project is to:

- Create Two Web Servers
- Create a LB that will serve the users
- Create a Nagio Server to monitor all servers
- Lockdown the system to limited ports
    - HTTP for LB only
    - SSH for Nagios Only
        - Nagios having SSH capability to all other Servers.

## Key Features

This system includes the following highlights:

- **Scalability**: Designed to grow with the organization's needs.
    - Additional Services can be introduced for additional Web Servers if Needed.
- **Reliability**: Built with robust principles to ensure uptime and performance.
    - One can add additional(reduncant LB to the mix)
- **Simplicity**: Easy to deploy, maintain, and scale.
    - Local Development via Docker for ease of development.

## Team and Contributions

This project was developed by:

- Kevin Campos: Automation Engineer
- Visit [Porfolio](https://mywebdev-resume.com){:target="_blank"} for more information about me.

## Acknowledgments

We would like to thank the following tools and frameworks that made this project possible:

- **Python**: The core programming language used to build and manage the project.
- **Docker**: Streamlined containerization for deployment and testing.
- **Flask**: Lightweight web framework for creating and managing web components.
- **python-dotenv**: Environment variable management for configuration.
- **mkdocs-material**: Elegant and feature-rich theme for project documentation.

These tools were instrumental in the development, deployment, and documentation of the project.


## Learn More

To explore more about the project, visit:

- [Infrastructure Overview](index.md)
